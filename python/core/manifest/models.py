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
from enum import Enum
from pydantic import BaseModel as PydanticBaseModel # noqa: F403 # type: ignore
from typing import Dict, List, Literal, Any, Optional

from dataclasses_json import config
from dataclasses import dataclass
from dataclasses import field as Field
from dataclasses_json import DataClassJsonMixin

from appbuilder.core.manifest.validate import validate_function_param_name, validate_function_name

class BaseModel(DataClassJsonMixin):
    """Base model for all models."""

    pass

class PropertyModel(PydanticBaseModel):
    """参数属性模型，用于描述函数参数的类型和元数据。

    Attributes:
        type (Any): 参数的类型。
    """
    type: Any
    description: Optional[str]


class ParametersModel(PydanticBaseModel):
    """函数参数模型，用于定义函数的参数结构。

    Attributes:
        type (Literal["object"]): 表示参数集合的类型，固定为 "object"。
        properties (Dict[str, PropertyModel]): 参数的具体属性映射，其中键是参数名，值是对应的属性模型。
        required (List[str]): 必须提供的参数列表。
    """
    type: Literal["object"]
    properties: Dict[str, PropertyModel]
    required: List[str]


class Manifest(PydanticBaseModel):
    """函数模型，用于描述函数的元信息。

    Attributes:
        type (Literal["function"]): 表示模型的类型，固定为 "function"。
        function (Dict[str, Any]): 函数的详细信息，包括名称、描述、参数、返回值等。
    """
    type: Literal["function"]
    function: Dict[str, Any]

class ParameterViewKind(str, Enum):
    """
    The kind of a parameter.


    Args:
        ARGUMENT: The parameter is a function argument.
        RETURN: The parameter is a function return.
        PATH: The parameter is a OpenAPI path parameter.
        QUERY: The parameter is a OpenAPI query parameter.
        HEADER: The parameter is a OpenAPI header parameter.
        COOKIE: The parameter is a OpenAPI cookie parameter.
    """

    ARGUMENT = "argument"
    RETURN = "return"
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"
    BODY = "body"

@dataclass
class ParameterView(BaseModel):
    """
    View of a function parameter.

    Args:
        name (str): The name of the parameter.
        description (str): The description of the parameter.
        default_value (str): The default value of the parameter.
        type_ (str): The type of the parameter.
        type_object (Any): The type object of the parameter.
        type_schema (Dict): The json schema of the parameter.
        required (bool): Whether the parameter is required.
        example (str): The example of the parameter.
        kind (str): The kind of the parameter. For python function it is argument or return.
          For OpenAPI it is location like query, path, header, cookie, body.
    """

    name: str
    description: str = None
    default_value: str = None
    type_: str = None
    type_object: Optional[Any] = Field(default=None, metadata = config(exclude=lambda value: True))
    type_schema: Dict = Field(default=None)
    required: bool = True
    example: str = None
    kind: str = None

    def __init__(
        self,
        name: str,
        description: str,
        default_value: str = None,
        type_: str = "str",
        type_object: Any = None,
        type_schema: Dict[str, Any] = None,
        required: bool = True,
        example: str = None,
        kind: str = ParameterViewKind.ARGUMENT,
    ):
        """Initialize a ParameterView."""
        validate_function_param_name(name)
        self.name = name
        self.description = description
        self.default_value = default_value
        self.type_ = type_
        self.type_object = type_object
        self.type_schema = type_schema
        self.required = required
        self.example = example
        self.kind = kind
        super().__init__()

    def as_semantic_kernel_parameter(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "default_value": self.default_value,
            "type": self.type_,
            "required": self.required,
        }

    @classmethod
    def merge(cls, a: "ParameterView", b: "ParameterView") -> "ParameterView":
        """Merge two parameter views."""
        return cls(
            name=a.name,
            description=(b.description or a.description),
            default_value=(b.default_value or a.default_value),
            type_=(b.type_ or a.type_),
            required=(b.required if b.required is not None else a.required),
            example=(b.example or a.example),
            kind=(b.kind or a.kind),
        )

@dataclass
class ManifestView(BaseModel):
    """View of a function."""

    name: str
    description: str
    parameters: List[ParameterView] = Field(default_factory=list)
    returns: Optional[List[ParameterView]] = Field(default_factory=list)
    is_async: bool = False
    is_stream: bool = False
    return_direct: bool = False

    _name_to_params: Dict[str, ParameterView] = Field(default_factory=dict)

    def __init__(
        self,
        name: str,
        description: str,
        parameters: List[ParameterView],
        returns: Optional[List[ParameterView]] = None,
        is_async: bool = False,
        is_stream: bool = False,
        return_direct: bool = False,
    ) -> None:
        """Initialize a ManifestView."""
        validate_function_name(name)
        self.name = name
        self.description = description
        self.parameters = parameters
        self.returns = returns
        self.is_async = is_async
        self.is_stream = is_stream
        self.return_direct = return_direct

        _name_to_params = {}
        for item in parameters:
            _name_to_params[item.name] = item
        self._name_to_params = _name_to_params

        super().__init__()

