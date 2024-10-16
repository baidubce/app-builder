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
import base64
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

    def file_to_base64(self, file_path):
        """
        读取指定路径的文件并将其内容转换为Base64编码的字符串。

        :param file_path: 文件的本地路径
        :return: Base64编码的字符串
        """
        try:
            # 以二进制模式读取文件内容
            with open(file_path, "rb") as file:
                file_data = file.read()

            # 将文件内容编码为Base64
            base64_encoded_data = base64.b64encode(file_data).decode('utf-8')

            return base64_encoded_data

        except Exception as e:
            print(f"读取文件或编码过程中出错: {e}")
            return None

