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
class TestIsComplexQuery(unittest.TestCase):

    def test_run(self):
        model_name = "ERNIE-3.5-8K"
        message = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
        is_complex_query = appbuilder.IsComplexQuery(model=model_name)
        out = is_complex_query(appbuilder.Message(content=message))
    
        self.assertIn("类型：复杂问题", out.content)


if __name__ == '__main__':
    unittest.main()
