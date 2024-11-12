# -*- coding: UTF-8 -*-
"""FunctionView classes."""

import inspect
import re
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    from pydantic.v1 import BaseModel as PydanticBaseModel # noqa: F403 # type: ignore
except ImportError:
    from pydantic import BaseModel as PydanticBaseModel

try:
    from pydantic.v1 import create_model
except ImportError:
    from pydantic import create_model 

from dataclasses_json import config
from dataclasses import dataclass
from dataclasses import field as Field
from dataclasses_json import DataClassJsonMixin

from appbuilder.utils.tool_definition_docstring import (
    DocstringsFormat,
    _parse_function_description_from_docstrings,
    get_docstring_view,
)
from appbuilder.utils.tool_definition_signature import get_signature_view

class BaseModel(DataClassJsonMixin):
    """Base model for all promptflow models."""

    pass

FUNCTION_NAME_REGEX = r"^[0-9A-Za-z_\u4e00-\u9fff]*$"
FUNCTION_PARAM_NAME_REGEX = r"^[0-9A-Za-z_\u4e00-\u9fff]*$"
FUNCTION_FLAG = "__pf_function__"


def validate_function_name(value: Optional[str]) -> None:
    """
    Validates that the function name is valid.

    Valid function names are non-empty and
    match the regex: [0-9A-Za-z_]*

    :param value: The function name to validate.

    :raises ValueError: If the function name is invalid.
    """
    if not value:
        raise ValueError("The function name cannot be `None` or empty")

    if not re.match(FUNCTION_NAME_REGEX, value):
        raise ValueError(
            f"Invalid function name: {value}. Function "
            f"names may only contain ASCII letters, "
            f"digits, and underscores."
        )


def validate_function_param_name(value: Optional[str]) -> None:
    """
    Validates that the function parameter name is valid.

    Valid function parameter names are non-empty and
    match the regex: [0-9A-Za-z_]*

    :param value: The function parameter name to validate.

    :raises ValueError: If the function parameter name is invalid.
    """
    if not value:
        raise ValueError("The function parameter name cannot be `None` or empty")

    if not re.match(FUNCTION_PARAM_NAME_REGEX, value):
        raise ValueError(
            f"Invalid function parameter name: {value}. Function parameter "
            f"names may only contain ASCII letters, digits, and underscores."
        )


# The following two functions are here to allow dynamically updating function description.
# Check tool/builtin/openapi_plugin.py for example.
def function_description(cls, func):
    """Get the description of a function."""

    if hasattr(func, "__pf_function__"):
        view = func.__pf_function__
        return view.description if view else ""


def update_function_description(func, description):
    """Update function description."""
    func.__dict__["__kernel_function_description__"] = description or ""
    func.__dict__["__pf_func_description__"] = description or ""


def get_function_schema_with_inspect(method):
    (
        args,
        _,
        varkw,
        defaults,
        kwonlyargs,
        kwonlydefaults,
        annotations,
    ) = inspect.getfullargspec(method)
    if len(args) > 0 and (args[0] == "self" or args[0] == "cls"):
        args = args[1:]  # remove self or cls

    if args or varkw:
        if defaults is None:
            defaults = ()
        non_default_args_count = len(args) - len(defaults)
        defaults = (...,) * non_default_args_count + defaults

        keyword_only_params = {param: kwonlydefaults.get(param, Any) for param in kwonlyargs}
        params = {param: (annotations.get(param, Any), default) for param, default in zip(args, defaults)}
        return create_model(
            "func",
            **params,
            **keyword_only_params,
            __base__=PydanticBaseModel,
            __config__=None,
            __doc__=""
        ).schema()["properties"]
    else:  # method has no arguments
        return None

def _exclude(value):
    return True


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
    type_object: Optional[Any] = Field(default=None, metadata=config(exclude=_exclude))
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
class FunctionView(BaseModel):
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
        """Initialize a FunctionView."""
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


