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

import requests

import appbuilder
from appbuilder.core.component import ComponentOutput
from appbuilder.core.components.v2 import SimilarQuestion

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestSimilarQuestion(unittest.TestCase):
    def setUp(self):
        self.com = SimilarQuestion(model="ERNIE-3.5-8K")

    def test_run(self):
        query = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        msg = appbuilder.Message(query)
        out = self.com.run(msg)
        self.assertIsNotNone(out)
        print(out)

    def test_tool_eval(self):
        query = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        for output in self.com.tool_eval(query):
            self.assertIsInstance(output, ComponentOutput)
            print(output)

if __name__ == '__main__':
    unittest.main()

