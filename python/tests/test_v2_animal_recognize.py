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
from appbuilder.core.components.v2 import AnimalRecognition
import os

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestAnimalRecognition(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        """
        self.animal_recognition = AnimalRecognition()

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        # Recognize animal
        output = self.animal_recognition.run(message)
        # Assert output is not None
        self.assertIsNotNone(output)
        self.assertIsInstance(output, appbuilder.Message)
        self.assertIsInstance(output.content["result"], list)
        self.assertIsInstance(output.content["result"][0]["name"], str)
        

    def test_run_with_url(self):
        """
        使用图片 URL 进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"
        # Create message with image URL
        message = appbuilder.Message(content={"url": image_url})
        # Recognize animal
        output = self.animal_recognition.run(message)
        # Assert output is not None
        self.assertIsNotNone(output)
        self.assertIsInstance(output, appbuilder.Message)

    def test_run_with_timeout_and_retry(self):
        """
        测试run方法，timeout、retry参数

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"url": image_url, "raw_image": raw_image})
        # Recognize animal with timeout and retry parameters
        output = self.animal_recognition.run(message, timeout=5.0, retry=3)
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
            self.animal_recognition.run(message)

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
            self.animal_recognition.run(message)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        img_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"
        img_name = "test_img.jpg"
        file_urls = {img_name: img_url}
        result = self.animal_recognition.tool_eval(img_name=img_name, img_url=img_url, file_urls=file_urls)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(ValueError):
            result = self.animal_recognition.tool_eval(name="animal_recognition", streaming=True,
                                                       origin_query="")
            next(result)

    def test_tool_eval_raise_exception(self):
        """测试 tool 方法对异常情况的处理。"""
        with self.assertRaises(ValueError):
            result = self.animal_recognition.tool_eval()
            next(result)


if __name__ == '__main__':
    unittest.main()
