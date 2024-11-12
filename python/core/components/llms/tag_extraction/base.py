# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments
from pydantic import Field


class TagExtractionArgs(ComponentArguments):
    """
    标签抽取配置

    Attributes:
        message (Message): 输入消息，用于模型的主要输入内容
    """
    message: Message = Field(...,
                             variable_name="query",
                             description="""输入消息，用于模型的主要输入内容，例如'本实用新型公开了一种可利用热能的太阳能光伏光热一体化组件，
                             包括太阳能电池，还包括有吸热板，太阳能电池粘附在吸热板顶面，吸热板内嵌入有热电材料制成的内芯，吸热板底面设置有蛇形管。
                             本实用新型结构紧凑，安装方便，能充分利用太阳能电池散发的热能，具有较高的热能利用率。'""")