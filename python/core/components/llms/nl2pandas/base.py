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
from appbuilder.core.message import Message
from pydantic import Field
from appbuilder.core.component import ComponentArguments


class Nl2pandasArgs(ComponentArguments):
    """
    自然语言转pandas代码 参数配置

    Attributes:
        message: Message = Field(...)
        table_info: str = Field(...)
    """
    message: Message = Field(..., 
                             variable_name="query", 
                             description="输入问题，一般是针对表格信息的提问，例如'海淀区的小学有哪些'")
    table_info: str = Field(...,  
                                variable_name="table_info", 
                                description="表格信息，一般是表格列名以及对应列名的举例和释义，例如'表格列信息如下：\n学校名 : 清华附小 , 字符串类型，代表小学学校的名称")