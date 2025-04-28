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

import unittest
import asyncio
import json
import os
import sys


class TestOpenAPIMCPConverter(unittest.TestCase):

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def setUp(self):
        """
        设置测试环境。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """

        from mcp_server.openapi import OpenAPIMCPConverter
        self.converter = OpenAPIMCPConverter(
            base_url="https://api.github.com",
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "OpenAPIMCPConverter-Test"
            },
            timeout=30.0,
            max_retries=3
        )

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    async def asyncSetUp(self):
        """异步设置，加载本地GitHub API规范"""
        import os
        # Get the path to the test data file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_spec_path = os.path.join(current_dir, 'data', 'ghes-3.0.json')
        await self.converter.load_spec(json_spec_path)

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_list_tools(self):
        """测试 list_tools 方法"""
        async def run_test():
            await self.asyncSetUp()
            tools = self.converter.list_tools()
            self.assertIsNotNone(tools)
            self.assertTrue(len(tools) > 0)

            # 验证前5个工具的结构
            for tool in tools[:5]:
                self.assertIn('name', tool)
                self.assertIn('description', tool)
                self.assertIn('input_schema', tool)

        asyncio.run(run_test())

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_call_tool_list_repos(self):
        """测试调用 list_repos_for_user 工具"""
        async def run_test():
            await self.asyncSetUp()
            # Get a list of available tools
            tools = self.converter.list_tools()
            tool_names = [tool['name'] for tool in tools]

            # Skip the test if the tool is not available
            if "get_/users/{username}/repos" not in tool_names:
                print("Skipping test_call_tool_list_repos: Tool 'get_/users/{username}/repos' not found in local test data")
                return

            result = await self.converter.call_tool(
                "get_/users/{username}/repos",
                {
                    "username": "octocat",
                    "type": "owner",
                    "sort": "created",
                    "per_page": 1
                }
            )
            self.assertIsNotNone(result)
            self.assertTrue(isinstance(result, list))

        asyncio.run(run_test())

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_call_tool_get_repo(self):
        """测试调用 get_repo 工具"""
        async def run_test():
            await self.asyncSetUp()
            # Get a list of available tools
            tools = self.converter.list_tools()
            tool_names = [tool['name'] for tool in tools]

            # Skip the test if the tool is not available
            if "get_/repos/{owner}/{repo}" not in tool_names:
                print("Skipping test_call_tool_get_repo: Tool 'get_/repos/{owner}/{repo}' not found in local test data")
                return

            result = await self.converter.call_tool(
                "get_/repos/{owner}/{repo}",
                {
                    "owner": "octocat",
                    "repo": "Hello-World"
                }
            )
            self.assertIsNotNone(result)
            self.assertIn('name', result)
            self.assertIn('owner', result)

        asyncio.run(run_test())

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_load_yaml_spec(self):
        """测试加载YAML格式的API规范"""
        async def run_test():
            import os
            # Get the path to the test data file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            yaml_spec_path = os.path.join(current_dir, 'data', 'ghes-3.0.yaml')

            # Create a new converter for YAML test
            from mcp_server.openapi import OpenAPIMCPConverter
            yaml_converter = OpenAPIMCPConverter(
                base_url="https://api.github.com",
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "OpenAPIMCPConverter-Test"
                },
                timeout=30.0,
                max_retries=3
            )

            # Load the YAML spec
            await yaml_converter.load_spec(yaml_spec_path)

            # Verify tools were loaded
            tools = yaml_converter.list_tools()
            self.assertIsNotNone(tools)
            self.assertTrue(len(tools) > 0)

            # Clean up
            await yaml_converter.close()

        asyncio.run(run_test())

    def tearDown(self):
        """清理测试环境"""
        async def cleanup():
            await self.converter.close()

        asyncio.run(cleanup())