def function(
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
    is_async: Optional[bool] = None,
    is_stream: Optional[bool] = None,
    disable_docstring: Optional[bool] = False,
    docstring_format: Optional[DocstringsFormat] = DocstringsFormat.GOOGLE,
    return_direct: Optional[bool] = False,
):
    """
    Decorator for functions.  Use some information to extract meta about function.
    Priority as follows:
    1. User provided value via arguments
    2. Function signature + annotations
    3. Docstring

    Args:
        description (str, optional): The functionality of the function, general user guildline.
        name (str, optional): The name of the function.
        is_async (bool, optional): Whether the function is asynchronous.
        is_stream (bool, optional): Whether the function is returning Iterator/AsyncIterator.
        disable_docstring (bool, optional): True to disable FunctionView extract meta from docstring.
        docstring_format (DocstringsFormat, optional): The format of the docstring,
        return_direct (bool, optional): Compatible with LangChain BaseTool.return_direct.
    """

    def decorator(func):
        """Decorator for function."""

        # Get meta from signature
        sig_params, sig_returns = get_signature_view(func=func)

        # Get meta from docstring
        doc_params, doc_returns = get_docstring_view(
            func=func, format=docstring_format, disable_docstring=disable_docstring
        )

        # Get meta from decorator
        dec_params = func.__pf_function_parameters__ if hasattr(func, "__pf_function_parameters__") else {}
        dec_params = {item.name: item for item in dec_params}
        dec_returns = func.__pf_function_returns__[0] if hasattr(func, "__pf_function_returns__") else {}

        # get schema from inspect
        schema = get_function_schema_with_inspect(method=func) or {}
        final_parameters = []
        for p in sig_params:
            k = p["name"]
            a = doc_params[k] if k in doc_params else {}
            # Annotated parameters overwrites the docstring parameters if key is the same.
            b = {**a, **p}
            # Decorator parameters overwrites the annotated parameters if there is any value, minimize decorator to write.
            c = dec_params[k] if k in dec_params else {}
            b["type_schema"] = schema.get(k, {})
            result = _merge_dict_parameter_view(b, c)
            final_parameters.append(result)

        final_return = {**doc_returns, **sig_returns}
        final_return = _merge_dict_parameter_view(final_return, dec_returns)

        # Use provided value if not None, otherwise use reflection.
        final_name = name or func.__name__
        final_desc = description or _parse_function_description_from_docstrings(func.__doc__)

        # inspect.iscoroutinefunction(func) is not enough to check if it's async generator.
        # https://github.com/python/cpython/issues/81371
        final_async = is_async or (inspect.iscoroutinefunction(func) or inspect.isasyncgenfunction(func))
        final_stream = is_stream or (inspect.isgeneratorfunction(func) or inspect.isasyncgenfunction(func))

        view = FunctionView(
            name=final_name,
            description=final_desc,
            parameters=[
                ParameterView(
                    name=p.get("name", ""),
                    description=p.get("description", None),
                    default_value=p.get("default_value", None),
                    type_=p.get("type_", None),
                    required=p.get("required", True),
                    example=p.get("example", None),
                    type_schema=p.get("type_schema", None),
                )
                for p in final_parameters
            ],
            returns=[
                ParameterView(
                    name="return",
                    description=final_return.get("description", None),
                    default_value=final_return.get("default_value", None),
                    type_=final_return.get("type_", None),
                    required=final_return.get("required", True),
                    example=final_return.get("example", None),
                )
            ],
            is_async=final_async,
            is_stream=final_stream,
            return_direct=return_direct,
        )

        # Attach view to function.
        func.__pf_function__ = view

        # Compatible to semantic kernel 0.9
        func.__kernel_function__ = True
        func.__kernel_function_description__ = final_desc
        func.__kernel_function_name__ = final_name
        func.__kernel_function_streaming__ = final_stream
        func.__kernel_function_parameters__ = final_parameters
        func.__kernel_function_return_type__ = final_return.get("type", "None")
        func.__kernel_function_return_description__ = final_return.get("description", "")
        func.__kernel_function_return_required__ = final_return.get("required", False)

        return func

    return decorator


def _merge_dict_parameter_view(dict: Dict[str, Any], view: ParameterView) -> Dict[str, Any]:
    if not view:
        return dict

    if view.description:
        dict["description"] = view.description
    if view.type_:
        dict["type_"] = view.type_
    if view.type_object:
        dict["type_object"] = view.type_object
    if view.required:
        dict["required"] = view.required
    if view.default_value:
        dict["default_value"] = view.default_value
    if view.example:
        dict["example"] = view.example
    if view.type_schema:
        dict["type_schema"] = view.type_schema
    return dict


