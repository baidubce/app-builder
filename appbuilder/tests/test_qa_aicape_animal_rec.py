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
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestAnimalRecognition(unittest.TestCase):
    
    def test_run(self):
        image_url = ("https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" 
                "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" 
                "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" 
                "62cf937c03f8c5260d51c6ae")
        
        animal_recognition = appbuilder.AnimalRecognition()
        out = animal_recognition.run(appbuilder.Message(content={"url": image_url}))
        
        self.assertIn("熊猫", str(out.content))


if __name__ == '__main__':
    unittest.main()