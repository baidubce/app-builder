# -*- coding: UTF-8 -*-
"""Parse function parameters from signature."""

import inspect
from inspect import Parameter, Signature
from typing import Any, Dict

NoneType = type(None)


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
    if param != Parameter.empty:
        ret = _parse_annotation(param.annotation)
    ret["name"] = param.name
    if param.default != Parameter.empty:
        ret["default_value"] = param.default
        ret["required"] = False
    return ret


def _parse_annotation(annotation: Parameter) -> Dict[str, Any]:
    # The keys of this dict is compatible with semantic-kernel, do not change them
    if annotation == Signature.empty:
        return {"type_": "Any", "required": True}
    if isinstance(annotation, str):
        return {"type_": annotation, "required": True}
    ret = _parse_internal_annotation(annotation, True)
    if hasattr(annotation, "__metadata__") and annotation.__metadata__:
        ret["description"] = annotation.__metadata__[0]
    return ret


def _parse_internal_annotation(annotation: Parameter, required: bool) -> Dict[str, Any]:
    if hasattr(annotation, "__forward_arg__"):
        return {"type_": annotation.__forward_arg__, "required": required}

    parent_type = getattr(annotation, "__name__", None)
    if getattr(annotation, "__name__", None) == "Optional":
        required = False
    if hasattr(annotation, "__args__"):
        results = [_parse_internal_annotation(arg, required) for arg in annotation.__args__]
        type_objects = [
            result["type_object"]
            for result in results
            if "type_object" in result and result["type_object"] is not NoneType
        ]
        str_results = [result["type_"] for result in results]
        if "NoneType" in str_results:
            str_results.remove("NoneType")
            required = False
        else:
            if parent_type == "Union":
                #  all optionals are optional
                # half optionals are required
                #  all  required are required
                required = not (all(not result["required"] for result in results))

        ret = {"type_": parent_type + "[" + ", ".join(str_results) + "]", "required": required}
        if type_objects and len(type_objects) == 1:
            ret["type_object"] = type_objects[0]
        return ret
    return {
        "type_": getattr(annotation, "__name__", ""),
        "type_object": annotation,
        "required": required,
    }
