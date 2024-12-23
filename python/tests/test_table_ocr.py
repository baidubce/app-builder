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

from appbuilder.core._exception import InvalidRequestArgumentError 

class TestTableOCR(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        """
        self.table_ocr = appbuilder.TableOCR()

    def test_run_with_raw_image(self):
        """
        使用原始图片进行单测

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024" \
                    "-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
                    "064079145ff4698856f477b820147768fc2187d3"

        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        # Table ocr
        output = self.table_ocr.run(message)
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
        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024" \
                    "-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
                    "064079145ff4698856f477b820147768fc2187d3"

        # Create message with image URL
        message = appbuilder.Message(content={"url": image_url})
        # Table ocr
        output = self.table_ocr.run(message)
        # Assert output is not None
        self.assertIsNotNone(output)

    def test_run_with_timeout_and_retry(self):
        """
        测试run方法，timeout、retry参数

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024" \
                    "-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
                    "064079145ff4698856f477b820147768fc2187d3"
        raw_image = requests.get(image_url).content
        message = appbuilder.Message(content={"raw_image": raw_image})
        #  TableOCR with timeout and retry parameters
        output = self.table_ocr.run(message, timeout=5.0, retry=3)
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
            self.table_ocr.run(message)

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
            self.table_ocr.run(message)
            
    def test_tool_eval(self):
        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024" \
                    "-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
                    "064079145ff4698856f477b820147768fc2187d3"
        result=self.table_ocr.tool_eval(name='name',streaming=False,files=['test'])
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)
        result=self.table_ocr.tool_eval(
            name='name',
            streaming=True,
            file_names=['test'],
            file_urls={'test':image_url}
            )
        res=next(result)
        self.assertEqual(res['visible_scope'],'llm')
        res=next(result)
        self.assertEqual(res['visible_scope'],'user')
        


if __name__ == '__main__':
    unittest.main()
