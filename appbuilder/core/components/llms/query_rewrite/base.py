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

class RewriteTypeChoices(Enum):
    """
    多轮改写类型选择
    """
    user_assistant_user = "带机器人回复"
    user_user = "仅用户查询"

    def to_chinese(self):
        """
        将RewriteTypeChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是RewriteTypeChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            RewriteTypeChoices.user_assistant_user: "带机器人回复",
            RewriteTypeChoices.user_user: "仅用户查询",
        }
        return descriptions[self]


class QueryRewriteArgs(ComponentArguments):
    """
    多轮改写配置
    
    Attributes:
        message: Message = Field(...)
        rewrite_type: RewriteTypeChoices = Field(...)
    """
    message: Message = Field(..., 
                             variable_name="query",
                             description="输入消息，用于模型的主要输入内容，例如'['我应该怎么办理护照？', '您可以查询官网或人工咨询', \
                                         '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']'")
    rewrite_type: RewriteTypeChoices = Field(...,  
                                             variable_name="rewrite_type",
                                             description="改写类型选项，可选值为 '带机器人回复'(改写时参考user查询历史和assistant回复历史)，\
                                                         '仅用户查询'(改写时参考user查询历史)。 默认是'带机器人回复'. ")