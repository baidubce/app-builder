"""
Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
import os

from appbuilder.core.components.llms.style_rewrite.base import StyleChoices
import appbuilder

class TestStyleRewriteComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        
        Args:
            无参数，默认值为空。
        
        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.model_name = "ERNIE-3.5-8K"
        self.node = appbuilder.StyleRewrite(model=self.model_name)
        self.sc=StyleChoices.YINGXIAO

    def test_to_chinese(self):
        result=self.sc.to_chinese()
        self.assertEqual(result,"营销话术")
        
    def test_run_with_custom_params(self):
        """测试 run 方法使用自定义参数"""
        query = "帮我写一篇关于人体工学椅的文案"
        msg = appbuilder.Message(query)
        style = "营销话术"
        answer = self.node(msg, style=style)
        self.assertIsNotNone(answer)
        # 检查 answer 是否符合预期

    def test_tool_eval_valid(self):
        """测试 tool_eval 方法使用有效参数"""
        query = "帮我写一篇关于人体工学椅的文案"
        result = self.node.tool_eval(name="style_rewrite", streaming=True, query=query)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool_eval 方法使用无效参数"""
        with self.assertRaises(ValueError):
            result = self.node.tool_eval(name="style_rewrite", streaming=True)
            next(result)


if __name__ == '__main__':
    unittest.main()
