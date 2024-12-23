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
class TestHandwritingOcr(unittest.TestCase):
    def test_run(self):
        image_url=("https://bj.bcebos.com/v1/appbuilder/test_handwrite_ocr.jpg?"
                   "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T"
                   "11%3A58%3A09Z%2F-1%2Fhost%2F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b0"
                "83d195c8b")
        
        image = image_url
        handwrite_ocr = appbuilder.HandwriteOCR()
        out = handwrite_ocr.run(appbuilder.Message(content={"url": image}))
        
        self.assertIn("我们家住的小区里有很多银杏树", str(out.content))


if __name__ == '__main__':
    unittest.main()