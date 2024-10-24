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
from appbuilder.core.component import ComponentArguments
from pydantic import Field


class MrcArgs(ComponentArguments):
    """
    阅读理解问答配置

    Attributes:
        message: Message
            用户输入的查询内容，例如'千帆平台都有哪些大模型？'
        context_list: list
            用户输入的检索片段列表，例如['content1', 'content2', 'content3',...]，也可以为空，即[]
        reject: bool
            控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能
        clarify: bool
            控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能
        highlight: bool
            控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能
        friendly: bool
            控制大模型友好对提升难过能力的开关，为true即为开启友好度提升功能，为false即为关闭重点强调功能
        cite: bool
            控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能
    """
    message: Message = Field(...,
                         variable_name="query",
                         description="输入用户query，例如'千帆平台都有哪些大模型？'")
    context_list: list = Field(...,
                                   variable_name="context_list",
                                   description="用户输入检索片段list，"
                                               "例如[content1, content2, content3,...]，也可以为空, 即[]")
    reject: bool = Field(...,
                         variable_name="reject",
                         description="控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能")
    clarify: bool = Field(...,
                          variable_name="clarify",
                          description="控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能")
    highlight: bool = Field(...,
                            variable_name="highlight",
                            description="控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能")
    friendly: bool = Field(...,
                           variable_name="friendly",
                           description="控制大模型友好对提升难过能力的开关，"
                                       "为true即为开启友好度提升功能，为false即为关闭友好度提升功能")
    cite: bool = Field(...,
                       variable_name="cite",
                       description="控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能")