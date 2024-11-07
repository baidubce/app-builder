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
from pydantic import Field
from enum import Enum
from appbuilder.core.component import ComponentArguments


class QueryTypeChoices(Enum):
    questions = '问题'
    phrases = '短语'
    questions_and_phrases = '全部'

    def to_chinese(self):
        """
        将QueryTypeChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是QueryTypeChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            QueryTypeChoices.questions: '问题',
            QueryTypeChoices.phrases: '短语',
            QueryTypeChoices.questions_and_phrases: '全部'
        }
        return descriptions[self]


class OutputFormatChoices(Enum):
    json_format = 'json'
    str_format = 'str'

    def to_chinese(self):
        """
        将OutputFormatChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是OutputFormatChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            OutputFormatChoices.json_format: 'json',
            OutputFormatChoices.str_format: 'str'
        }
        return descriptions[self]


class OralQueryGenerationArgs(ComponentArguments):
    """口语化Query生成配置
    """
    text: str = Field(...,
                      valiable_name='text',
                      description='输入文本，用于生成Query')
    query_type: QueryTypeChoices = Field(...,
                                         variable_name='query_type',
                                         description='待生成的query类型，可选值为问题、短语和全部（问题+短语）。')
    output_format: QueryTypeChoices = Field(...,
                                            variable_name='output_format',
                                            description='输出格式，可选值为json、str。')