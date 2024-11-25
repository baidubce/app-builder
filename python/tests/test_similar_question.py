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

class TestSimilarQuestionComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        
        Args:
            无参数，默认值为空。
        
        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.model_name = "ERNIE-3.5-8K"
        self.node = appbuilder.SimilarQuestion(model=self.model_name)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数"""
        query = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        msg = appbuilder.Message(query)
        answer = self.node(msg)
        self.assertIsNotNone(answer)

    def test_tool_eval_valid(self):
        """测试 tool_eval 方法使用有效参数"""
        query = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        result = self.node.tool_eval(name="similar_question", streaming=True, query=query)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool_eval 方法使用无效参数"""
        with self.assertRaises(ValueError):
            result = self.node.tool_eval(name="similar_question", streaming=True)
            next(result)


if __name__ == '__main__':
    unittest.main()
