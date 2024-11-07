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
class TestDocCropEnhance(unittest.TestCase):

    def test_run(self):
        image_url = (
            "https://bj.bcebos.com/v1/appbuilder/doc_enhance_test.png?"
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01"
            "-24T12%3A51%3A09Z%2F-1%2Fhost%2F2020d2433da471b40dafa933d557a1e"
            "be8abf28df78010f865e45dfcd6dc3951")
        enhance_type = 0
        doc_enhance = appbuilder.DocCropEnhance()
        out = doc_enhance.run(appbuilder.Message(content={"url": image_url}, enhance_type=enhance_type))

        res = out.content
        self.assertIsNotNone(res["image_processed"])
        self.assertIsNotNone(res["points"])

    
if __name__ == '__main__':
    unittest.main()