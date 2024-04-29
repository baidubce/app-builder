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

import unittest
import os
import time
import appbuilder
import requests
from parameterized import parameterized, param
import appbuilder
from appbuilder import Message

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

table_info_txt_1 = '''表格列信息如下：
                        学校名 : 清华附小 , 字符串类型，代表小学学校的名称
                        所属地区 : 西城区 , 字符串类型，表示该小学学校所在的位置
                        创办时间 : 1998 , 数字值类型，表示该小学学校的创办时间
                        类别 : 公立小学 , 字符串类型，表示该小学学校所在的类别
                        学生人数 : 2000 , 数字值类型，表示该小学学校的学生数量
                        教职工人数 : 140 , 数字值类型，表示该小学学校的教职工数量
                        教学班数量 : 122 , 数字值类型，表示该小学学校的教学班数量
                    '''
models = ["ERNIE-3.5-8K"]

@unittest.skip("Open api request limit reached")
class TestNl2pandasComponent(unittest.TestCase):
    @parameterized.expand([
        param(models[0], "海淀区有哪些学校", table_info_txt_1, None, None),
        param(models[0], "西城区公立小学班级人数大于30人的数量", table_info_txt_1, False, 0.1),
        param(models[0], "列出所有学校", table_info_txt_1, True, 0.99),
    ])
    def test_normal_case(self, model_name, query, table_info, stream, temperature):
        """
        TestNl2pandasComponent正常用例
        """
        builder = appbuilder.Nl2pandasComponent(model=model_name)
        msg = Message(content=query)
        # res = builder(msg, table_info, stream=stream, temperature=temperature)
        input_params = {
            "table_info": table_info
        }
        if stream is not None:
            input_params["stream"] = stream
        if temperature is not None:
            input_params["temperature"] = temperature
        res = builder(msg, **input_params)

        if stream:
            content = "".join([i for i in res.content])
        else:
            content = res.content
        assert content
        # assert "代码" in content, "结果中未返回代码"
        log.info("{}: {}".format(model_name, content))
        time.sleep(1)

    @parameterized.expand([
        param(models[0], "海淀区有哪些学校", "表格", 2, "ValueError", "stream",
                         "Input should be a valid boolean"),
    ])
    def test_abnormal_case(self, model_name, query, table_info, stream, err_type, err_param, err_msg):
        """
        TestNl2pandasComponent异常用例
        """
        try:
            builder = appbuilder.Nl2pandasComponent(model=model_name)
            msg = Message(content=query)
            res = builder(msg, table_info, stream=stream)
            content = res.content
            log.info(content)
            assert False, "未捕获到错误信息"
        except Exception as e:
            assert isinstance(e, eval(err_type)), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type)
            assert err_param in str(e), "捕获的异常参数类型不正确"
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()