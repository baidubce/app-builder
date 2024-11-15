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
import unittest
from typing import Any, Dict, List, Optional, Union
from appbuilder import FunctionView, manifest

#@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestToolDefinitionSignature(unittest.TestCase):


    def test_is_normal(self):
        @manifest()
        def func():
            return 1

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.is_async is False
        assert view.is_stream is False


    def test_is_async(self):
        @manifest()
        async def func():
            import asyncio

            await asyncio.sleep(0)

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.is_async is True
        assert view.is_stream is False


    def test_is_stream(self):
        @manifest()
        def func():
            for i in range(2):
                yield i

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.is_async is False
        assert view.is_stream is True


    def test_is_async_and_stream(self):
        @manifest()
        async def func():
            import asyncio

            for i in range(1):
                await asyncio.sleep(0)
                yield i

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.is_async is True
        assert view.is_stream is True


    def test_decorator_google_style_function_description_no_args(self):
        @manifest()
        def func():
            """A function to test function description.

            Args:
                name (str): Name of object.

            Returns:
                str: Styled string.
            """
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.name == "func"
        assert view.description == "A function to test function description."
        assert view.is_async is False
        assert view.is_stream is False

        assert len(view.parameters) == 0


    def test_decorator_google_style_basic(self):
        @manifest()
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

        view = func.__ab_manifest__

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


    def test_decorator_google_style_list(self):
        @manifest()
        def func(
            val: List[str],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "List[str]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_list_of_dicts(self):
        @manifest()
        def func(
            val: List[Dict[str, List[str]]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "List[Dict[str, List[str]]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_dict(self):
        @manifest()
        def func(
            val: Dict[str, Any],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Dict[str, Any]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_dict_of_lists(self):
        @manifest()
        def func(
            val: Dict[str, List[Dict[str, List[str]]]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Dict[str, List[Dict[str, List[str]]]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_simple(self):
        @manifest()
        def func(
            val: Union[str, int, Any],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[str, int, Any]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union(self):
        @manifest()
        def func(
            val: Union[str, List[int]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[str, List[int]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest1_dict(self):
        @manifest()
        def func(
            val: Union[float, Dict[str, int]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[float, Dict[str, int]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_combine(self):
        @manifest()
        def func(
            val: Union[float, Union[str, int]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[float, str, int]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_no_annotation(self):
        @manifest()
        def func(
            val,
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Any"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_default(self):
        @manifest()
        def func(val: str = "value") -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)
        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value == "value"
        assert view.parameters[0].type_ == "str"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_optional(self):
        @manifest()
        def func(
            val: Optional[str],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_optional_equals_none(self):
        @manifest()
        def func(
            val: Optional[str] = None,
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_optional_list(self):
        @manifest()
        def func(
            val: Optional[List[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[List[str]]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_list_nest_optional(self):
        @manifest()
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

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].description == "Value of obj. Defaults to None."
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "List[Optional[str]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest_single_optional(self):
        @manifest()
        def func(
            val: Union[Optional[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Optional[str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest_optional(self):
        @manifest()
        def func(
            val: Union[Optional[int], Optional[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        # This one looks like a bug of inspect
        assert view.parameters[0].type_ == "Union[int, str]"
        assert view.parameters[0].required is False
        assert view.parameters[0].example is None


    def test_decorator_google_style_union_nest1_dict_optional_value(self):
        @manifest()
        def func(
            val: Union[float, Dict[str, Optional[int]]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, FunctionView)

        assert view.parameters[0].name == "val"
        assert view.parameters[0].default_value is None
        assert view.parameters[0].type_ == "Union[float, Dict[str, Optional[int]]]"
        assert view.parameters[0].required is True
        assert view.parameters[0].example is None


if __name__ == '__main__':
    unittest.main()