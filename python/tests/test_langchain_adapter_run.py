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
import os
import unittest
import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.component import Component

class HelloWorldComponent(Component):
    manifests = [
        {
            "name": "hello_world",
            "description": "向使用这个工具的人打招呼",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "使用者的名字"
                    }
                }
            }
        }
    ]

    def run(self, name: str, **kwargs):
        return "hello world from {}".format(name)


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestLandmarkRecognition(unittest.TestCase):
    def setUp(self):
        self.component = HelloWorldComponent()

    def test_to_langchain_tool(self):
        tool = self.component.create_langchain_tool()
        from langchain.tools import StructuredTool
        self.assertIsInstance(tool, StructuredTool)

    def test_langchain_tool_run(self):
        tool = self.component.create_langchain_tool()
        res = tool.run(
            tool_input = {
                "name": "test"
            }
        )
        self.assertEqual(res, "hello world from test")

    def test_langchin_tool_elements(self):
        tool = self.component.create_langchain_tool()
        name = tool.name
        self.assertEqual(name, "hello_world")

        desc = tool.description
        self.assertEqual(desc, "向使用这个工具的人打招呼")

        args = tool.args
        self.assertEqual(args, {'name': {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'description': '使用者的名字', 'title': 'Name'}})



if __name__ == '__main__':
    unittest.main()