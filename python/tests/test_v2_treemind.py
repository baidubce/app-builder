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
from appbuilder.core.message import Message
from appbuilder.core.component import Component
from appbuilder.core.component import ComponentOutput
from appbuilder.core.components.v2 import TreeMind

@unittest.skip("测试API超限，暂时跳过")
class TestTreeMindComponent(unittest.TestCase):
    def setUp(self):
        """
            初始化测试用例，设置环境变量和网关URL。
        如果没有设置CAR_EXPERT_TOKEN环境变量，则使用空字符串。
        Args:
            None.
        Returns:
            None.
        """
        self.tm = TreeMind()
        self.query = "生成一份年度总结的思维导图"

    def test_treemind_component_tool_eval(self):
        """测试tool_eval方法的返回值是否正确
        """
        import time
        time.sleep(1)
        result = self.tm.tool_eval(query=self.query)
        self.assertIsNotNone(result)
        for r in result:
            self.assertIsNotNone(r)

    def test_run_with_invalid_input(self):
        """测试run函数在传入无效输入的情况下的行为。
        """
        message = Message(content={})
        with self.assertRaises(ValueError):
            self.tm.run(message)

    def test_tool_eval_invalid(self):
        """测试 tool 方法传入无效输入的情况下的行为"""
        with self.assertRaises(TypeError):
            result = self.tm.tool_eval(name="treemind", streaming=True, origin_query="")
            next(result)

    def test_tool_eval(self):
        result = self.tm.tool_eval(query=self.query)
        for r in result:
            self.assertIsInstance(r, ComponentOutput)

if __name__ == '__main__':
    unittest.main()