# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

from typing import Optional

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.components.llms.tag_extraction.base import TagExtractionArgs
from appbuilder.core.message import Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class TagExtraction(CompletionBaseComponent):
    """
    标签抽取组件，基于生成式大模型进行关键标签的抽取。

    Examples:

    .. code-block:: python

        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'

        tag_extraction = appbuilder.TagExtraction(model="Qianfan-Agent-Speed-8K")
        answer = tag_extraction(appbuilder.Message("从这段文本中抽取关键标签"))

    """

    name = "tag_extraction"
    version = "v1"
    meta = TagExtractionArgs

    manifests = [
        {
            "name": "tag_extraction",
            "description": "标签抽取组件，基于生成式大模型进行关键标签的抽取。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "输入消息，用于模型的主要输入内容"
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
            model: str = "Qianfan-Agent-Speed-8K",
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = True,
            **kwargs
    ):
        """初始化TagExtraction模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
            TagExtractionArgs, model=model, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10, top_p=0.0):
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (obj:`Message`, 必选): 输入消息，用于模型的主要输入内容。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。
                取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
                默认值为 1e-10。
            top_p (float, 可选): 影响输出文本的多样性，取值越大，生成文本的多样性越强。
                取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
                默认值为 0。
        
        Returns:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature, top_p=top_p)

    @components_run_stream_trace
    def tool_eval(self, query: str, **kwargs):
        """
        tool_eval for function call
        """
        if not query:
            raise ValueError("param `query` is required")
        msg = Message(query)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, stream=False, temperature=temperature, top_p=top_p)

        yield self.create_output(type="text", text=str(message.content), usage=message.token_usage)
