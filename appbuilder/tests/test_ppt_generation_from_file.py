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
    'file_url':'https://fsh.bcebos.com/v1/chenqingyang/data/PPT%E7%94%9F%E6%88%90%E6%B5%8B%E8%AF%95%E6%95%B0%E6%8D%AE/'
               '%E6%A0%B7%E4%BE%8B%E6%B5%8B%E8%AF%95%E6%96%87%E4%BB%B6/%E6%96%87%E4%BB%B6%E7%94%9F%E6%88%90PPT_%E5%8A%'
               '9F%E8%83%BD%E6%B5%8B%E8%AF%95%E6%96%87%E4%BB%B6.doc?authorization=bce-auth-v1%2F2ea5034b154145dc8962ca'
               'e2393d71a6%2F2024-08-01T12%3A15%3A17Z%2F-1%2Fhost%2F9ceed45f60a852d3ef56f405d21916af3596b2988b8f9166fa'
               '6533bd79bf0f45',
    'user_name':'百度千帆AppBuilder'
}


@unittest.skip("暂时跳过")
class TestPPTGenerationFromFileComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.ppt_generator = appbuilder.PPTGenerationFromFile()
    
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
        print(f'\n[result]\n')
        for chunk_data in self.ppt_generator.tool_eval(stream=True, **TEST_INPUT):
            print(chunk_data)


if __name__ == '__main__':
    unittest.main()