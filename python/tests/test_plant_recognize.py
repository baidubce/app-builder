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
from appbuilder.core.message import Message

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestPlantRecognition(unittest.TestCase):

    def setUp(self):
        """
        设置环境变量
        Args:
            None.
        Returns:
            None.
        """
        # 从BOS存储读取样例文件
        self.image_url = ("https://bj.bcebos.com/v1/appbuilder/"
                          "palnt_recognize_test.jpg?authorization="
                          "bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%"
                          "2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2"
                          "Faa2217067f78f0236c8262cdd89a4b4f4b2188"
                          "d971ca547c53d01742af4a2cbe")
        self.raw_image = requests.get(self.image_url).content
        self.plant_recognize = appbuilder.PlantRecognition()

        # 输入参数为一张图片

    def test_run_with_image_url(self):
        """
        使用图片url进行单测

        Args:
            None

        Returns:
            None

        """
        # Create message with raw_image
        inp = Message(content={"url": self.image_url})
        msg = self.plant_recognize.run(inp)
        self.assertIsNotNone(msg.content)

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        # Create message with raw_image
        inp = Message(content={"raw_image": self.raw_image})
        msg = self.plant_recognize.run(inp)
        self.assertIsNotNone(msg.content)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        img_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                  "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                  "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                  "62cf937c03f8c5260d51c6ae"
        img_name = "test_img.jpg"
        file_urls = {img_name: img_url}
        result = self.plant_recognize.tool_eval(name="plant_recognition", streaming=True,
                                                img_name=img_name, file_urls=file_urls, origin_query="")
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(ValueError):
            result = self.plant_recognize.tool_eval(name="plant_recognition", streaming=True,
                                                    origin_query="")
            next(result)


if __name__ == '__main__':
    unittest.main()
