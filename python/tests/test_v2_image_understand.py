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
import time 

from appbuilder.core.message import Message
from appbuilder.core._exception import NoFileUploadedExecption
from appbuilder.core.components.v2 import ImageUnderstand

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestImageUnderstand(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量
        Args:
            None.
        Returns:
            None.
        """
        # 从BOS存储读取样例文件
        self.image_url = "https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bfe25c372b7e56e6"
        self.raw_image = requests.get(self.image_url).content
        self.image_understand = ImageUnderstand()

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
        inp = Message(content={"url": self.image_url, "question": "图像内容是什么？"})
        msg = self.image_understand.run(inp)
        self.assertIsNotNone(msg.content)
        self.assertIsInstance(msg, Message)
        self.assertIsInstance(msg.content["description"], str)
        time.sleep(1)

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        # Create message with raw_image
        inp = Message(content={"raw_image": self.raw_image, "question": "图像内容是什么？"})
        msg = self.image_understand.run(inp)
        self.assertIsNotNone(msg.content)
        self.assertIsInstance(msg, Message)
        self.assertIsInstance(msg.content["description"], str)
        time.sleep(1)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        img_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                  "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                  "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                  "62cf937c03f8c5260d51c6ae"
        img_name = "test_img.jpg"

        file_urls = {img_name: img_url}
        result = self.image_understand.tool_eval(img_name=img_name, img_url=img_url)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)
        time.sleep(1)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(NoFileUploadedExecption):
            result = self.image_understand.tool_eval(name="image_understand", streaming=True,
                                                     origin_query="")
            next(result)
            time.sleep(1)

    def test_run_language_en(self):
        """测试 tool 方法对无效请求的处理。"""
        inp = Message(content={"raw_image": self.raw_image, "question": "图像内容是什么？", "language": "en"})
        self.image_understand.run(inp)
        time.sleep(1) 
    
    def test_run_raise(self):
        # question is empty
        with self.assertRaises(ValueError):
            inp = Message(content={"raw_image": self.raw_image, "question": ""})
            self.image_understand.run(inp)
        
        # question length bigger than 100
        with self.assertRaises(ValueError):
            question="test"*26
            inp = Message(content={"raw_image": self.raw_image, "question": question, "language": ""})
            self.image_understand.run(inp)


if __name__ == "__main__":
    unittest.main()

