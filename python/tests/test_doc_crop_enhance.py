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
import requests
import appbuilder
import os
class TestDocCropEnhance(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        """
        self.doc_crop_enhance = appbuilder.DocCropEnhance()

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/doc_enhance_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01" \
                    "-24T12%3A51%3A09Z%2F-1%2Fhost%2F2020d2433da471b40dafa933d557a1e" \
                    "be8abf28df78010f865e45dfcd6dc3951"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        # Doc enhance
        output = self.doc_crop_enhance.run(message)
        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_url(self):
        """
        使用图片 URL 进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/doc_enhance_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01" \
                    "-24T12%3A51%3A09Z%2F-1%2Fhost%2F2020d2433da471b40dafa933d557a1e" \
                    "be8abf28df78010f865e45dfcd6dc3951"
        # Create message with image URL
        message = appbuilder.Message(content={"url": image_url})
        # Doc enhance
        output = self.doc_crop_enhance.run(message)
        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_timeout_and_retry(self):
        """
        测试run方法，enhance_type、timeout、retry参数

        Args:
            None

        Returns:
            None

        """
        # 定义一个图片URL
        image_url = "https://bj.bcebos.com/v1/appbuilder/doc_enhance_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01" \
                    "-24T12%3A51%3A09Z%2F-1%2Fhost%2F2020d2433da471b40dafa933d557a1e" \
                    "be8abf28df78010f865e45dfcd6dc3951"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        #  Doc enhance with timeout and retry parameters
        output = self.doc_crop_enhance.run(message, enhance_type=3, timeout=5.0, retry=3)

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
            self.doc_crop_enhance.run(message)

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
            self.doc_crop_enhance.run(message)


if __name__ == '__main__':
    unittest.main()
