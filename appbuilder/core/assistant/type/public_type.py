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
    """
    表示助理功能调用的模型。

    Attributes:
        name (str): 函数调用的名称。
        arguments (str): 函数调用的参数列表。
    """
    name: str
    arguments: str


class AssistantExample(BaseModel):
    """
    表示助理功能示例的模型。

    Attributes:
        role (str): 示例的角色，默认为 "user"。
        content (str): 示例的内容。
        function_call (AssistantFunctionCall): 函数调用的实例。
    """
    role: str = "user"
    content: str
    function_call: AssistantFunctionCall


class AssistantFunctionJsonSchema(BaseModel):
    """
    表示助理功能的JSON Schema的模型。

    Attributes:
        type (str): Schema的类型，默认为 'object'。
        properties (Union[dict, None]): JSON对象的属性，默认为None。
        required (Union[list[str], None]): 必需的属性列表，默认为None。
    """
    type: str = 'object'
    properties: Union[dict, None] = None
    required: Union[list[str], None] = None


class AssistantFunction(BaseModel):
    """
    表示助理功能的模型。

    Attributes:
        name (str): 功能的名称。
        description (str): 功能的描述。
        parameters (Union[AssistantFunctionJsonSchema, None]): 功能的参数Schema，默认为None。
        responses (Union[AssistantFunctionJsonSchema, None]): 功能的响应Schema，默认为None。
        examples (Union[list[list[AssistantExample]], None]): 功能的示例列表，默认为None。
    """
    name: str
    description: str
    parameters: Union[AssistantFunctionJsonSchema, None] = None
    responses:  Union[AssistantFunctionJsonSchema, None] = None
    examples: Union[list[list[AssistantExample]], None] = None


class AssistantTool(BaseModel):
    """
    表示助理工具的模型。

    Attributes:
        type (str): 工具的类型，默认为 'function'。
        function (AssistantFunction): 功能的实例。
    """
    type: str = 'function'
    function: AssistantFunction = None


class ResponseFormat(str, Enum):
    """
    表示响应格式的枚举类型。

    Values:
        TEXT: 文本格式。
        JSON_OBJECT: JSON对象格式。
    """
    TEXT = 'text'
    JSON_OBJECT = 'json_object'


class AssistantText(BaseModel):
    """
    表示助理文本内容的模型。

    Attributes:
        value (str): 文本的值。
        annotations (Optional[list[str]]): 文本的注解列表，默认为None。
    """
    value: str = ""
    annotations: Optional[list[str]] = None


class AssistantContent(BaseModel):
    """
    表示助理内容的模型。

    Attributes:
        type (str): 内容类型，默认为 "text"。
        text (Optional[AssistantText]): 文本内容的实例，默认为None。
    """
    type: str = "text"
    text: Optional[AssistantText] = None
