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
from pydantic import BaseModel
from typing import Dict, List, Literal, Any

class PropertyModel(BaseModel):
    """参数属性模型，用于描述函数参数的类型和元数据。

    Attributes:
        type (Any): 参数的类型。
    """
    type: Any


class ParametersModel(BaseModel):
    """函数参数模型，用于定义函数的参数结构。

    Attributes:
        type (Literal["object"]): 表示参数集合的类型，固定为 "object"。
        properties (Dict[str, PropertyModel]): 参数的具体属性映射，其中键是参数名，值是对应的属性模型。
        required (List[str]): 必须提供的参数列表。
    """
    type: Literal["object"]
    properties: Dict[str, PropertyModel]
    required: List[str]


class Manifest(BaseModel):
    """函数模型，用于描述函数的元信息。

    Attributes:
        type (Literal["function"]): 表示模型的类型，固定为 "function"。
        function (Dict[str, Any]): 函数的详细信息，包括名称、描述、参数、返回值等。
    """
    type: Literal["function"]
    function: Dict[str, Any]

