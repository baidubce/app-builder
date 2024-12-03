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
from appbuilder.core.components.v2 import Translation
from appbuilder.core.component import ComponentOutput

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestTranslation(unittest.TestCase):
    def setUp(self) -> None:
        self.com = Translation()

    def test_run(self):
        msg = appbuilder.Message(content="你好")
        result = self.com.run(message = msg, to_lang="en")
        print(result)

    def test_tool_eval(self):
        result = self.com.tool_eval(q="你好", to_lang="en")
        for res in result:
            assert isinstance(res, ComponentOutput)
            print(res)

if __name__ == '__main__':
    unittest.main()
