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
import time
import appbuilder
from appbuilder.core.components.v2 import StyleRewrite
from appbuilder.core.component import ComponentOutput

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestStyleRewrite(unittest.TestCase):
    def setUp(self) -> None:
        self.com = StyleRewrite(model="ERNIE-3.5-8K")
    
    def test_normal_case(self):
        time.sleep(2)
        text = "文心大模型发布新版"
        style = "激励话术"
        msg = appbuilder.Message(content=text)
        out = self.com(msg, style=style)
        self.assertIn("文心大模型", out.content)

    def test_tool_eval(self):
        time.sleep(2)
        text = "文心大模型发布新版"
        style = "营销话术"
        out = self.com.tool_eval(query=text, style=style)
        for item in out:
            self.assertIsInstance(item, ComponentOutput)

    def test_non_stream_tool_eval(self):
        text = "成都是个包容的城市"
        style = "直播话术"
        out = self.com.non_stream_tool_eval(query=text, style=style)
        print(out)
        self.assertIsInstance(out, ComponentOutput)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(TypeError):
            result = self.com.tool_eval(name="image_understand", streaming=True,
                                                     origin_query="")


if __name__ == '__main__':
    unittest.main()
