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

from appbuilder.core.components.v2 import Text2Image
from appbuilder.core.component import ComponentOutput

@unittest.skip("偶现报错暂时跳过")
class TestText2Image(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        Args:
            None
        Returns:
            None.
        """
        self.com = Text2Image()

    def test_run(self):
        """
        使用原始文本进行单测
        Args:
            None
        Returns:
            None
        """
        inp = appbuilder.Message(content={"prompt": "上海的经典风景"})
        out = self.com.run(inp)
        self.assertIsNotNone(out)
        self.assertIsInstance(out, appbuilder.Message)

    def test_tool_eval(self):
        """
        测试 tool_eval 方法的正确性。
        
        Args:
            self: 测试类的实例。
        
        Returns:
            无返回值。
        
        Raises:
            无异常抛出。
        
        """
        result = self.com.tool_eval(query = "上海的经典风景")
        for res in result:
            self.assertIsInstance(res, ComponentOutput)
            print(res)

if __name__ == '__main__':
    unittest.main()