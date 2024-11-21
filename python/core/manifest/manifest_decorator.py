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
import inspect
from typing import Any, Dict, Optional

from pydantic.v1 import BaseModel as PydanticBaseModel # noqa: F403 # type: ignore
from pydantic.v1 import create_model

from appbuilder.core.manifest.manifest_signature import get_signature
from appbuilder.core.manifest.models import ParameterViewKind, ParameterView, ManifestView

# The following two functions are here to allow dynamically updating function description.
# Check tool/builtin/openapi_plugin.py for example.
def function_description(cls, func):
    """Get the description of a function."""

    if hasattr(func, "__ab_manifest__"):
        view = func.__ab_manifest__
        return view.description if view else ""


def update_function_description(func, description):
    """Update function description."""
    func.__dict__["__kernel_function_description__"] = description or ""
    func.__dict__["__ab_manifest_description__"] = description or ""


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

def manifest(
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
    is_async: Optional[bool] = None,
    is_stream: Optional[bool] = None,
    return_direct: Optional[bool] = False,
):
    """
    Decorator for functions. Use some information to extract meta about function.
    Priority as follows:
    1. User provided value via arguments
    2. Function signature + annotations

    Args:
        description (str, optional): The functionality of the function, general user guideline.
        name (str, optional): The name of the function.
        is_async (bool, optional): Whether the function is asynchronous.
        is_stream (bool, optional): Whether the function is returning Iterator/AsyncIterator.
        return_direct (bool, optional): Compatible with LangChain BaseTool.return_direct.
    """

    def decorator(func):
        """Decorator for function."""

        # Get meta from signature
        sig_params, sig_returns = get_signature(func=func)

        # Get meta from decorator
        dec_params = func.__ab_manifest_parameters__ if hasattr(func, "__ab_manifest_parameters__") else {}
        dec_params = {item.name: item for item in dec_params}
        dec_returns = func.__ab_manifest_returns__[0] if hasattr(func, "__ab_manifest_returns__") else {}

        # get schema from inspect
        schema = get_function_schema_with_inspect(method=func) or {}
        final_parameters = []
        for p in sig_params:
            k = p["name"]
            # Use decorator parameters to override annotations
            c = dec_params[k] if k in dec_params else {}
            p["type_schema"] = schema.get(k, {})
            result = _merge_dict_parameter_view(p, c)
            final_parameters.append(result)

        final_return = {**sig_returns}
        final_return = _merge_dict_parameter_view(final_return, dec_returns)

        # Use provided value if not None, otherwise use reflection.
        final_name = name or func.__name__
        final_desc = description or ""

        # inspect.iscoroutinefunction(func) is not enough to check if it's async generator.
        # https://github.com/python/cpython/issues/81371
        final_async = is_async or (inspect.iscoroutinefunction(func) or inspect.isasyncgenfunction(func))
        final_stream = is_stream or (inspect.isgeneratorfunction(func) or inspect.isasyncgenfunction(func))

        view = ManifestView(
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
        func.__ab_manifest__ = view

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


def manifest_parameter(
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
        # This will be merged into ManifestView if function decorator runs last like:
        # @function
        # @function_parameter
        # @function_parameter
        if hasattr(func, "__ab_manifest_parameters__"):
            current_views = func.__ab_manifest_parameters__
        else:
            current_views = []
        current_views.append(new_view)
        func.__ab_manifest_parameters__ = current_views

        # function_parameter runs after function, merge ParameterView in ManifestView
        if hasattr(func, "__ab_manifest__"):
            new_list = _update_list(
                new_view,
                func.__ab_manifest__.parameters,
                lambda item, new_item: item.name == new_item.name,
                lambda item, new_item: ParameterView.merge(item, new_item),
            )
            func.__ab_manifest__.parameters = new_list

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


def manifest_return(
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

        # function_return runs after function, merge ParameterView in ManifestView
        if hasattr(func, "__ab_manifest__"):
            current_view = func.__ab_manifest__.returns[0]
            merged_view = ParameterView.merge(current_view, new_view)
            func.__ab_manifest__.returns = [merged_view]
        else:
            merged_view = new_view
        func.__ab_manifest_returns__ = [merged_view]

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

