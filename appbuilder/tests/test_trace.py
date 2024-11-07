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


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestTrace(unittest.TestCase):
    def test_trace(self):
        from appbuilder.utils.trace._function import _client_tool_trace_output_deep_iterate
        try:
            test_dict = {
                "a": 1,
                "b": [2],
                "c": {3: "4"},
            }
            _client_tool_trace_output_deep_iterate(output=test_dict, span=None)
        except:
            print("test_trace测试span添加dict类型")

        

if __name__ == "__main__":
    unittest.main()