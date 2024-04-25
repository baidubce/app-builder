# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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

from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from appbuilder.core.assistant.type import (
    AssistantTool,
    ResponseFormat,
    AssistantModel
)

# AssistantFilesCreateResponse类，用于描述创建助理文件后的响应信息
class AssistantFilesCreateResponse(BaseModel):
    id: str = ""  # 文件ID
    bytes: int = 0  # 文件大小（字节）
    object: str = ""  # 文件对象标识
    purpose: str = ""  # 文件用途
    create_at: int = 0  # 文件创建时间戳
    filename: str = ""  # 文件名
    classification_id: str = ""  # 文件分类ID

# AssistantCreateRequest类，用于描述创建助理的请求参数
class AssistantCreateRequest(BaseModel):
    model: AssistantModel = Field(default="ERNIE-4.0-8K")  # 使用的模型
    name: str = Field(default="", min_length=1, max_length=64, pattern="^[0-9a-zA-Z_-]+$")  # 助理名称
    description: str = Field(default="", max_length=512)  # 助理描述
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)  # 响应格式
    instructions: str = Field(default="", max_length=4096)  # 助理的通用指令
    thought_instructions: str = Field(default="", max_length=4096)  # 助理的思维指令
    chat_instructions: str = Field(default="", max_length=4096)  # 助理的聊天指令
    tools: list[AssistantTool] = Field(default=[], max_length=10)  # 助理使用的工具列表
    file_ids: list[str] = Field(default=[], max_length=10)  # 关联文件的ID列表
    metadata: dict = Field(default={}, max_length=16)  # 元数据
    assistant_id: str = ""  # 助理ID

# AssistantCreateResponse类，用于描述创建助理后的响应信息
class AssistantCreateResponse(BaseModel):
    id: Optional[str] = ""  # 助理ID
    object: Optional[str] = ""  # 助理对象标识
    name: Optional[str] = ""  # 助理名称
    description: Optional[str] = ""  # 助理描述
    instructions: Optional[str]  # 助理的通用指令
    tools: Optional[list[AssistantTool]] = Field(default=[])  # 助理使用的工具列表
    created_at: Optional[int] = 0  # 助理创建时间戳
    thought_instructions: Optional[str] = ""  # 助理的思维指令
    chat_instructions: Optional[str] = ""  # 助理的聊天指令
    response_format: Optional[ResponseFormat] = Field(default=ResponseFormat.TEXT)  # 响应格式
    file_ids: Optional[list[str]] = Field(default=[])  # 关联文件的ID列表
    metadata: Optional[dict] = Field(default={}, max_length=16)  # 元数据