def function_parameter(
    *,
    name: str,
    description: str = None,
    default_value: str = None,
    type: str = None,
    required: Optional[bool] = None,
    example: str = None,
):
    """
    Decorator for function parameters.

    Args:
        name -- The name of the parameter
        description -- The description of the parameter
        default_value -- The default value of the parameter
        type -- The type of the parameter, used for function calling
        required -- Whether the parameter is required
        example -- The example of the parameter

    """

    def decorator(func):
        """Decorator for function parameter."""

        new_view = ParameterView(
            name=name,
            description=description,
            default_value=default_value,
            type_=type,
            required=required,
            example=example,
            kind=ParameterViewKind.ARGUMENT,
        )

        # Update parameter view lists for function_parameter decorator.
        # This will be merged into FunctionView if function decorator runs last like:
        # @function
        # @function_parameter
        # @function_parameter
        if hasattr(func, "__pf_function_parameters__"):
            current_views = func.__pf_function_parameters__
        else:
            current_views = []
        current_views.append(new_view)
        func.__pf_function_parameters__ = current_views

        # function_parameter runs after function, merge ParameterView in FunctionView
        if hasattr(func, "__pf_function__"):
            new_list = _update_list(
                new_view,
                func.__pf_function__.parameters,
                lambda item, new_item: item.name == new_item.name,
                lambda item, new_item: ParameterView.merge(item, new_item),
            )
            func.__pf_function__.parameters = new_list

        # Compatible to semantic kernel 0.9
        if hasattr(func, "__kernel_function_parameters__"):
            item = {
                "name": name,
                "description": description,
                "default_value": default_value,
                "type": type,
                "required": required,
            }

            new_list = _update_list(
                item,
                func.__kernel_function_parameters__,
                lambda item, new_item: item["name"] == new_item["name"],
                lambda item, new_item: _merge_dict(item, new_item),
            )
            func.__kernel_function_parameters__ = new_list

        return func

    return decorator


def function_return(
    *,
    description: str = None,
    default_value: str = None,
    type_: str = None,
    required: Optional[bool] = None,
    example: str = None,
):
    """
    Decorator for function return.

    Args:
        description -- The description of the return
        default_value -- The default value of the return
        type -- The type of the return, used for function calling
        required -- Whether the return is required
        example -- The example of the return

    """

    def decorator(func):
        """Decorator for function return."""

        new_view = ParameterView(
            name="return",
            description=description,
            default_value=default_value,
            type_=type_,
            required=required,
            example=example,
            kind=ParameterViewKind.RETURN,
        )

        # function_return runs after function, merge ParameterView in FunctionView
        if hasattr(func, "__pf_function__"):
            current_view = func.__pf_function__.returns[0]
            merged_view = ParameterView.merge(current_view, new_view)
            func.__pf_function__.returns = [merged_view]
        else:
            merged_view = new_view
        func.__pf_function_returns__ = [merged_view]

        # Compatible to semantic kernel 0.9
        func.__kernel_function_return_type__ = merged_view.type_
        func.__kernel_function_return_description__ = merged_view.description
        func.__kernel_function_return_required__ = merged_view.required

        return func

    return decorator


def _merge_dict(current_dict, new_dict):
    result = current_dict.copy()
    for k, v in new_dict.items():
        if v:
            result[k] = v
    return result


# Replace the parameter with the same name and keep order.
# Since there are few parameters for each function, keep use list for simplicity
def _update_list(new_item, list, condition, replacer):
    new_list = []
    replaced = False
    for item in list:
        if condition(item, new_item):
            replaced = True
            merged_item = replacer(item, new_item)
            new_list.append(merged_item)
    # Missing parameter append to the end.
    if not replaced:
        new_list.append(new_item)
    return new_list

if __name__ == "__main__":
    @function(description="anotated function", disable_docstring=True)
    @function_parameter(name="param", description="a parameter", type="str", default_value="default_val")
    @function_return(description="a result", default_value="default_result")
    def func(param: str) -> str:
        return param

    view = func.__pf_function__

    assert isinstance(view, FunctionView)
    assert view.name == "func"
    assert view.description == "anotated function"
    assert view.is_async is False
    assert view.is_stream is False

    assert view.parameters[0].name == "param"
    assert view.parameters[0].description == "a parameter"
    assert view.parameters[0].default_value == "default_val"
    assert view.parameters[0].type_ == "str"
    assert view.parameters[0].required is True
    assert view.parameters[0].example is None

    assert view.returns[0].name == "return"
    assert view.returns[0].description == "a result"
    assert view.returns[0].default_value == "default_result"
    assert view.returns[0].type_ == "str"
    assert view.returns[0].required is True
    assert view.returns[0].example is None
