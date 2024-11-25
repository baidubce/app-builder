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
from appbuilder import Manifest, manifest, manifest_parameter
from appbuilder.core.manifest.manifest_decorator import _merge_dict, _update_list


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestManifestDecorator(unittest.TestCase):
    def test_disable_docstring(self):
        @manifest(description="anotated function")
        @manifest_parameter(name="param", description="a parameter", type="str")
        def func(param: str) -> str:
            return param

        manifest_from_function = func.__ab_manifest__

        # 断言顶层的结构
        assert manifest_from_function.type == "function", "Type does not match 'function'"
        assert (
            manifest_from_function.function["name"] == "func"
        ), "Function name does not match 'func'"
        assert (
            manifest_from_function.function["description"] == "anotated function"
        ), "Description does not match"

        # 断言参数结构
        parameters = manifest_from_function.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言具体参数
        properties = parameters["properties"]
        assert "param" in properties, "'param' parameter missing"
        assert properties["param"]["type"] == "str", "'param' type does not match 'str'"
        assert (
            properties["param"]["description"] == "a parameter"
        ), "'param' description does not match"

        # 断言必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert parameters["required"] == [
            "param"
        ], "'required' does not match ['param']"

    def test_combine(self):
        @manifest()
        @manifest_parameter(name="param")
        def func(param: str = "[]") -> int:
            """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
            return param

        # 获取装饰器生成的 Manifest
        manifest_from_function = func.__ab_manifest__

        # 断言顶层结构
        assert manifest_from_function.type == "function", "Type does not match 'function'"
        assert (
            manifest_from_function.function["name"] == "func"
        ), "Function name does not match 'func'"
        assert (
            manifest_from_function.function["description"]
            == """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
        ), "Description does not match"

        # 断言参数结构
        parameters = manifest_from_function.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言具体参数
        properties = parameters["properties"]
        assert "param" in properties, "'param' parameter missing"
        assert properties["param"]["type"] == "str", "'param' type does not match 'str'"
        assert "description" in properties["param"], "'param' description missing"
        assert (
            properties["param"]["description"] == None
        ), "'param' description does not match"

        # 断言必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert (
            "param" not in parameters["required"]
        ), "'param' should not be required as it has a default value"

    def test_reversed_decorators(self):
        @manifest_parameter(name="param", description="DECORATOR A list of numbers.")
        @manifest()
        def func(param: str = "[]") -> int:
            """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
            return param

        # 获取装饰器生成的 Manifest
        manifest_from_function = func.__ab_manifest__

        # 断言顶层结构
        assert manifest_from_function.type == "function", "Type does not match 'function'"
        assert (
            manifest_from_function.function["name"] == "func"
        ), "Function name does not match 'func'"
        assert (
            manifest_from_function.function["description"]
            == """An example function.

            Args:
                param (str): A list of numbers.

            Returns:
                int: The sum of parameter.
            """
        ), "Description does not match"

        # 断言参数结构
        parameters = manifest_from_function.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言具体参数
        properties = parameters["properties"]
        assert "param" in properties, "'param' parameter missing"
        assert properties["param"]["type"] == "str", "'param' type does not match 'str'"

        # 断言必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert (
            "param" in parameters["required"]
        ), "'param' should not be required as it has a default value"

    def test_only_function_decorator(self):
        @manifest()
        def func(param: str = "[]") -> int:
            " "
            return param

        view = func.__ab_manifest__

        # 获取装饰器生成的 Manifest
        manifest_from_function = func.__ab_manifest__

        # 断言顶层结构
        assert manifest_from_function.type == "function", "Type does not match 'function'"
        assert (
            manifest_from_function.function["name"] == "func"
        ), "Function name does not match 'func'"
        assert (
            manifest_from_function.function["description"] == " "
        ), "Description should be None when not explicitly provided"

        # 断言参数结构
        parameters = manifest_from_function.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言具体参数
        properties = parameters["properties"]
        assert "param" in properties, "'param' parameter missing"
        assert properties["param"]["type"] == "str", "'param' type does not match 'str'"

        # 检查是否为必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert (
            "param" not in parameters["required"]
        ), "'param' should not be required as it has a default value"

    def test_merge_dict(self):
        self.assertEqual(_merge_dict({}, {}), {})
        self.assertEqual(_merge_dict({}, {"a": 1}), {"a": 1})

    def test_update_list(self):
        def condition(item, new_item):
            return item['id'] == new_item['id']

        def replacer(item, new_item):
            item.update(new_item)
            return item

        existing_item = {'id': 1, 'value': 'a'}
        new_item = {'id': 1, 'value': 'b'}
        list = [existing_item]
        expected_result = [new_item]
        self.assertEqual(_update_list(new_item, list, condition, replacer), expected_result)

if __name__ == "__main__":
    unittest.main()
