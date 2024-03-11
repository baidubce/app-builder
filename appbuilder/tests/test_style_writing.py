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

import appbuilder
from appbuilder.core.components.llms.style_writing.component import StyleQueryChoices, LengthChoices


class TestStyleWritingComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        
        Args:
            无参数，默认值为空。
        
        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.model_name = "ERNIE Speed-AppBuilder"
        self.node = appbuilder.StyleWriting(model=self.model_name)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数"""
        query = "帮我写一篇关于人体工学椅的文案"
        msg = appbuilder.Message(query)
        answer = self.node(msg)
        self.assertIsNotNone(answer)
        # 可以添加更多断言来检查 answer 的特定属性

    def test_run_with_custom_params(self):
        """测试 run 方法使用自定义参数"""
        query = "帮我写一篇关于人体工学椅的文案"
        msg = appbuilder.Message(query)
        style = "小红书"
        length = 300
        answer = self.node(msg, style_query=style, length=length)
        self.assertIsNotNone(answer)
        # 检查 answer 是否符合预期

    def test_run_with_invalid_params(self):
        """测试 run 方法使用无效参数"""
        query = "帮我写一篇关于人体工学椅的文案"
        msg = appbuilder.Message(query)
        style = "无效样式"
        with self.assertRaises(ValueError):
            self.node(msg, style_query=style)

    def test_run_with_different_style_query(self):
        """测试不同的 style_query 参数值"""
        node = appbuilder.StyleWriting("ERNIE Speed-AppBuilder")
        msg = appbuilder.Message("测试消息")
        for style_query in StyleQueryChoices:
            with self.subTest(style_query=style_query):
                answer = node(msg, style_query=style_query.value, length=100)
                self.assertIsNotNone(answer)

    def test_run_with_different_length(self):
        """测试不同的 length 参数值"""
        node = appbuilder.StyleWriting("ERNIE Speed-AppBuilder")
        msg = appbuilder.Message("测试消息")
        for length in LengthChoices:
            with self.subTest(length=length):
                answer = node(msg, style_query="通用", length=length.value)
                self.assertIsNotNone(answer)

    def test_run_with_stream_and_temperature(self):
        """测试不同的 stream 和 temperature 参数值"""
        node = appbuilder.StyleWriting("ERNIE Speed-AppBuilder")
        msg = appbuilder.Message("测试消息")
        answer = node(msg, style_query="通用", length=100, stream=False, temperature=0.5)
        self.assertIsNotNone(answer)


if __name__ == '__main__':
    unittest.main()
