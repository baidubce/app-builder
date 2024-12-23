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
from appbuilder.core.components.v2 import StyleWriting
from appbuilder.core.component import ComponentOutput

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestStyleWriting(unittest.TestCase):
    def setUp(self):
        self.com = StyleWriting(model = "ERNIE-3.5-8K")

    def test_run(self):
        query = "帮我写一篇关于足球的文案"
        msg = appbuilder.Message(query)
        style = "小红书"
        length = 100
        out = self.com.run(msg, style_query=style, length=length)
        print(out)

    def test_tool_eval(self):
        query = "帮我写一篇关于足球的文案"
        style = "小红书"
        length = 150
        result = self.com.tool_eval(query, style, length)
        for res in result:
            assert isinstance(res, ComponentOutput)
            print(res)

if __name__ == '__main__':
    unittest.main()