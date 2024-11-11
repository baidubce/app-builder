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
    
class DocstringsFormat(Enum):
    """Python docstring format."""

    AUTO = "auto"
    GOOGLE = "google"
    # https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
    SPHINX = "sphinx"
    NUMPY = "numpy"

def _get_function_docs(func: callable) -> Tuple:
    if not func.__doc__:
        return None

    return _parse_function_doc(func.__doc__)

def _parse_function_doc(docstring: str) -> Tuple:
    fist_line, rest = docstring.split("\n", 1) if "\n" in docstring else (docstring, "")
    # we dedent the first line separately,because its common that it often starts right after """
    fist_line = fist_line.strip()
    if fist_line:
        fist_line += "\n"
    docs = fist_line + dedent(rest)
    return docs

def _find_and_parse_params_from_docstrings(docstring: str, format: DocstringsFormat) -> str:
    """
    Find Args section in docstring.
    """

    if format == DocstringsFormat.AUTO or format == DocstringsFormat.GOOGLE:
        # auto here means more more free format than google
        args_section_start_regex_pattern = r"(^|\n)(Args|Arguments|Parameters)\s*:?\s*\n"
        args_section_end_regex_pattern = r"(^|\n)([A-Z][a-z]+)\s*:?\s*\n"
        returns_section_start_pattern = r"(^|\n)(Returns|Ret)\s*:?\s*\n"
        return_param_start_parser_regex = r"(^|\n)\s+(?P<type>[^\)]*)\s*:\s*(?=[^\n]+)"
        if format == DocstringsFormat.GOOGLE:
            param_start_parser_regex = (
                r"(^|\n)\s+(?P<name>[\*]{0,2}[a-zA-Z_][a-zA-Z0-9_]*)\s*(\((?P<type>[^\)]*)\))?\s*:\s*(?=[^\n]+)"
            )
        else:
            param_start_parser_regex = (
                r"(^|\n)\s+(?P<name>[\*]{0,2}[a-zA-Z_][a-zA-Z0-9_]*)\s*(\((?P<type>[^\)]*)\))?\s*(-|:)\s*(?=[^\n]+)"
            )
    elif format == DocstringsFormat.NUMPY:
        args_section_start_regex_pattern = r"(^|\n)(Args|Arguments|Parameters)\s*\n\s*---+\s*\n"
        args_section_end_regex_pattern = r"(^|\n)([A-Z][a-z]+)\s*\n\s*---+\s*\n"
        param_start_parser_regex = (
            r"(^|\n)\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)(\s*:\s*(?P<type>[^\)]*)\s*)?\n\s+(?=[^\n]+)"
        )
    elif format == DocstringsFormat.SPHINX:
        args_section_start_regex_pattern = None  # we will look for :param everywhere
        args_section_end_regex_pattern = r"(\n)\s*:[a-z]"
        param_start_parser_regex = (
            r"(^|\n)\s*:param\s+(?P<type>[^\)]*)\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?=[^\n]+)"
        )

    params = _parse_params(
        docstring,
        args_section_start_regex_pattern,
        args_section_end_regex_pattern,
        param_start_parser_regex,
        has_name=True,
    )

    returns_param_name = "default"
    returns = _parse_params(
        docstring,
        returns_section_start_pattern,
        args_section_end_regex_pattern,
        return_param_start_parser_regex,
        has_name=False,
        param_name=returns_param_name,
    )

    if not params and format == DocstringsFormat.AUTO:
        # try other options
        options = [DocstringsFormat.NUMPY, DocstringsFormat.SPHINX]
        for option in options:
            params, returns = _find_and_parse_params_from_docstrings(docstring, option)
            if params:
                return params, returns[returns_param_name] if returns_param_name in returns else {}
    else:
        return params, returns[returns_param_name] if returns_param_name in returns else {}


def _parse_params(
    docstring,
    args_section_start_regex_pattern,
    args_section_end_regex_pattern,
    param_start_parser_regex,
    has_name=True,
    param_name="default",
):
    optional_pattern = r",\s+optional\s*"
    args_section = None
    args_section_start = 0
    args_section_end = None

    if args_section_start_regex_pattern:
        match = re.search(args_section_start_regex_pattern, docstring)
        if match:
            args_section_start = match.end()
            if args_section_end_regex_pattern:
                match = re.search(args_section_end_regex_pattern, docstring[args_section_start:])
                if match:
                    args_section_end = match.start() + args_section_start
            if not args_section_end:
                args_section_end = len(docstring)
            args_section = docstring[args_section_start:args_section_end]
        else:
            args_section = None
    else:
        args_section = docstring

    params = {}
    if args_section:
        last_param = None
        last_param_end = None
        for param_start_match in re.finditer(param_start_parser_regex, args_section):
            if last_param_end is not None:
                last_param["description"] = args_section[last_param_end : param_start_match.start()].strip()

            param_name = param_start_match.group("name") if has_name else param_name
            param_name = param_name.lstrip("*")

            param_type = param_start_match.group("type")
            param_required = True
            if param_type and re.search(optional_pattern, param_type):
                param_required = False
                param_type = re.sub(optional_pattern, "", param_type).strip()
            last_param = {"type": param_type or "", "description": None, "required": param_required}
            last_param_end = param_start_match.end()
            params[param_name] = last_param

        if last_param_end is not None:
            section_end = None
            if args_section_start_regex_pattern is None and args_section_end_regex_pattern:
                # this is handling SPHINX, we didnt parse the start so we cant parse the end until all the params are consumed... now we can parse the end after the last param
                section_end_match = re.search(args_section_end_regex_pattern, docstring[last_param_end:])
                if section_end_match:
                    section_end = last_param_end + section_end_match.start()
            if not section_end:
                section_end = len(docstring)
            last_param["description"] = args_section[last_param_end:section_end].strip()
    return params

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

def function_to_json(func) -> FunctionModel:
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
    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(f"无法获取函数 {func.__name__} 的签名: {str(e)}")

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
            "parameters": parameters_model.dict(),
        }
    )

    return function_model

if __name__ == "__main__":
    # 使用示例函数
    def get_current_weather(location: str, unit: str) -> str:
        """
        查询指定中国城市的当前天气。

        Args:
            location (str): 城市名称，例如："北京"
            unit (int): 温度单位，可选 "celsius" 或 "fahrenheit"

        Returns:
            Dict[str, str]: Returns a dict.
        """
        return "北京今天25度"

    # 获取结果并转换为字典
    model = function_to_json(get_current_weather)
    result = model.dict()

    print(result)
