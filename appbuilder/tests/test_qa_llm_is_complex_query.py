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

text = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"

models = ["ERNIE-3.5-8K"]

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestIsComplexQuery(unittest.TestCase):
    @parameterized.expand([
        param(models[0], text, None, 0.1),
        param(models[0], text, True, 0.99),
    ] )
    def test_normal_case(self, model_name, message, stream, temperature):
        """
            TestIsComplexQuery正常用例
        """
        builder = appbuilder.IsComplexQuery(model=model_name)
        msg = Message(content=message)
        input_params = {}
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
        # assert "这个问题涉及到吸塑包装盒在工业化生产和物流运输中的重要性" in content
        log.info(content)
        time.sleep(1)

    @parameterized.expand([
        param("aaa", text, "NameError", "model",
                                              "not available! You can query available models through: appbuilder."
                                              "get_model_list()")
    ])
    def test_abnormal_case(self, model_name, message, err_type, err_param, err_msg):
        """
            IsComplexQuery 异常用例
        """
        try:
            builder = appbuilder.IsComplexQuery(model=model_name)
            msg = Message(content=message)
            res = builder(msg)
            content = res.content
            log.info(content)
            assert False, "未捕获到错误信息"
        except Exception as e:
            # assert isinstance(e, eval(err_type)), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type)
            assert err_param in str(e), "捕获的异常参数类型不正确"
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()