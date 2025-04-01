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
# !/usr/bin/env python3


import os
import unittest
from typing import List, Tuple
import appbuilder
from appbuilder.core.components.v2 import QueryRewrite


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")  
class TestQueryRewriteComponent(unittest.TestCase):
    def setUp(self):
        """
        初始化查询重写组件的单元测试基类。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        """
        # 设置环境变量和初始化TranslateComponent实例
        self.model_name = "ERNIE-3.5-8K"
        self.node = QueryRewrite(model=self.model_name)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数"""
        query = ['我应该怎么办理护照？', '您可以查询官网或人工咨询', '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']
        msg = appbuilder.Message(query)
        answer = self.node(msg)
        self.assertIsNotNone(answer)
        # 可以添加更多断言来检查 answer 的特定属性

    def test_run_with_custom_params(self):
        """测试 run 方法使用自定义参数"""
        query = ['我应该怎么办理护照？', '您可以查询官网或人工咨询', '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']
        msg = appbuilder.Message(query)
        type = "仅用户查询"
        answer = self.node(msg, rewrite_type=type)
        self.assertIsNotNone(answer)
        # 检查 answer 是否符合预期

    def test_run_with_stream_and_temperature(self):
        """测试不同的 stream 和 temperature 参数值"""
        node = QueryRewrite("ERNIE-3.5-8K")
        query = ['我应该怎么办理护照？', '您可以查询官网或人工咨询', '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']
        msg = appbuilder.Message(query)
        answer = node(msg, rewrite_type="带机器人回复", stream=False, temperature=0.5)
        self.assertIsNotNone(answer)
        
    def test_run_raise(self):
        with self.assertRaises(ValueError):
            self.node(message=None)

        query = ['我应该怎么办理护照？', '您可以查询官网或人工咨询']
        msg=appbuilder.Message(query)
        with self.assertRaises(ValueError):
            self.node(message=msg)
           
        test_str='test'*1500    
        query = [test_str]
        msg=appbuilder.Message(query)
        with self.assertRaises(ValueError):
            self.node(message=msg) 

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        params = {
            'query': ['我应该怎么办理护照？', '您可以查询官网或人工咨询']
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
                'query': None
            }
            result = self.node.tool_eval(**params)
            next(result)


if __name__ == '__main__':
    unittest.main()
