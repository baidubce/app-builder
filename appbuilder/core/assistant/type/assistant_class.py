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

# class AssitantFileInfo(BaseModel):
#     url: str = ""
#     url_type: str = ""
#     file_name: str = ""
#     file_id: str = ""

# class AssistantAnnotation(BaseModel):
#     type: str = "file_info"
#     text: str = ""
#     start_index: int = 0
#     end_index: int = 0
#     file_info: Union[AssitantFileInfo, None] = None

class AssistantFilesCreateResponse(BaseModel):
    id: str = ""
    bytes: int = 0
    object: str = ""
    purpose: str = ""
    create_at: int = 0
    filename: str = ""
    classification_id: str = ""

class AssistantCreateRequest(BaseModel):
    model: AssistantModel = Field(default="ERNIE-4.0-8K")
    name: str = Field(default="", min_length=1,
                      max_length=64, pattern="^[0-9a-zA-Z_-]+$")
    description: str = Field(default="", max_length=512)
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    instructions: str = Field(default="", max_length=4096)
    thought_instructions: str = Field(default="", max_length=4096)
    chat_instructions: str = Field(default="", max_length=4096)
    tools: list[AssistantTool] = Field(default=[], max_length=10)
    file_ids: list[str] = Field(default=[], max_length=10)
    metadata: dict = Field(default={}, max_length=16)
    assistant_id: str = ""


class AssistantCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    name: str = ""
    description: str = ""
    instructions: str
    tools: Optional[list[AssistantTool]] = Field(default=[])
    created_at: int = 0
    thought_instructions: str = ""
    chat_instructions: str = ""
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    file_ids: Optional[list[str]] = Field(default=[])
