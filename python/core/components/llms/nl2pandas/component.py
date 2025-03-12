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
from pydantic import BaseModel, Field
from typing import Optional
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import Nl2pandasArgs
 
class Nl2pandasComponent(CompletionBaseComponent):
    """
    自然语言转pandas大模型组件， 基于生成式大模型对query进行理解并生成对应语义的可执行python代码（主要使用pandas），可用于基于表格的查询、问答等多种场景。

    Examples:

    .. code-block:: python

        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'
        table_info = '''表格列信息如下：
        学校名 : 清华附小 , 字符串类型，代表小学学校的名称
        所属地区 : 西城区 , 字符串类型，表示该小学学校所在的位置
        创办时间 : 1998 , 数字值类型，表示该小学学校的创办时间
        类别 : 公立小学 , 字符串类型，表示该小学学校所在的类别
        学生人数 : 2000 , 数字值类型，表示该小学学校的学生数量
        教职工人数 : 140 , 数字值类型，表示该小学学校的教职工数量
        教学班数量 : 122 , 数字值类型，表示该小学学校的教学班数量
        '''
        query = "海淀区有哪些学校"
        query = appbuilder.Message(query)
        
        nl2pandas = appbuilder.Nl2pandasComponent(model="Qianfan-Agent-Speed-8K")
        answer = nl2pandas(query, table_info = table_info)
    """
    name = "nl2pandas"
    version = "v1"
    meta = Nl2pandasArgs

    manifests = [
        {
            "name": "nl2pandas",
            "description": "输入用户查询query，基于生成式大模型对query进行理解并生成对应语义的可执行python代码（主要使用pandas），可用于基于表格的查询、问答等多种场景",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "text": "string",
                        "description": "输入问题，一般是针对表格信息的提问，例如'海淀区的小学有哪些'"
                    },
                    "table_info": {
                        "text": "string",
                        "description": "表格信息，一般是表格列名以及对应列名的举例和释义，例如'表格列信息如下：\n学校名 : 清华附小 , 字符串类型，代表小学学校的名称"
                    }
                },
                "required": [
                    "query",
                    "table_info"
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
        """初始化Nl2pandasComponent模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
                Nl2pandasArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

    @components_run_trace
    def run(self, message, table_info=None, stream=False, temperature=1e-10, top_p=0):
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (obj:`Message`): 输入问题，通常是针对表格信息的提问，如'海淀区的小学有哪些'。这是一个必需的参数。
            table_info (obj:`Message`, optional): 表格信息，包括表格列名、对应列名的示例和释义。默认值为 None，但这是一个必需的参数。
            stream (bool, optional): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, optional): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, table_info=table_info, stream=stream, temperature=temperature, top_p=top_p)

    @components_run_stream_trace
    def tool_eval(self, name: str, streaming: bool = False, **kwargs):
        """
        tool_eval for function call
        """
        traceid = kwargs.get("traceid")
        query = kwargs.get("query", None)
        table_info = kwargs.get("table_info", None)
        if not query or not table_info:
            raise ValueError("param `query` and 'table_info' are required")
        msg = Message(query)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, table_info=table_info, stream=False, temperature=temperature,
                              top_p=top_p, request_id=traceid)

        if streaming:
            yield str(message.content)
        else:
            return str(message.content)
