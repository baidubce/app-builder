"""
Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import os
import unittest
import appbuilder

TEST_INPUT = {
    "query": appbuilder.Message("这篇文档讲了什么"),
    "instruction": "请根据文档内容回答问题",
    "addition_instruction": "请你用一句话简短概括",
    "file_path": "data/qa_demo.xlsx",
    "stream": True,
    "app_id": "87187054-78f0-4ef3-b710-fdcf2bfba7f2"
}


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestDocumentUnderstandingComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.du = appbuilder.DocumentUnderstanding()

    def test_run_with_stream(self):
        """测试 run 方法流式输出
        """
        query = TEST_INPUT.get("query")
        results = self.du.run(query,
                             TEST_INPUT.get("file_path"),
                             instruction=TEST_INPUT.get("instruction"),
                             addition_instruction=TEST_INPUT.get("addition_instruction"),
                             stream=TEST_INPUT.get("stream"),
                             app_id=TEST_INPUT.get("app_id"))

        for result in results:
            self.assertIsNotNone(result)
            print(f'\n[result]\n{result}\n')

    def test_run_with_nostream(self):
        """测试 run 方法非流式输出
        """
        query = TEST_INPUT.get("query")
        results = self.du.run(query,
                             TEST_INPUT.get("file_path"),
                             instruction=TEST_INPUT.get("instruction"),
                             addition_instruction=TEST_INPUT.get("addition_instruction"),
                             stream=False,
                             app_id=TEST_INPUT.get("app_id"))

        for result in results:
            self.assertIsNotNone(result)
            print(f'\n[result]\n{result}\n')
    def test_run_with_nofile(self):
        """测试 run 方法上传无效文件
        """
        query = TEST_INPUT.get("query")
        # 使用 assertRaises 捕获预期异常
        with self.assertRaises(FileNotFoundError):  # 假设无效文件抛出 FileNotFoundError 异常
            results = self.du.run(query,
                                  "invalid_file.txt",  # 使用无效文件
                                  instruction=TEST_INPUT.get("instruction"),
                                  addition_instruction=TEST_INPUT.get("addition_instruction"),
                                  stream=False,
                                  app_id=TEST_INPUT.get("app_id"))

            # 如果 run 方法抛出异常，以下代码将不会执行
            for result in results:
                self.assertIsNotNone(result)
                print(f'\n[result]\n{result}\n')

    def test_tool_eval(self):
        '''测试tool_eval方法'''
        INPUT_JON_ = {
            "instruction": TEST_INPUT.get("instruction", ""),
            "addition_instruction": TEST_INPUT.get("addition_instruction", ""),
            "app_id": TEST_INPUT.get("app_id")
        }
        query = TEST_INPUT.get("query", "")
        results = self.du.tool_eval(query, file_path=TEST_INPUT.get("file_path", ""), stream=False, **INPUT_JON_)
        for result in results:
            print(result)


if __name__ == '__main__':
    unittest.main()
