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
class TestQrcodeOcr(unittest.TestCase):

    def test_run(self):
        image_url = (
            "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?"
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6"
            "e74ab057ce26d50e966dc31ff083e6a9c41b"
        )
        location = "true"

        qrcode_ocr = appbuilder.QRcodeOCR()
        out = qrcode_ocr.run(appbuilder.Message(content={"url": image_url, "location": location}))

        self.assertIn("QR_CODE", str(out.content))
        

if __name__ == '__main__':
    unittest.main()