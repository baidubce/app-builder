# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import appbuilder
from appbuilder import Message

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestNl2pandasComponent(unittest.TestCase):
    def test_normal_case(self):
        model_name = "ERNIE-3.5-8K"
        query = "海淀区的学校数量"
        table_info = '''表格列信息如下：
                        学校名 : 清华附小 , 字符串类型，代表小学学校的名称
                        所属地区 : 西城区 , 字符串类型，表示该小学学校所在的位置
                        创办时间 : 1998 , 数字值类型，表示该小学学校的创办时间
                        类别 : 公立小学 , 字符串类型，表示该小学学校所在的类别
                        学生人数 : 2000 , 数字值类型，表示该小学学校的学生数量
                        教职工人数 : 140 , 数字值类型，表示该小学学校的教职工数量
                        教学班数量 : 122 , 数字值类型，表示该小学学校的教学班数量
                    '''

        nl2pandas = appbuilder.Nl2pandasComponent(model=model_name)
        msg = Message(content=query)
        input_params = {
            "table_info": table_info,
        }
        out = nl2pandas(msg, **input_params)

        self.assertIn("df[", out.content)

if __name__ == '__main__':
    unittest.main()
