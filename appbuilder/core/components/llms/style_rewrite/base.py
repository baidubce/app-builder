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
from enum import Enum


class StyleChoices(Enum):
    """
    StyleChoices枚举类，包含了五种风格：

    Attributes:
        YINGXIAO : 营销话术
        JIAOXUE : 教学话术
        JILI : 激励话术
        KEFU : 客服话术
        ZHIBO : 直播话术
    """
    YINGXIAO = "营销话术"
    JIAOXUE = "教学话术"
    JILI = "激励话术"
    KEFU = "客服话术"
    ZHIBO = "直播话术"

    def to_chinese(self):
        """
        将StyleChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是StyleChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            StyleChoices.YINGXIAO: "营销话术",
            StyleChoices.JIAOXUE: "教学话术",
            StyleChoices.JILI: "激励话术",
            StyleChoices.KEFU: "客服话术",
            StyleChoices.ZHIBO: "直播话术"
        }
        return descriptions[self]


class StyleRewriteArgs(ComponentArguments):
    """
    文本风格转写配置

    Attributes:
        message: Message
        style: StyleChoices
    """
    message: Message = Field(...,
                             variable_name="query",
                             description="需要改写的文本，该字段为必须字段。")
    style: StyleChoices = Field(...,
                                variable_name="style",
                                description="想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选")