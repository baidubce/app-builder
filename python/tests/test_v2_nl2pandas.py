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
import unittest
import os
import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.components.v2 import Nl2pandasComponent


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestNl2pandasComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量及必要数据。
        """
        self.model_name = "ERNIE-3.5-8K"
        self.node = Nl2pandasComponent(model=self.model_name)
        self.table_info = '''表格列信息如下：
        学校名 : 清华附小 , 字符串类型，代表小学学校的名称
        所属地区 : 西城区 , 字符串类型，表示该小学学校所在的位置
        创办时间 : 1998 , 数字值类型，表示该小学学校的创办时间
        类别 : 公立小学 , 字符串类型，表示该小学学校所在的类别
        学生人数 : 2000 , 数字值类型，表示该小学学校的学生数量
        教职工人数 : 140 , 数字值类型，表示该小学学校的教职工数量
        教学班数量 : 122 , 数字值类型，表示该小学学校的教学班数量
        '''

    def test_run_with_stream_and_temperature(self):
        """测试 stream 和 temperature 参数"""
        query = "海淀区有哪些学校"
        msg = Message(query)
        code = self.node(msg, table_info=self.table_info, stream=False, temperature=0.5)
        self.assertIsNotNone(code)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        params = {
            'query': '海淀区有哪些学校',
            'table_info': self.table_info
        }
        result = self.node.tool_eval(**params)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)
        result = self.node.tool_eval(streaming=False, **params)
        res = [item for item in result]

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(ValueError):
            params = {
                'query': '海淀区有哪些学校',
                'table_info': None
            }
            result = self.node.tool_eval(**params)
            next(result)
        
        with self.assertRaises(ValueError):
            params = {
                'query': None,
                'table_info': self.table_info
            }
            result = self.node.tool_eval(**params)
            next(result)


if __name__ == '__main__':
    unittest.main()
