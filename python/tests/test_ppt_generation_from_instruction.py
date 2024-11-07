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
    'text': '生成一个介绍北京的PPT。',
    'custom_data': {},
    'complex': 1,
    'user_name': '百度千帆AppBuilder'
}


@unittest.skip("暂时跳过")
class TestPPTGenerationComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        # os.environ['APPBUILDER_TOKEN'] = os.environ['APPBUILDER_TOKEN_PPT_GENERATION']
        self.ppt_generator = appbuilder.PPTGenerationFromInstruction()
    
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