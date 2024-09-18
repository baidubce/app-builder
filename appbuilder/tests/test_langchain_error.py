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

class HelloWorldComponentwithoutMainfest(Component):
    def run(self, name: str, **kwargs):
        return Message(content="hello world from {}".format(name))
    
class HelloWorldComponentwithMultiTools(Component):
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
        },
        {
            "name": "hello_world_2",
            "description": "向使用这个工具的人打招呼",
        },
        {
            "name": "general_ocr",
            "description": "提供更高精度的通用文字识别能力，能够识别图片中的文字，不支持html后缀文件的输入",
            "parameters": {
                "type": "object",
                "properties": {
                    "img_url": {
                        "type": "string",
                        "description": "待识别图片的url,根据该url能够获取图片"
                    },
                    "img_name": {
                        "type": "string",
                        "description": "待识别图片的文件名,用于生成图片url"
                    },
                },
                "anyOf": [
                    {
                        "required": [
                            "img_url"
                        ]
                    },
                    {
                        "required": [
                            "img_name"
                        ]
                    }
                ]
            }
        }

    ]

    def run(self, name: str, **kwargs):
        return Message(content="hello world from {}".format(name))

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestLandmarkRecognition(unittest.TestCase):
    def test_without_mainfest(self):
        component = HelloWorldComponentwithoutMainfest()
        with self.assertRaises(ValueError):
            tool = component.create_langchain_tool()

    def test_with_multi_tools(self):
        component = HelloWorldComponentwithMultiTools()
        with self.assertRaises(ValueError):
            tool = component.create_langchain_tool()

    def test_with_multi_tools_v2(self):
        component = HelloWorldComponentwithMultiTools()
        tools = component.create_langchain_tool(tool_name="hello_world")


    def test_with_multi_tools_v3(self):
        component = HelloWorldComponentwithMultiTools()
        with self.assertRaises(ValueError):
            tools = component.create_langchain_tool(tool_name="hello_world_3")

    def test_with_multi_tools_v4(self):
        component = HelloWorldComponentwithMultiTools()
        with self.assertRaises(RuntimeError):
            tools = component.create_langchain_tool(tool_name="hello_world_2")

    def test_with_multi_tools_v5(self):
        component = HelloWorldComponentwithMultiTools()
        tools = component.create_langchain_tool(tool_name="general_ocr")

if __name__ == '__main__':
    unittest.main()