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
import os
import unittest
from appbuilder import FunctionView, function, function_parameter, function_return
from typing import Any, Dict, List, Optional, Union

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestToolDefinitionDecorator(unittest.TestCase):
    def test_disable_docstring():
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


    def test_combine():
        @function()
        @function_parameter(name="param", example="[1,2,3]")
        @function_return(description="Sum of param as list of number without odds.", example="6")
        def func(param: str = "[]") -> int:
            """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
            return param

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == "An example function."
        assert view.is_async is False
        assert view.is_stream is False

        assert view.parameters[0].name == "param"
        assert view.parameters[0].description == "A list of numbers."
        assert view.parameters[0].default_value == "[]"
        assert view.parameters[0].type_ == "str"
        assert view.parameters[0].required is False
        assert view.parameters[0].example == "[1,2,3]"

        assert view.returns[0].name == "return"
        assert view.returns[0].description == "Sum of param as list of number without odds."
        assert view.returns[0].default_value is None
        assert view.returns[0].type_ == "int"
        assert view.returns[0].required is True
        assert view.returns[0].example == "6"


    def test_reversed_decorators():
        @function_parameter(name="param", example="[1,2,3]", description="DECORATOR A list of numbers.")
        @function_return(description="DECORATOR The sum of parameter.", example="6")
        @function()
        def func(param: str = "[]") -> int:
            """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
            return param

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == "An example function."
        assert view.is_async is False
        assert view.is_stream is False

        assert view.parameters[0].name == "param"
        assert view.parameters[0].description == "DECORATOR A list of numbers."
        assert view.parameters[0].default_value == "[]"
        assert view.parameters[0].type_ == "str"
        assert view.parameters[0].required is False
        assert view.parameters[0].example == "[1,2,3]"

        assert view.returns[0].name == "return"
        assert view.returns[0].description == "DECORATOR The sum of parameter."
        assert view.returns[0].default_value is None
        assert view.returns[0].type_ == "int"
        assert view.returns[0].required is True
        assert view.returns[0].example == "6"


    def test_only_function_decorator():
        @function()
        def func(param: str = "[]") -> int:
            return param

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description is None
        assert view.is_async is False
        assert view.is_stream is False

        assert view.parameters[0].name == "param"
        assert view.parameters[0].description is None
        assert view.parameters[0].default_value == "[]"
        assert view.parameters[0].type_ == "str"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None

        assert view.returns[0].name == "return"
        assert view.returns[0].description is None
        assert view.returns[0].default_value is None
        assert view.returns[0].type_ == "int"
        assert view.returns[0].required is True
        assert view.returns[0].example is None

    def test_is_normal():
        @function()
        def func():
            return 1

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.is_async is False
        assert view.is_stream is False


    def test_is_async():
        @function()
        async def func():
            import asyncio

            await asyncio.sleep(0)

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.is_async is True
        assert view.is_stream is False


    def test_is_stream():
        @function()
        def func():
            for i in range(2):
                yield i

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.is_async is False
        assert view.is_stream is True


    def test_is_async_and_stream():
        @function()
        async def func():
            import asyncio

            for i in range(1):
                await asyncio.sleep(0)
                yield i

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.is_async is True
        assert view.is_stream is True


    def test_decorator_google_style_function_description_no_args():
        @function()
        def func():
            """A function to test function description.

            Args:
                name (str): Name of object.

            Returns:
                str: Styled string.
            """
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == "A function to test function description."
        assert view.is_async is False
        assert view.is_stream is False

        assert len(view.parameters) == 0


    def test_decorator_google_style_basic():
        @function()
        def func(
            name: str,
        ) -> str:
            """Function with required parameter.

            Args:
                name (str): Name of object.

            Returns:
                str: Styled string.
            """
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == "Function with required parameter."
        assert view.is_async is False
        assert view.is_stream is False
        assert view.parameters[0].name == "name"
        assert view.parameters[0].description == "Name of object."
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "str"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_list():
        @function()
        def func(
            val: List[str],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "List[str]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_list_of_dicts():
        @function()
        def func(
            val: List[Dict[str, List[str]]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "List[Dict[str, List[str]]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_dict():
        @function()
        def func(
            val: Dict[str, Any],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Dict[str, Any]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_dict_of_lists():
        @function()
        def func(
            val: Dict[str, List[Dict[str, List[str]]]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Dict[str, List[Dict[str, List[str]]]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_simple():
        @function()
        def func(
            val: Union[str, int, Any],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[str, int, Any]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union():
        @function()
        def func(
            val: Union[str, List[int]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[str, List[int]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest1_dict():
        @function()
        def func(
            val: Union[float, Dict[str, int]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[float, Dict[str, int]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_combine():
        @function()
        def func(
            val: Union[float, Union[str, int]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[float, str, int]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_no_annotation():
        @function()
        def func(
            val,
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Any"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_default():
        @function()
        def func(val: str = "value") -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)
        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value == "value"
        assert view.parameters[0].type_ == "str"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_optional():
        @function()
        def func(
            val: Optional[str],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_optional_equals_none():
        @function()
        def func(
            val: Optional[str] = None,
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_optional_list():
        @function()
        def func(
            val: Optional[List[str]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[List[str]]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_list_nest_optional():
        @function()
        def func(
            val: List[Optional[str]],
        ) -> str:
            """Functhion with optional parameter.

            Args:
                val (str): Value of obj. Defaults to None.

            Returns:
                str: Styled string.
            """
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].description == "Value of obj. Defaults to None."
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "List[Optional[str]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest_single_optional():
        @function()
        def func(
            val: Union[Optional[str]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest_optional():
        @function()
        def func(
            val: Union[Optional[int], Optional[str]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        # This one looks like a bug of inspect
        assert view.parameters[0].type_ == "Union[int, str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest1_dict_optional_value():
        @function()
        def func(
            val: Union[float, Dict[str, Optional[int]]],
        ) -> str:
            return ""

        view = func.__pf_function__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[float, Dict[str, Optional[int]]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None

if __name__ == "__main__":
    unittest.main()