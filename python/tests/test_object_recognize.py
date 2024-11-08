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
import requests
import appbuilder
from appbuilder.core._exception import InvalidRequestArgumentError

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestObjectRecognize(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.object_recognition = appbuilder.ObjectRecognition()

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc" \
                    "1ba1de0a8f072bc5a87102bd32f9e3"
        raw_image = requests.get(image_url).content

        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})

        # Recognize landmark
        output = self.object_recognition.run(message)

        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_no_image(self):
        """
         测试run函数在传入无效图像的情况下的行为

        Args:
            None

        Returns:
            None

        """
        # create empty message
        message = appbuilder.Message(content={})

        # Assert ValueError is raised
        with self.assertRaises(ValueError):
            self.object_recognition.run(message)

    def test_run_with_timeout_and_retry(self):
        """
        测试run方法，timeout、retry参数

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc" \
                    "1ba1de0a8f072bc5a87102bd32f9e3"
        raw_image = requests.get(image_url).content

        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})

        # Recognize landmark with timeout and retry parameters
        output = self.object_recognition.run(message, timeout=5.0, retry=3)

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
        message = appbuilder.Message({"url": url})
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.object_recognition.run(message=message)

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
            self.object_recognition.run(message=message)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        image_url = "https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc" \
                    "1ba1de0a8f072bc5a87102bd32f9e3"
        result = self.object_recognition.tool_eval(name="object_recognition", streaming=True, img_url=image_url)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(InvalidRequestArgumentError):
            result = self.object_recognition.tool_eval(name="object_recognition", streaming=True)
            next(result)
        
        with self.assertRaises(InvalidRequestArgumentError):
            result=self.object_recognition.tool_eval(name='test',streaming=False,file_urls={'test_01':'test'},img_name='test')
            next(result)
        

if __name__ == '__main__':
    unittest.main()
