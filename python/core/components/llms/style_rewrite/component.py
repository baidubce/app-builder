# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message

from typing import Optional
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import StyleRewriteArgs


class StyleRewrite(CompletionBaseComponent):
    """
    文本风格转写大模型组件， 基于生成式大模型对文本的风格进行改写，支持有营销、客服、直播、激励及教学五种话术。

    Examples:

    .. code-block:: python

        import os
        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'

        style_rewrite = appbuilder.StyleRewrite(model="Qianfan-Agent-Speed-8K")
        answer = style_rewrite(appbuilder.Message("文心大模型发布新版本"), style="激励话术")

    """
    name = "style_rewrite"
    version = "v1"
    meta = StyleRewriteArgs

    manifests = [
        {
            "name": "style_rewrite",
            "description": "能够将一段文本转换成不同的风格（营销、客服、直播、激励及教学话术），同时保持原文的基本意义不变。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要改写的文本。"
                    },
                    "style": {
                        "type": "string",
                        "description": "想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选. 默认是营销话术。",
                        "enum": ["营销话术", "客服话术", "直播话术", "激励话术", "教学话术"]
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    def __init__(
            self,
            model=None,
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = False,
            **kwargs
    ):
        """初始化StyleRewrite模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
            StyleRewriteArgs, model=model, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)

    @components_run_trace
    def run(self, message, style="营销话术", stream=False, temperature=1e-10, top_p=0.0, request_id=None):
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            style (str, optional): 想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选。默认为"营销话术"。
            stream (bool, optional): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, optional): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
            obj:`Message`: 模型运行后的输出消息。
        
        """
        return super().run(message=message, style=style, stream=stream, temperature=temperature, top_p=top_p, request_id=request_id)

    @components_run_stream_trace 
    def tool_eval(self, name: str, streaming: bool = False, **kwargs):
        """
        执行工具评估函数
        
        Args:
            name (str): 函数名称，本函数不使用该参数，但保留以符合某些框架的要求。
            streaming (bool, optional): 是否以流的形式返回结果。默认为 False，即一次性返回结果。如果设置为 True，则以生成器形式逐个返回结果。
            **kwargs: 其他参数，包含但不限于：
                traceid (str): 请求的跟踪ID，用于日志记录和跟踪。
                query (str): 待评估的文本。
                style (str, optional): 评估风格，可选值为 ['营销话术', '客服话术', '直播话术', '激励话术', '教学话术']。默认为 '营销话术'。
                model_configs (dict, optional): 模型配置参数，可选的键包括：
                    temperature (float, optional): 温度参数，用于控制生成文本的随机性。默认为 1e-10。
                    top_p (float, optional): top_p 采样参数，用于控制生成文本的多样性。默认为 0.0。
        
        Returns:
            如果 streaming 为 False，则直接返回评估结果字符串。
            如果 streaming 为 True，则以生成器形式逐个返回评估结果字符串。
        
        Raises:
            ValueError: 如果缺少参数 'query'。
        """
        traceid = kwargs.get("traceid")
        query = kwargs.get("query", None)
        if not query:
            raise ValueError("param `query` is required")
        msg = Message(query)
        style = kwargs.get("style", "营销话术")
        if style not in ["营销话术", "客服话术", "直播话术", "激励话术", "教学话术"]:
            style = "营销话术"
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, style=style, stream=False, temperature=temperature, top_p=top_p, request_id=traceid)
        
        if streaming:
            yield str(message.content)
        else:
            return str(message.content)
