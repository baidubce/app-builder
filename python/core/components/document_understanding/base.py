"""
Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from pydantic import Field
from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments



class DocumentUnderstandingArgs(ComponentArguments):
    '''长文档问答配置'''
    message: Message = Field(...,
                         variable_name="query",
                         description="用户输入query")
    file_path: str = Field(...,
                           variable_name="file_path",
                             description="用户上传的文件路径")
    instruction: str = Field(default="",
                           variable_name='instruction',
                           description='用户指令')
    addition_instruction: str = Field(default="",
                                      variable_name='addition_instruction',
                                      description='用户增强指令')