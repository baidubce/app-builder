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
from appbuilder.core._exception import InvalidRequestArgumentError
from appbuilder.core.components.v2 import ObjectRecognition
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.object_recognize.model import ObjectRecognitionRequest

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestObjectRecognition(unittest.TestCase):
    def setUp(self):
        self.com = ObjectRecognition()
        self.image_url = "https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?" \
                        "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                        "11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc" \
                        "1ba1de0a8f072bc5a87102bd32f9e3"
        self.func_recognize = self.com._recognize

    def test_run(self):
        raw_image = requests.get(self.image_url).content
        message = appbuilder.Message(content={"raw_image": raw_image, "url": self.image_url})
        out = self.com.run(message)
        self.assertIsNotNone(out)
        print(out)

    def test_tool_eval(self):
        result = self.com.tool_eval(img_url=self.image_url)
        for res in result:
            self.assertIsInstance(res, ComponentOutput)
            print(res)

    def test_tool_eval_error(self):
        result = self.com.tool_eval(img_name='test_path')
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)

        result = self.com.tool_eval()
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)

    def test_recognize_error(self):
        with self.assertRaises(ValueError):
            self.func_recognize(ObjectRecognitionRequest())

        with self.assertRaises(AppBuilderServerException):
            self.func_recognize(ObjectRecognitionRequest(url='test-url'), retry=1)

if __name__ == '__main__':
    unittest.main()