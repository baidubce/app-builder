"""text to pandas"""
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


"""
自然语言转pandas
"""
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message
from pydantic import BaseModel, Field
from typing import Optional
from appbuilder.core.component import ComponentArguments


class Nl2pandasArgs(ComponentArguments):
    """自然语言转pandas代码 参数配置"""
    message: Message = Field(..., 
                             variable_name="query", 
                             description="输入问题，一般是针对表格信息的提问，例如'海淀区的小学有哪些'")
    table_info: str = Field(...,  
                                variable_name="table_info", 
                                description="表格信息，一般是表格列名以及对应列名的举例和释义，例如'表格列信息如下：\n学校名 : 清华附小 , 字符串类型，代表小学学校的名称")
 
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
            
            nl2pandas = appbuilder.Nl2pandasComponent(model="ERNIE Speed-AppBuilder")
            answer = nl2pandas(query, table_info = table_info)
    """
    name = "nl2pandas"
    version = "v1"
    meta = Nl2pandasArgs

    def __init__(
        self, 
        model=None,
        secret_key: Optional[str] = None, 
        gateway: str = "",
        lazy_certification: bool = False,
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

    def run(self, message, table_info=None, stream=False, temperature=1e-10, top_p=0):
        """
        使用给定的输入运行模型并返回结果。

        参数:
            query (obj:`Message`): 输入问题，一般是针对表格信息的提问，例如'海淀区的小学有哪些'。这是一个必需的参数。
            table_info (obj:`Message`): 表格信息，是表格列名以及对应列名的举例和释义。无默认值，这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p(float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, table_info=table_info, stream=stream, temperature=temperature, top_p=top_p)
