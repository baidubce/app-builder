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
    'file_key': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx',
    'style': '科技',
    'color': '蓝色',
    'title': '',
    'pleader': '百度千帆AppBuilder',
    'advisor': '百度千帆AppBuilder',
    'school': '',
    'school_logo': '',
    'school_picture': ''
}


@unittest.skipUnless(os.getenv('TEST_CASE', 'UNKNOWN') == 'CPU_SERIAL', '')
class TestPPTGenerationFromPaperComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.ppt_generator = appbuilder.PPTGenerationFromPaper()
    
    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数
        """
        msg = appbuilder.Message(TEST_INPUT)
        result = self.ppt_generator(msg)
        # print(result)
        self.assertIsNotNone(result)
        print(f'\n[result]\n{result.content}\n')
    
    def test_tool_eval_with_default_params(self):
        """测试 tool_eval 方法使用默认参数
        """
        ppt_download_link = self.ppt_generator.tool_eval(**TEST_INPUT)
        # print(ppt_download_link)
        self.assertIsNotNone(ppt_download_link)
        print(f'\n[result]\n{ppt_download_link}\n')


if __name__ == '__main__':
    unittest.main()