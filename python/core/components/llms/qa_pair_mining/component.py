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
from pydantic import Field
from typing import Optional

from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import QAPairMiningMeta


class QAPairMining(CompletionBaseComponent):
    """ 
    基于输入文本内容，快速生成多个问题及对应答案,极大提高信息提炼的效率和准确性.广泛用于在线客服、智能问答等领域。

    Examples:

    .. code-block:: python
        import os
        import appbuilder

        os.environ["APPBUILDER_TOKEN"] = "..."

        qa_mining = appbuilder.QAPairMining(model="Qianfan-Agent-Speed-8K")
        # 输入文本（对此文本挖掘问答对）
        msg =  '2017年，工商银行根据外部宏观环境变化，及时调整业务策略，优化资产负债结构，' + \
            '保持存贷款业务协调发展，提升资产负债配置效率。' + \
            '2018年3月末，工商银行总资产264,937.81亿元，比上年末增加4,067.38亿元。'
        msg = appbuilder.Message(msg)
        answer = qa_mining(msg)

        print(">>> Output: {}".format(answer.content))
    
    """
    name = "qa_pair_mining"
    version = "v1"
    meta = QAPairMiningMeta

    manifests = [
        {
            "name": "qa_pair_mining",
            "description": "基于输入文本内容，快速生成多个问题及对应答案，极大提高信息提炼的效率和准确性。广泛用于在线客服、智能问答等领域。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "输入消息，用于模型的输入，一般为文档段落。"
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
        """初始化QAPairMining(问答对挖掘)模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
                QAPairMiningMeta, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10, top_p=0.0):
        """
        给定输入（message）到模型运行，同时指定运行参数，并返回结果。
        
        Args:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, optional): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, optional): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature, top_p=top_p)

    @components_run_stream_trace
    def tool_eval(self, name: str, streaming: bool = False, **kwargs):
        """
        tool_eval for function call
        """
        traceid = kwargs.get("traceid")
        query = kwargs.get("query", None)
        if not query:
            raise ValueError("param `query` is required")
        msg = Message(query)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, stream=False, temperature=temperature, top_p=top_p, request_id=traceid)

        if streaming:
            yield str(message.content)
        else:
            return str(message.content)
