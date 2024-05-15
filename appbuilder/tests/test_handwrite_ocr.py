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
from appbuilder.core._exception import InvalidRequestArgumentError 

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
        self.image_url=("https://bj.bcebos.com/v1/appbuilder/test_handw"
                        "rite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8"
                        "m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2"
                        "F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b")
        self.raw_image = requests.get(self.image_url).content
        self.handwrite_ocr = appbuilder.HandwriteOCR()

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
        msg = self.handwrite_ocr.run(inp)
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
        msg = self.handwrite_ocr.run(inp)
        self.assertIsNotNone(msg.content)
        
    def test_tool_eval(self):
        result=self.handwrite_ocr.tool_eval(name='name',streaming=False,files=['test'])
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)
        result=self.handwrite_ocr.tool_eval(
            name='name',
            streaming=True,
            file_names=['test'],
            file_urls={'test':self.image_url}
            )
        res=next(result)
        self.assertEqual(res['visible_scope'],'llm')
        res=next(result)
        self.assertEqual(res['visible_scope'],'user')


if __name__ == '__main__':
    unittest.main()
