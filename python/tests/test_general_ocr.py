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
import os
import unittest
import base64
import requests
import appbuilder
from appbuilder.core._exception import InvalidRequestArgumentError

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestGeneralOCR(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.general_ocr = appbuilder.GeneralOCR()

    def test_run_with_raw_image(self):
        """
        测试只使用有效图片进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                    "857a27513734d765495f89ffa5f73"
        raw_image = requests.get(image_url).content
        image_base64 = base64.b64encode(raw_image)
        # Create message with raw_image
        message = appbuilder.Message(content={"image_base64": image_base64})

        # Recognize landmark
        output = self.general_ocr.run(message)

        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_no_image(self):
        """
        测试run函数在传入无效图像的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        # create empty message
        message = appbuilder.Message(content={})

        # Assert ValueError is raised
        with self.assertRaises(ValueError):
            self.general_ocr.run(message)

    def test_run_with_timeout_and_retry(self):
        """
         测试run函数在传入timeout、retry参数

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                    "857a27513734d765495f89ffa5f73"
        raw_image = requests.get(image_url).content
        image_base64 = base64.b64encode(raw_image)
        # Create message with raw_image
        message = appbuilder.Message(content={"image_base64": image_base64})

        # Recognize general_ocr with timeout and retry parameters
        output = self.general_ocr.run(message, timeout=5.0, retry=3)

        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_invalid_url(self):
        """
        测试run函数在传入无效URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        url = "http://example.com/invalid_url.jpg"
        message = appbuilder.Message({"image_url": url})
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.general_ocr.run(message=message)

    def test_run_without_image_and_url(self):
        """
        测试run 函数在没有传入图像和URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        message = appbuilder.Message({})
        with self.assertRaises(ValueError):
            self.general_ocr.run(message=message)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        image_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                    "857a27513734d765495f89ffa5f73"
        result = self.general_ocr.tool_eval(name="general_ocr", streaming=True, img_url=image_url)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(InvalidRequestArgumentError):
            result = self.general_ocr.tool_eval(name="general_ocr", streaming=True)
            next(result)

    def test_new_tool_eval(self):
        img_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                    "857a27513734d765495f89ffa5f73"
        result = self.general_ocr.tool_eval(img_url=img_url, language_type='CHN_ENG', name="general_ocr", streaming=True,)
        for res in result:
            print(res)


if __name__ == '__main__':
    unittest.main()
