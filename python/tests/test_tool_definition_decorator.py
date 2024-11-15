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
from appbuilder import FunctionView, manifest, manifest_parameter, manifest_return
from typing import Any, Dict, List, Optional, Union

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestToolDefinitionDecorator(unittest.TestCase):
    def test_disable_docstring(self):
        @manifest(description="anotated function", disable_docstring=True)
        @manifest_parameter(name="param", description="a parameter", type="str", default_value="default_val")
        @manifest_return(description="a result", default_value="default_result")
        def func(param: str) -> str:
            return param

        view = func.__ab_manifest__

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


    def test_combine(self):
        @manifest()
        @manifest_parameter(name="param", example="[1,2,3]")
        @manifest_return(description="Sum of param as list of number without odds.", example="6")
        def func(param: str = "[]") -> int:
            """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
            return param

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == ""
        assert view.is_async is False
        assert view.is_stream is False

        assert view.parameters[0].name == "param"
        assert view.parameters[0].description == None
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


    def test_reversed_decorators(self):
        @manifest_parameter(name="param", example="[1,2,3]", description="DECORATOR A list of numbers.")
        @manifest_return(description="DECORATOR The sum of parameter.", example="6")
        @manifest()
        def func(param: str = "[]") -> int:
            """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
            return param

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == ""
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


    def test_only_function_decorator(self):
        @function()
        def func(param: str = "[]") -> int:
            return param

        view = func.__ab_manifest__

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

if __name__ == "__main__":
    unittest.main()