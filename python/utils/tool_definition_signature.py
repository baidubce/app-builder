# -*- coding: UTF-8 -*-
"""Parse function parameters from signature."""

import inspect
from inspect import Parameter, Signature
from typing import Any, Dict, Union, Optional, List, get_origin, get_args
import logging

NoneType = type(None)

# 映射内置泛型类型到 typing 模块的名称
TYPE_MAPPING = {
    dict: "Dict",
    list: "List",
    set: "Set",
    tuple: "Tuple",
    Union: "Union",
    Optional: "Optional",
    Any: "Any",
    int: "int",
    str: "str",
    float: "float",
    bool: "bool",
    # 根据需要添加更多映射
}


def get_signature_view(func):
    """Get signature view of a function."""

    signature = inspect.signature(func)
    _parameters = [_parse_parameter(param) for param in signature.parameters.values() if param.name != "self"]
    signature_returns = (
        _parse_annotation(signature.return_annotation) if signature.return_annotation != Signature.empty else {}
    )
    return _parameters, signature_returns


def _parse_parameter(param: Parameter) -> Dict[str, Any]:
    ret = {}
    if param.annotation != Parameter.empty:
        ret = _parse_annotation(param.annotation)
    else:
        ret["type_"] = "Any"
        ret["required"] = True  # 默认为 True

    ret["name"] = param.name

    if param.default != Parameter.empty:
        ret["default_value"] = param.default
        ret["required"] = False
    else:
        ret["required"] = ret.get("required", True)

    return ret


def _parse_annotation(annotation: Any) -> Dict[str, Any]:
    # The keys of this dict are compatible with semantic-kernel, do not change them
    if annotation == Signature.empty:
        return {"type_": "Any", "required": True}
    if isinstance(annotation, str):
        return {"type_": annotation, "required": True}
    ret = _parse_internal_annotation(annotation, True)
    if hasattr(annotation, "__metadata__") and annotation.__metadata__:
        ret["description"] = annotation.__metadata__[0]
    return ret


def _parse_internal_annotation(annotation: Any, required: bool) -> Dict[str, Any]:
    if hasattr(annotation, "__forward_arg__"):
        return {"type_": annotation.__forward_arg__, "required": required}

    # 获取 origin 和 args
    origin = get_origin(annotation)
    args = get_args(annotation)

    # 确定 parent_type
    if origin is not None:
        parent_type = TYPE_MAPPING.get(origin, origin.__name__ if hasattr(origin, '__name__') else str(origin))
    else:
        parent_type = TYPE_MAPPING.get(annotation, annotation.__name__ if hasattr(annotation, '__name__') else str(annotation))

    if parent_type == "Optional":
        required = False

    if args:
        results = [_parse_internal_annotation(arg, required) for arg in args]
        type_objects = [
            result["type_object"]
            for result in results
            if "type_object" in result and result["type_object"] is not NoneType
        ]
        str_results = [result["type_"] for result in results]

        if "NoneType" in str_results:
            str_results.remove("NoneType")
            required = False

            if parent_type == "Union":
                if len(str_results) == 1:
                    type_ = f"Optional[{str_results[0]}]"
                else:
                    type_ = f"Union[{', '.join(str_results)}]"
            else:
                type_ = f"{parent_type}[{', '.join(str_results)}]"
        else:
            if parent_type == "Union":
                # 所有选项都为非必需
                required = not (all(not result["required"] for result in results))
            type_ = f"{parent_type}[{', '.join(str_results)}]"

        ret = {"type_": type_, "required": required}
        if type_objects and len(type_objects) == 1:
            ret["type_object"] = type_objects[0]
        logging.debug(f"Parsed annotation: {annotation}, type_: {type_}, required: {required}")
        return ret

    type_ = TYPE_MAPPING.get(annotation, annotation.__name__ if hasattr(annotation, "__name__") else str(annotation))
    logging.debug(f"Parsed annotation: {annotation}, type_: {type_}, required: {required}")
    return {
        "type_": type_,
        "type_object": annotation,
        "required": required,
    }