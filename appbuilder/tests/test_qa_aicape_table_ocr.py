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
class TestTableOcr(unittest.TestCase):

    def test_run(self):
        image_url = (
            "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?"
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6"
            "064079145ff4698856f477b820147768fc2187d3"
        )

        table_ocr = appbuilder.TableOCR()
        out = table_ocr.run(appbuilder.Message(content={"url": image_url}))
        
        self.assertIn("tables_result", out.content)
        self.assertIn("header", out.content["tables_result"][0])
        self.assertIn("body", out.content["tables_result"][0])
        self.assertIn("table_location", out.content["tables_result"][0])
        self.assertIn("流动资金来源", str(out.content))

if __name__ == '__main__':
    unittest.main()
