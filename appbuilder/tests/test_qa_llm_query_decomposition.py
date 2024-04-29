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

models = appbuilder.get_model_list("", ["chat"], True)
models=["ERNIE-3.5-8K"]

@unittest.skip("Open api request limit reached")
class TestMixcardOcr(unittest.TestCase):
    @parameterized.expand([
        param(models[0], "吸塑包装盒在工业化生产和物流运输中分别有什么重要性", None, None),
        param(models[0], "伴随“光腿神器”的热卖，网络上的各种吐槽也接踵而至。一些打底裤为追求塑造完美腿型及修"
                                    "身效果，选择不恰当的面料或剪裁方式，使得穿上后有过度紧绷感、压迫感，甚至有人形容穿起来像被“裹"
                                    "了小脚”，不得不自己DIY改造一番才能使用。近期，“光腿神器的危害有多大”“警惕光腿神器这一美丽陷"
                                    "阱”等话题频繁登上热搜。医生提醒称，“光腿神器”不仅不能瘦腿，穿错“光腿神器”会引发足部、下肢血"
                                    "管、关节、皮肤问题等累及全身多部位、组织的健康问题。", True, None),
        param(models[0], "吸塑包装盒在工业化生产和物流运输中分别有什么重要性", True, 0.1),
    ])
    def test_normal_case(self, model_name, query, stream, temperature):
        """
        TestQueryDecomposition正常用例
        """
        builder = appbuilder.QueryDecomposition(model=model_name)
        msg = Message(content=query)
        res = builder(msg)

        if stream:
            content = "".join([i for i in res.content])
        else:
            content = res.content
        print(content)
        decomposition_msg = content.split("\n")
        assert len(decomposition_msg) > 0, "未返回分解的结果"
        # for res in decomposition_msg:
        #     assert res[0].isdigit(), "返回结果错误: 开头不是编号"
        time.sleep(1)

    @parameterized.expand([
        param(models[0], "吸塑包装盒在工业化生产和物流运输中分别有什么重要性", 123, None,
                         "ValueError", "stream", "Input should be a valid boolean"),
    ])
    def test_abnormal_case(self, model_name, query, stream, temperature, err_type, err_param, err_msg):
        """
        TestQueryDecomposition异常用例
        """
        try:
            input_params = {
            }
            if stream is not None:
                input_params["stream"] = stream
            if temperature is not None:
                input_params["temperature"] = temperature
            builder = appbuilder.QueryDecomposition(model=model_name)
            msg = Message(content=query)
            res = builder(msg, **input_params)
            content = res.content
            assert False, "未捕获到错误信息"
        except Exception as e:
            print("错误为 {}".format(e))
            assert isinstance(e, eval(err_type)), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type)
            assert err_param in str(e), "捕获的异常参数类型不正确"
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()