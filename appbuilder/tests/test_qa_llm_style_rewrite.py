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
class TestStyleRewrite(unittest.TestCase):
    def test_normal_case(self):
        text = "文心大模型发布新版"
        model_name = "ERNIE-3.5-8K"
        style = "激励话术"

        builder = appbuilder.StyleRewrite(model=model_name)
        msg = appbuilder.Message(content=text)
        out = builder(msg, style=style)

        self.assertIn("文心大模型", out.content)


if __name__ == '__main__':
    unittest.main()
