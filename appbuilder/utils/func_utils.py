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
import inspect

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

def function_to_json(func) -> dict:
    """
    将Python函数转换为可序列化为JSON的字典格式，包含函数的名称、描述和参数签名。

    参数:
        func: 需要转换的函数。

    返回:
        表示函数签名的字典格式。

    抛出:
        ValueError: 如果函数没有文档字符串。
    """
    # 检查文档字符串
    if not func.__doc__:
        raise ValueError(f"Function '{func.__name__}' is missing a docstring description.")

    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    signature = inspect.signature(func)

    parameters = {}
    for param in signature.parameters.values():
        param_type = type_map.get(param.annotation, "string")
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }

def convert_and_call(func, str_args: dict):
    """
    根据函数的签名，将字符串类型的参数转换为目标类型，并调用该函数。

    参数:
        func (Callable): 目标函数。
        str_args (dict): 字符串形式的参数字典。

    返回:
        Any: 函数调用的返回值。

    抛出:
        ValueError: 如果参数不能转换为目标类型。
    """
    # 获取函数的签名
    signature = inspect.signature(func)
    
    # 将字符串参数转换为对应类型
    converted_args = {}
    for name, param in signature.parameters.items():
        if name in str_args:
            # 获取目标类型
            param_type = param.annotation
            
            # 尝试转换参数
            try:
                if param_type is int:
                    converted_args[name] = int(str_args[name])
                elif param_type is float:
                    converted_args[name] = float(str_args[name])
                elif param_type is bool:
                    converted_args[name] = str_args[name].lower() in ['true', '1', 't', 'yes']
                elif param_type is list:
                    converted_args[name] = eval(str_args[name])  # 将字符串解析为列表
                elif param_type is dict:
                    converted_args[name] = eval(str_args[name])  # 将字符串解析为字典
                else:
                    converted_args[name] = str_args[name]  # 保持字符串形式
            except (ValueError, SyntaxError, TypeError) as e:
                raise ValueError(f"无法将参数 '{name}' 转换为类型 {param_type}: {e}")
        else:
            # 如果参数在str_args中不存在，使用默认值
            converted_args[name] = param.default
    
    # 调用函数并返回结果
    return func(**converted_args)
    
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]