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

import warnings
from functools import wraps
from pydantic import BaseModel
from typing import Dict, List, Literal, Any

from appbuilder.utils.tool_definition_signature import get_signature_view

def deprecated(reason=None, version=None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    def decorator(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            messages = "Call deprecated API {}().".format(func.__qualname__)
            if reason is not None:
                messages += " Deprecated because {}.".format(reason)
            
            if version is not None:
                messages += " This API will be removed after version {}.".format(version)
            
            messages += "\nDetailed information: "

            warnings.warn(messages,
                        category=DeprecationWarning,
                        stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        return new_func
    return decorator

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PropertyModel(BaseModel):
    type: Any

class ParametersModel(BaseModel):
    type: Literal["object"]
    properties: Dict[str, PropertyModel]
    required: List[str]

class FunctionModel(BaseModel):
    type: Literal["function"]
    function: Dict[str, Any]

def function_to_manifest(func) -> FunctionModel:
    """
    利用 tool_definition_signature.py 提供的 get_signature_view 方法解析函数的签名和参数信息，
    并生成一个 FunctionModel 实例。

    Args:
        func: 要转换的函数。

    Returns:
        FunctionModel: 包含函数元信息的模型。
    """
    if func.__doc__ is None:
        raise ValueError(f"函数 {func.__name__} 缺少文档字符串")

    # 使用 tool_definition_signature 提取函数签名信息
    sig_params, sig_returns = get_signature_view(func)

    # 构造参数模型
    properties = {}
    required = []

    for param in sig_params:
        param_info = {
            "type": param.get("type_", None),  # 类型
            "description": param.get("description", None),  # 描述
        }

        # 验证类型字段是否有有效值
        if not param_info["type"]:
            raise ValueError(f"参数 '{param['name']}' 缺少类型信息，请在函数签名中指定类型。")

        # 构造 PropertyModel
        properties[param["name"]] = PropertyModel(**param_info)

        # 记录必需参数
        if param.get("required", False):
            required.append(param["name"])

    # 构造返回值描述
    return_info = {
        "type": sig_returns.get("type_", None),
        "description": sig_returns.get("description", None),
    }

    # 构造 ParametersModel
    parameters_model = ParametersModel(
        type="object",
        properties=properties,
        required=required,
    )

    # 构造 FunctionModel
    function_manifest = FunctionModel(
        type="function",
        function={
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": parameters_model.model_dump(),
            "returns": return_info,
        },
    )

    return function_manifest

def decorator_to_manifest(function_view) -> FunctionModel:
    # 提取参数信息
    parameters = {}
    required_fields = []

    for param in function_view.parameters:
        # 验证类型字段是否有有效值
        if not param.type_:
            raise ValueError(f"参数 '{param.name}' 缺少类型信息，请在函数签名中指定类型。")

        # 定义每个参数的属性模型
        parameters[param.name] = PropertyModel(
            type=param.type_,
            description=param.description
        )
        # 检查参数是否是必填项
        if param.required:
            required_fields.append(param.name)

    # 创建 ParametersModel
    parameters_model = ParametersModel(
        type="object",
        properties=parameters,
        required=required_fields
    )
    if not function_view.description:
        raise ValueError(f"函数 {function_view.name} 缺少描述")
    
    # 构建 FunctionModel
    function_manifest = FunctionModel(
        type="function",
        function={
            "name": function_view.name,
            "description": function_view.description,
            "parameters": parameters_model.dict(),  # 转换为字典格式
            "returns": {
                "type": function_view.returns[0].type_,
                "description": function_view.returns[0].description
            }
        }
    )

    return function_manifest