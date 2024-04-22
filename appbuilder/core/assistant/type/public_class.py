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
from enum import Enum
from typing import Union
from typing import Optional

class AssistantFunctionCall(BaseModel):
    name: str
    arguments: str


class AssistantExample(BaseModel):
    role: str = "user"
    content: str
    function_call: AssistantFunctionCall


class AssistantFunctionJsonSchema(BaseModel):
    type: str = 'object'
    properties: Union[dict, None] = None
    required: Union[list[str], None] = None


class AssistantFunction(BaseModel):
    name: str
    description: str
    parameters: Union[AssistantFunctionJsonSchema, None] = None
    responses:  Union[AssistantFunctionJsonSchema, None] = None
    examples: Union[list[list[AssistantExample]], None] = None


class AssistantTool(BaseModel):
    type: str = 'function'
    function: AssistantFunction = None


class ResponseFormat(str, Enum):
    TEXT = 'text'
    JSON_OBJECT = 'json_object'


class AssistantModel(str, Enum):
    ERNIE_408K = 'ERNIE-4.0-8K'

class AssistantText(BaseModel):
    value: str = ""
    annotations: Optional[list[str]] = None


class AssistantContent(BaseModel):
    type: str = "text"
    text: Optional[AssistantText] = None
