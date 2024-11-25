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
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Any, Optional

from appbuilder.core.manifest.manifest_signature import get_signature


class PropertyModel(BaseModel):
    """参数属性模型，用于描述函数参数的类型和元数据。

    Attributes:
        type (Optional[str]): 参数的类型。
        description (Optional[str]): 参数的描述信息。
    """

    name: str
    type: Optional[str]
    description: Optional[str]
    required: bool = True

    @classmethod
    def merge(cls, a: "PropertyModel", b: "PropertyModel") -> "PropertyModel":
        """Merge two parameter views."""
        return cls(
            name=a.name,
            description=(b.description or a.description),
            type=(b.type or a.type),
            required=(b.required if b.required is not None else a.required),
        )


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

    @classmethod
    def from_function(cls, func) -> "Manifest":
        """
        利用 manifest_signature.py 提供的 get_signature 方法解析函数的签名和参数信息，
        并生成一个 Manifest 实例。

        Args:
            func: 要转换的函数。

        Returns:
            Manifest: 包含函数元信息的模型。
        """
        # 使用 manifest_signature 提取函数签名信息
        sig_params, sig_returns = get_signature(func)

        # 构造参数模型
        properties = {}
        required = []

        if hasattr(func, "__ab_manifest__"):
            return func.__ab_manifest__

        for param in sig_params:
            param_info = {
                "name": param["name"],  # 参数名称
                "type": param.get("type_", None),  # 类型
                "description": param.get("description", None),  # 描述
                "required": param.get("required", False),  # 是否必需
            }

            # 验证类型字段是否有有效值
            if not param_info["type"]:
                param_info["type"] = "Any"

            # 构造 PropertyModel
            properties[param["name"]] = PropertyModel(
                name=param_info["name"],
                type=param_info["type"],
                description=param_info["description"],
                required=param_info["required"],
            )

            # 记录必需参数
            if param_info["required"]:
                required.append(param["name"])

        # 构造 ParametersModel
        parameters_model = ParametersModel(
            type="object",
            properties=properties,
            required=required,
        )

        # 构造 Manifest 对象
        manifest = cls(
            type="function",
            function={
                "name": func.__name__,
                "description": func.__doc__,  # 去掉多余的空格
                "parameters": parameters_model.model_dump(),
            },
        )

        return manifest
