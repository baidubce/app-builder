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
from appbuilder.core._exception import NoFileUploadedExecption, InvalidRequestArgumentError
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
        img_urls = ["https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                  "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                  "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                  "62cf937c03f8c5260d51c6ae",
                  "https://agi-dev-platform-file.bj.bcebos.com/files_qa/10b495b5ceea44e5a1e7d194f3a59ed7/uploads/file-6cxezmhc_1.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2025-08-04T03%3A27%3A03Z%2F259200%2Fhost%2Ff420874be9fe2511a73eab458339aad110d97c55742b14fb4fabf78cc0e1d4cc"]
        img_name = "test_img.jpg"
        _sys_file_urls = {"开户许可证.jpeg": "https://agi-dev-platform-file.bj.bcebos.com/files_qa/10b495b5ceea44e5a1e7d194f3a59ed7/uploads/file-wjka6g3h_%E5%BC%80%E6%88%B7%E8%AE%B8%E5%8F%AF%E8%AF%81.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2025-08-04T03%3A28%3A23Z%2F259200%2Fhost%2F2e3355869d9f62143051a12c2b19bc39b33d439e18839fe6dd15d0f37ab3a999"}

        result = self.image_understand.tool_eval(img_names=[img_name, "hh"], img_urls=img_urls, _sys_file_urls=_sys_file_urls)
        # for item in result:
        #     print(item)
        res = [item for item in result]
        print(res)
        self.assertNotEqual(len(res), 0)
        time.sleep(1)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(InvalidRequestArgumentError):
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

