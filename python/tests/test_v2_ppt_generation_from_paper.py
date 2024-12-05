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
import time
import unittest
import appbuilder
from appbuilder.core.component import ComponentOutput
from appbuilder.core.components.v2 import PPTGenerationFromPaper

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestPPTGenerationFromPaperComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.ppt_generator = PPTGenerationFromPaper()
        self.test_data = {
            '_sys_file_urls':  {'test_file': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx'},
            'style': '科技'
        }
    
    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数
        """
        time.sleep(2)
        user_input = {
            'file_key': list(self.test_data['_sys_file_urls'].values())[0],
            'style': self.test_data['style']
        }
        msg = appbuilder.Message(user_input)
        result = self.ppt_generator(msg)
        print(result)
        self.assertIsNotNone(result)

    def test_ppt_generation_from_file_non_stream(self):
        """测试non_stream_tool_eval
        """
        time.sleep(2)
        result = self.ppt_generator.non_stream_tool_eval(**self.test_data)
        self.assertIsInstance(result, ComponentOutput)




if __name__ == '__main__':
    unittest.main()