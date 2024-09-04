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
class TestMixcardOcr(unittest.TestCase):

    def test_run(self):
        image_url = (
            "https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgol"
            "jdEDAzLm%2F2024-01-24T06%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe1865e4393da5a3515e90d72d81ef18"
            "296bd29598"
        )

        mixcard_ocr = appbuilder.MixCardOCR()
        out = mixcard_ocr.run(appbuilder.Message(content={"url": image_url}))
        
        self.assertIn("110103", str(out.content))
        

if __name__ == '__main__':
    unittest.main()
