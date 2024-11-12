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

import re
import inspect
import warnings
from enum import Enum
from functools import wraps
from textwrap import dedent
from pydantic import BaseModel, ValidationError
from typing import Dict, List, Literal, Any, Optional, Tuple

from appbuilder.utils.tool_definition_docstring import (
    DocstringsFormat,
    _parse_function_description_from_docstrings,
    get_docstring_view,
)

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
    type: str
    description: Optional[str] = None

class ParametersModel(BaseModel):
    type: Literal["object"]
    properties: Dict[str, PropertyModel]
    required: List[str]

class FunctionModel(BaseModel):
    type: Literal["function"]
    function: Dict[str, Any]

def function_to_model(func) -> FunctionModel:
    """
    将Python函数转换为Pydantic的BaseModel实例，描述函数的签名，包括名称、描述和参数。
    通过解析注释来提取类型和描述信息。
    
    Args:
        func: 要转换的函数。
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    # 获取函数签名
    signature = inspect.signature(func)

    if func.__doc__ is None:
        raise ValueError(f"函数 {func.__name__} 缺少文档字符串")

    # 解析注释中的参数和返回值信息
    doc = _get_function_docs(func)
    doc_params, _ = _find_and_parse_params_from_docstrings(docstring=doc, format=DocstringsFormat.GOOGLE)

    # 解析参数信息
    properties = {}
    required = []
    for param in signature.parameters.values():
        # 提取参数类型，默认使用 "string" 作为基础类型
        param_type = type_map.get(param.annotation)

        # 先从 doc_params 获取类型，如果没有定义则使用 param_type
        doc_param_info = doc_params.get(param.name, {})
        doc_type = doc_param_info.get("type", None)

        # 设置参数信息，优先使用 docstring 类型，其次使用函数签名中的类型
        param_info = {
            "type": param_type if param_type is not None else doc_type,   # 优先使用函数签名中类型 param_type
            "description": doc_param_info.get("description", None),       # 从docstring中提取参数描述
        }
        # 验证类型字段是否有有效值
        if not param_info["type"]:
            raise ValueError(f"参数 '{param.name}' 缺少类型信息，请在函数签名或注释中指定类型。")

        # 添加到属性字典中
        properties[param.name] = PropertyModel(**param_info)

        # 将无默认值的参数作为必传参数
        if param.default == inspect._empty:
            required.append(param.name)

    # 生成参数模型
    parameters_model = ParametersModel(
        type="object",
        properties=properties,
        required=required
    )

    # 生成 FunctionModel 实例
    function_model = FunctionModel(
        type="function",
        function={
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": parameters_model.model_dump(),
        }
    )

    return function_model