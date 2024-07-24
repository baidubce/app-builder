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

    type: str = "object"
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
    responses: Union[AssistantFunctionJsonSchema, None] = None
    examples: Union[list[list[AssistantExample]], None] = None


class AssistantTool(BaseModel):
    """
    表示助理工具的模型。

    Attributes:
        type (str): 工具的类型，默认为 'function'。
        function (AssistantFunction): 功能的实例。
    """

    type: str = "function"
    function: AssistantFunction = None


class ResponseFormat(str, Enum):
    """
    表示响应格式的枚举类型。

    Values:
        TEXT: 文本格式。
        JSON_OBJECT: JSON对象格式。
    """

    TEXT = "text"
    JSON_OBJECT = "json_object"


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


class AssistantChatParameters(BaseModel):
    """
    表示助理聊天参数的模型。
    Attributes:
        temperature (Optional[float]): 	采样温度，较高的数值会使输出更随机。取值范围严格大于0，小于等于1，默认为0.8。
        top_p (Optional[float]): top_p，核采样方法的概率阈值，影响输出文本的多样性，较高的数值会使输出的文本更加多样性。取值范围大于等于0，小于等于1，默认为0.8。
        penalty_score (Optional[float]): 惩罚分数，减少重复生成的现象，值越大表示惩罚越大。取值范围大于等于1，小于等于2，默认为1.0。
    """

    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.8
    penalty_score: Optional[float] = 1.0


class AssistantThoughtParameters(BaseModel):
    """
    表示助理思考参数的模型。
    Attributes:
        temperature (Optional[float]): 	采样温度，较高的数值会使输出更随机。取值范围严格大于0，小于等于1，默认为0.01。
        top_p (Optional[float]): top_p，核采样方法的概率阈值，影响输出文本的多样性，较高的数值会使输出的文本更加多样性。取值范围大于等于0，小于等于1，默认为0。
        penalty_score (Optional[float]): 惩罚分数，减少重复生成的现象，值越大表示惩罚越大取值范围大于等于1，小于等于2，默认为1.0。
    """

    temperature: Optional[float] = 0.01
    top_p: Optional[float] = 0
    penalty_score: Optional[float] = 1.0


class AssistantModelParameters(BaseModel):
    """
    表示助理模型的参数的模型。
    Attributes:
        chat_parameters (Optional[AssistantChatParameters]): 聊天参数的实例，默认为None。
        thought_parameters (Optional[AssistantThoughtParameters]): 思考参数的实例，默认为None。
    """

    chat_parameters: Optional[AssistantChatParameters] = AssistantChatParameters()
    thought_parameters: Optional[AssistantThoughtParameters] = (
        AssistantThoughtParameters()
    )


class AssistantUserInfo(BaseModel):
    """
    表示用户信息。
    Attributes:
        id (Optional[str]): 用户ID，默认为None。
        name (Optional[str]): 用户名称，默认为None。
        nickname (Optional[str]): 用户昵称，默认为None。
        watermark (Optional[str]): 用户水印，默认为None。
        intro (Optional[str]): 用户简介，默认为None。
        baidu_id (Optional[str]): 用户百度ID，默认为None。
    """

    id: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    watermark: Optional[str] = None
    intro: Optional[str] = None
    baidu_id: Optional[str] = None


class AssistantUserLoc(BaseModel):
    """
    表示用户位置信息。
    Attributes:
        loc (Optional[str]): 用户当前的地理位置信息，使用json格式描述
        uip (Optional[str]): 用户的ipv4地址
        uipv6 (Optional[str]): 用户的ipv6地址
    """

    loc: Optional[str] = None
    uip: Optional[str] = None
    uipv6: Optional[str] = None
