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
import os

import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestIsComplexQueryComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        
        Args:
            无参数，默认值为空。
        
        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.model_name = "ERNIE-3.5-8K"
        self.node = appbuilder.IsComplexQuery(model=self.model_name)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数"""
        query = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
        msg = appbuilder.Message(query)
        answer = self.node(msg)
        self.assertIsNotNone(answer)

    # def test_run_with_custom_params(self):
    #     """测试 run 方法使用自定义参数"""
    #     query = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
    #     msg = appbuilder.Message(query)
    #     answer = self.node(msg, stream=True, temperature=0.5)
    #     self.assertIsNotNone(answer)
    #     # 检查 answer 是否符合预期

    def test_run_with_invalid_params(self):
        """测试 run 方法使用无效参数"""
        query = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
        msg = appbuilder.Message(query)
        with self.assertRaises((ValueError, TypeError)):
            self.node(msg, invalid_param="invalid")

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        params = {
            'name': 'is_complex_query',
            'query': '吸塑包装盒在工业化生产和物流运输中分别有什么重要性？'
        }
        result = self.node.tool_eval(streaming=True, **params)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)
        result = self.node.tool_eval(streaming=False, **params)
        res = [item for item in result]

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(ValueError):
            params = {
                'name': 'is_complex_query'
            }
            result = self.node.tool_eval(streaming=True, **params)
            next(result)


if __name__ == '__main__':
    unittest.main()
