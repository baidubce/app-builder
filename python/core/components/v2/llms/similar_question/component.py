# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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

""" similar question
"""
from typing import Optional

from appbuilder.core.message import Message
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from appbuilder.core.components.llms.similar_question.base import SimilarQuestionMeta


class SimilarQuestion(CompletionBaseComponent):
    r""" 
    基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
    
    Examples:

    .. code-block:: python
        
        import os
        import appbuilder

        os.environ["APPBUILDER_TOKEN"] = "..."

        qa_mining = appbuilder.SimilarQuestion(model="Qianfan-Agent-Speed-8K")

        msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        msg = appbuilder.Message(msg)
        answer = qa_mining(msg)

        print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    manifests = [
        {
            "name": "similar_question",
            "description": "基于输入的问题，挖掘出与该问题相关的类似问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "输入的问题，用于大模型根据该问题输出相关的类似问题。"
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
            model: str="Qianfan-Agent-Speed-8K",
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = True,
            **kwargs
    ):
        """初始化StyleRewrite模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
            **kwargs: 其他关键字参数.
        
        Returns:
            None
        
        """
        super().__init__(
            SimilarQuestionMeta, model=model, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification, **kwargs)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10, top_p=0.0, request_id=None):
        """
        给定输入（message）到模型运行，同时指定运行参数，并返回结果。
        
        Args:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p(float, 可选): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature, top_p=top_p, request_id=request_id)

    @components_run_stream_trace
    def tool_eval(self, 
                  query: str,
                  **kwargs):
        """
        根据给定的query和可选参数生成并返回文本输出。
        
        Args:
            query (str): 需要生成文本的输入查询字符串。
            **kwargs: 其他可选参数。
        
        Returns:
            Generator[Output]: 返回一个生成器，生成类型为Output的对象。
        
        """
        traceid = kwargs.get("_sys_traceid", "")
        msg = Message(query)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, stream=False, temperature=temperature, top_p=top_p, request_id=traceid)
        
        yield self.create_output(type="text", text=str(message.content), name="text", usage=message.token_usage)