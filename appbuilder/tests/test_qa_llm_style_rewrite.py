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

text="文心大模型发布新版"
models = appbuilder.get_model_list("", ["chat"], True)

@unittest.skip("Open api request limit reached")
class TestStyleRewrite(unittest.TestCase):
    @parameterized.expand([
        param(models[0], text, "激励话术", None, None),
        param(models[0], text, "激励话术", True, None),

        param(models[0], text, "激励话术", False, 0.01),
    ])
    def test_normal_case(self, model_name, text, style, stream, temperature):
        """
        正常用例
        """
        builder = appbuilder.StyleRewrite(model=model_name)
        msg = Message(content=text)
        input_params = {}

        if stream is not None:
            input_params["stream"] = stream
        if temperature is not None:
            input_params["temperature"] = temperature

        res = builder(msg, style=style, **input_params)

        if stream:
            content = "".join([i for i in res.content])
        else:
            content = res.content 
         
        assert "文心" in content or "Wenxin" in content or "assistant" in content 
        # assert "大" in content
        assert "模型" in content or "model" in content or "assistant" in content     
        time.sleep(1)

    @parameterized.expand([
        param(
            " ", text, "激励话术", 'not available! You can query available models through: appbuilder.'
                                    'get_model_list()'),
        param(
            "aaa", text, "激励话术", 'not available! You can query available models through: appbuilder.'
                                        'get_model_list()'
        ),
        param(
            'ERNIE-Bot 4.0', text, None, "1 validation error for StyleRewriteArgs"
        ),
        param(
            'ERNIE-Bot 4.0', text, "style", '1 validation error for StyleRewriteArgs')
    ])
    def test_abnormal_case(self, model_name, text, style, err_msg):
        """
        异常用例
        """
        try:
            builder = appbuilder.StyleRewrite(model=model_name)
            msg = Message(content=text)
            res = builder(msg, style=style)
            content = res.content
            assert False, "未捕获到错误信息"
        except Exception as e:
            # assert isinstance(e, eval(err_type)), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type)
            # assert err_param in str(e), "捕获的异常参数类型不正确"
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()