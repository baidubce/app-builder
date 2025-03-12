# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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
import unittest
import os
import requests
import unittest
import appbuilder

from appbuilder.core._exception import InvalidRequestArgumentError
from appbuilder.core.components.v2 import QRcodeOCR

class TestQRcodeOCR(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        """
        self.qrcode_ocr = QRcodeOCR()

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-" \
                    "01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6" \
                    "e74ab057ce26d50e966dc31ff083e6a9c41b"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        # Qrcode ocr
        output = self.qrcode_ocr.run(message)
        # Assert output is not None
        print(output)
        self.assertIsNotNone(output)

    def test_run_with_url(self):
        """
        使用图片 URL 进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-" \
                    "01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6" \
                    "e74ab057ce26d50e966dc31ff083e6a9c41b"
        # Create message with image URL
        message = appbuilder.Message(content={"url": image_url})
        # Qrcode ocr
        output = self.qrcode_ocr.run(message)
        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_args(self):
        """
        测试run方法，location、timeout、retry参数

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-" \
                    "01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6" \
                    "e74ab057ce26d50e966dc31ff083e6a9c41b"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        #  Qrcode ocr with timeout and retry parameters
        output = self.qrcode_ocr.run(message, location="true", timeout=5.0, retry=3)

        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_invalid_input(self):
        """
        测试run函数在传入无效输入的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        # create empty message
        message = appbuilder.Message(content={})
        # Assert ValueError is raised
        with self.assertRaises(ValueError):
            self.qrcode_ocr.run(message)

    def test_run_with_invalid_url(self):
        """
        测试run函数在传入无效URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        url = "http://example.com/invalid_url.jpg"
        message = appbuilder.Message(content={"url": url})
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.qrcode_ocr.run(message)
        
        with self.assertRaises(InvalidRequestArgumentError):
            self.qrcode_ocr.run(message=message,location='test')
        
            
    def test_tool_eval(self):
        image_url = "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-" \
                    "01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6" \
                    "e74ab057ce26d50e966dc31ff083e6a9c41b"
        result=self.qrcode_ocr.tool_eval(file_names=['test'])
        with self.assertRaises(InvalidRequestArgumentError):
            msg = next(result)
            print(msg)
        result=self.qrcode_ocr.tool_eval(
            file_names=['test'],
            _sys_file_urls={'test':image_url},
            location='True',
        )
        res=next(result)
        print(res)
        self.assertEqual(res.content[-1].visible_scope,'llm')
        res=next(result)
        print(res)
        self.assertEqual(res.content[-1].visible_scope,'user')
        
        

if __name__ == '__main__':
    unittest.main()
