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


class StyleQueryChoices(Enum):
    """
    StyleQueryChoices是一个枚举类型，包含三个选项：
    
    Attributes:
        BILIBILI ("B站")
        XIAOHONGSHU ("小红书")
        GENERAL ("通用")
    """
    BILIBILI = "B站"
    XIAOHONGSHU = "小红书"
    GENERAL = "通用"

    def to_chinese(self):
        """
        将StyleQueryChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是StyleQueryChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            StyleQueryChoices.BILIBILI: "B站",
            StyleQueryChoices.XIAOHONGSHU: "小红书",
            StyleQueryChoices.GENERAL: "通用",
        }
        return descriptions[self]


class LengthChoices(Enum):
    SHORT = 100  # 短
    MEDIUM = 300  # 中
    LONG = 600  # 长

    def to_chinese(self):
        """
        将LengthChoices枚举对象转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            str: 转换后的中文描述，包括"短"、"中"和"长"。
        
        """
        descriptions = {
            LengthChoices.SHORT: "短",
            LengthChoices.MEDIUM: "中",
            LengthChoices.LONG: "长",
        }
        return descriptions[self]


class StyleWritingArgs(ComponentArguments):
    """
    风格写作配置

    Attributes:
        message: Message = Field(...)
        style_query: StyleQueryChoices = Field(...)
        length: LengthChoices = Field(...)
    """
    message: Message = Field(...,
                             variable_name="query",
                             description="输入消息，用于模型的主要输入内容，例如'帮我生成一个介绍保温杯的话术'")
    style_query: StyleQueryChoices = Field(...,
                                           variable_name="style_query",
                                           description="风格查询选项，可选值为 'B站', '小红书', '通用'。")
    length: LengthChoices = Field(...,
                                  variable_name="length",
                                  description="输出长度，可选值为 '短' (100), '中' (300), '长' (600)。")