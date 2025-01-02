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
from appbuilder.core.components.v2 import StyleRewrite
from appbuilder.core.component import ComponentOutput
from appbuilder import AppBuilderTracer


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestStyleRewrite(unittest.TestCase):
    def setUp(self) -> None:
        self.com = StyleRewrite(model="ERNIE-3.5-8K")
        self.tracer = AppBuilderTracer(
            enable_phoenix = False,
            enable_console = True
        )

    def test_non_stream_tool_eval(self):
        self.tracer.start_trace()
        text = "成都是个包容的城市"
        style = "直播话术"
        out = self.com.non_stream_tool_eval(query=text, style=style)
        print(out)
        self.assertIsInstance(out, ComponentOutput)
        self.tracer.end_trace()

if __name__ == '__main__':
    unittest.main()