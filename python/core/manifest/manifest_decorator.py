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
import inspect
from typing import Any, Dict, Optional

from pydantic.v1 import BaseModel as PydanticBaseModel  # noqa: F403 # type: ignore
from pydantic.v1 import create_model

from appbuilder.core.manifest.manifest_signature import get_signature
from appbuilder.core.manifest.models import Manifest, PropertyModel, ParametersModel

def manifest(
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
):
    """
    Decorator for functions. Use some information to extract meta about function.
    Priority as follows:
    1. User provided value via arguments
    2. Function signature + annotations

    Args:
        description (str, optional): The functionality of the function, general user guideline.
        name (str, optional): The name of the function.
    """

    def decorator(func):
        """Decorator for function."""

        # Get meta from signature
        sig_params, sig_returns = get_signature(func=func)

        # Get meta from decorator
        dec_params_list = (
            func.__ab_manifest_parameters__
            if hasattr(func, "__ab_manifest_parameters__")
            else []
        )
        dec_params = {item.name: item for item in dec_params_list}

        properties = {}
        required_fields = []
        for param in sig_params:
            dec_param = dec_params.get(param["name"])
            param_type = param.get("type_") or getattr(dec_param, "type", None)

            param_info = {
                "name": param["name"],  # 参数名称
                "type": param_type,
                "description": getattr(
                    dec_params.get(param["name"]), "description", None
                ),  # 描述
                "required": param.get(
                    "required", getattr(dec_params.get(param["name"]), "required", True)
                ),  # 是否必需
            }

            # 构造 PropertyModel
            properties[param["name"]] = PropertyModel(
                name=param_info["name"],
                type=param_info["type"],
                description=param_info["description"],
                required=param_info["required"],
            )

            # 记录必需参数
            if param_info["required"]:
                required_fields.append(param["name"])

        # 确定函数的最终名称和描述
        final_name = name or func.__name__
        final_desc = description or func.__doc__

        parameters_model = ParametersModel(
            type="object",
            properties={
                k: v.model_dump(exclude_none=False) for k, v in properties.items()
            },
            required=required_fields,
        )

        view = Manifest(
            type="function",
            function={
                "name": final_name,
                "description": final_desc,
                "parameters": parameters_model.model_dump(),
            },
        )

        # Attach view to function.
        func.__ab_manifest__ = view

        # Compatible to semantic kernel 0.9 ~ 1.6 according to this url: https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/functions/kernel_function_decorator.py
        func.__kernel_function__ = True
        func.__kernel_function_description__ = final_desc
        func.__kernel_function_name__ = final_name

        return func

    return decorator


def manifest_parameter(
    *,
    name: str,
    description: str = None,
    type: str = None,
    required: bool = True,
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

        new_view = PropertyModel(
            name=name,
            type=type,
            description=description,
            required=required,
        )
        # Update parameter view lists for function_parameter decorator.
        # This will be merged into ManifestView if function decorator runs last like:
        # @manifest
        # @manifest_parameter
        # @manifest_parameter
        if hasattr(func, "__ab_manifest_parameters__"):
            current_views = func.__ab_manifest_parameters__
        else:
            current_views = []
        current_views.append(new_view)
        func.__ab_manifest_parameters__ = current_views

        if hasattr(func, "__ab_manifest__"):
            # 获取现有的 parameters
            parameters_dict = func.__ab_manifest__.function.get("parameters", {})
            parameters_model = ParametersModel(**parameters_dict)

            # 更新 properties
            existing_property = parameters_model.properties.get(new_view.name)
            if existing_property:
                merged_property = PropertyModel.merge(existing_property, new_view)
                parameters_model.properties[new_view.name] = merged_property
            else:
                parameters_model.properties[new_view.name] = new_view

            # 更新 required 字段
            if new_view.required:
                if new_view.name not in parameters_model.required:
                    parameters_model.required.append(new_view.name)
            else:
                if new_view.name in parameters_model.required:
                    parameters_model.required.remove(new_view.name)

            # 更新 func.__ab_manifest__.function["parameters"]
            func.__ab_manifest__.function["parameters"] = parameters_model.model_dump()

        # Compatible to semantic kernel 0.9 ~ 1.6 according to this url: https://github.com/microsoft/semantic-kernel/blob/main/python/semantic_kernel/functions/kernel_function_decorator.py
        if hasattr(func, "__kernel_function_parameters__"):
            item = {
                "name": name,
                "description": description,
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
