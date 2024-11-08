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
class TestPlantRecognition(unittest.TestCase):

    def test_run(self):
        image_url = (
            "https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa"
            "8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2"
            "188d971ca547c53d01742af4a2cbe"
        )

        plant_recognition = appbuilder.PlantRecognition()
        out = plant_recognition.run(appbuilder.Message(content={"url": image_url}))
        
        self.assertTrue("plant_score_list" in out.content)
        self.assertIn("树", str(out.content))
        

if __name__ == '__main__':
    unittest.main()
