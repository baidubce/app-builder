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
import os
from typing import Any, Dict, List, Optional, Union
from appbuilder import Manifest, manifest


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestManifestSignature(unittest.TestCase):
    def test_is_normal(self):
        @manifest()
        def func():
            return 1

        view = func.__ab_manifest__

        assert isinstance(view, Manifest)

    def test_is_async(self):
        @manifest(description="test")
        async def func():
            import asyncio

            await asyncio.sleep(0)

        view = func.__ab_manifest__

        assert isinstance(view, Manifest)

    def test_is_stream(self):
        @manifest()
        def func():
            for i in range(2):
                yield i

        view = func.__ab_manifest__

        assert isinstance(view, Manifest)

    def test_is_async_and_stream(self):
        @manifest()
        async def func():
            import asyncio

            for i in range(1):
                await asyncio.sleep(0)
                yield i

        view = func.__ab_manifest__

        assert isinstance(view, Manifest)

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

        assert isinstance(view, Manifest)
        assert view.function["name"] == "func"
        assert (
            view.function["description"]
            == """A function to test function description.

            Args:
                name (str): Name of object.

            Returns:
                str: Styled string.
            """
        )

        # Assert that parameters are an empty dictionary since there are no function arguments
        assert view.function["parameters"]["properties"] == {}
        assert view.function["parameters"]["required"] == []

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

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest)

        # 检查函数元信息
        assert view.function["name"] == "func", "Function name does not match 'func'"
        assert (
            view.function["description"]
            == """Function with required parameter.

            Args:
                name (str): Name of object.

            Returns:
                str: Styled string.
            """
        )

        # 检查参数结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'name'
        properties = parameters["properties"]
        assert "name" in properties, "'name' parameter missing"
        name_property = properties["name"]
        assert name_property["type"] == "str", "'name' type does not match 'str'"
        assert (
            name_property["description"] is None
        ), "'name' description does not match None"
        assert name_property["required"] is True, "'name' required does not match True"

    def test_decorator_google_style_list(self):
        @manifest()
        def func(
            val: List[str],
        ) -> str:
            """Function with a List parameter.

            Args:
                val (List[str]): A list of strings.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest)

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "List[str]"
        ), "'val' type does not match 'List[str]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_list_of_dicts(self):
        @manifest()
        def func(
            val: List[Dict[str, List[str]]],
        ) -> str:
            """Function with a complex nested parameter.

            Args:
                val (List[Dict[str, List[str]]]): A list of dictionaries mapping strings to lists of strings.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "List[Dict[str, List[str]]]"
        ), "'val' type does not match 'List[Dict[str, List[str]]]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_dict(self):
        @manifest()
        def func(
            val: Dict[str, Any],
        ) -> str:
            """Function with a dictionary parameter.

            Args:
                val (Dict[str, Any]): A dictionary with string keys and any values.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "Dict[str, Any]"
        ), "'val' type does not match 'Dict[str, Any]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_dict_of_lists(self):
        @manifest()
        def func(
            val: Dict[str, List[Dict[str, List[str]]]],
        ) -> str:
            """Function with a complex nested parameter.

            Args:
                val (Dict[str, List[Dict[str, List[str]]]]): A dictionary where keys are strings and values are lists of dictionaries.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "Dict[str, List[Dict[str, List[str]]]]"
        ), "'val' type does not match 'Dict[str, List[Dict[str, List[str]]]]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_union_simple(self):
        @manifest()
        def func(
            val: Union[str, int, Any],
        ) -> str:
            """Function with a Union parameter.

            Args:
                val (Union[str, int, Any]): A parameter that can accept multiple types.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "Union[str, int, Any]"
        ), "'val' type does not match 'Union[str, int, Any]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_union(self):
        @manifest()
        def func(
            val: Union[str, List[int]],
        ) -> str:
            """Function with a Union parameter.

            Args:
                val (Union[str, List[int]]): A parameter that can accept a string or a list of integers.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "Union[str, List[int]]"
        ), "'val' type does not match 'Union[str, List[int]]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_union_nest1_dict(self):
        @manifest()
        def func(
            val: Union[float, Dict[str, int]],
        ) -> str:
            """Function with a nested Union parameter.

            Args:
                val (Union[float, Dict[str, int]]): A parameter that can accept a float or a dictionary with string keys and integer values.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "Union[float, Dict[str, int]]"
        ), "'val' type does not match 'Union[float, Dict[str, int]]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_union_combine(self):
        @manifest()
        def func(
            val: Union[float, Union[str, int]],
        ) -> str:
            """Function with a combined Union parameter.

            Args:
                val (Union[float, str, int]): A parameter that can accept a float, string, or integer.

            Returns:
                str: A result string.
            """
            return ""

        view = func.__ab_manifest__

        # 检查生成的 Manifest 对象
        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        # 检查参数的总体结构
        parameters = view.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 检查具体参数 'val'
        properties = parameters["properties"]
        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证 'val' 参数的各项属性
        assert (
            val_property["type"] == "Union[float, str, int]"
        ), "'val' type does not match 'Union[float, str, int]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_no_annotation(self):
        @manifest(description="Test Function")
        def func(
            val,
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert val_property["type"] == "Any", "'val' type does not match 'Any'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_default(self):
        @manifest(description="Test Function")
        def func(val: str = "value") -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert val_property["type"] == "str", "'val' type does not match 'str'"
        assert val_property["required"] is False, "'val' required does not match False"

    def test_decorator_google_style_optional(self):
        @manifest(description="Test Function")
        def func(
            val: Optional[str],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert (
            val_property["type"] == "Optional[str]"
        ), "'val' type does not match 'Optional[str]'"
        assert val_property["required"] is False, "'val' required does not match False"

    def test_decorator_google_style_optional_equals_none(self):
        @manifest(description="Test Function")
        def func(
            val: Optional[str] = None,
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert (
            val_property["type"] == "Optional[str]"
        ), "'val' type does not match 'Optional[str]'"
        assert val_property["required"] is False, "'val' required does not match False"

    def test_decorator_google_style_optional_list(self):
        @manifest(description="Test Function")
        def func(
            val: Optional[List[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert (
            val_property["type"] == "Optional[List[str]]"
        ), "'val' type does not match 'Optional[List[str]]'"
        assert val_property["required"] is False, "'val' required does not match False"

    def test_decorator_google_style_list_nest_optional(self):
        @manifest(description="Test Function")
        def func(
            val: List[Optional[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert (
            val_property["type"] == "List[Optional[str]]"
        ), "'val' type does not match 'List[Optional[str]]'"
        assert val_property["required"] is True, "'val' required does not match True"

    def test_decorator_google_style_union_nest_single_optional(self):
        @manifest(description="Test Function")
        def func(
            val: Union[Optional[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert (
            val_property["type"] == "Optional[str]"
        ), "'val' type does not match 'Optional[str]'"
        assert val_property["required"] is False, "'val' required does not match False"

    def test_decorator_google_style_union_nest_optional(self):
        @manifest(description="Test Function")
        def func(
            val: Union[Optional[int], Optional[str]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        # 验证类型，inspect 可能优化嵌套 Union
        assert (
            val_property["type"] == "Union[int, str]"
        ), "'val' type does not match 'Union[int, str]'"
        assert val_property["required"] is False, "'val' required does not match False"

    def test_decorator_google_style_union_nest1_dict_optional_value(self):
        @manifest(description="Test Function")
        def func(
            val: Union[float, Dict[str, Optional[int]]],
        ) -> str:
            return ""

        view = func.__ab_manifest__

        assert isinstance(view, Manifest), "view is not an instance of Manifest"

        parameters = view.function["parameters"]
        properties = parameters["properties"]

        assert "val" in properties, "'val' parameter missing"
        val_property = properties["val"]

        assert (
            val_property["type"] == "Union[float, Dict[str, Optional[int]]]"
        ), "'val' type does not match 'Union[float, Dict[str, Optional[int]]]'"
        assert val_property["required"] is True, "'val' required does not match True"


if __name__ == "__main__":
    unittest.main()

