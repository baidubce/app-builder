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
import appbuilder
import requests
from parameterized import parameterized, param
import appbuilder

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

image_url = ("https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa"
             "8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2"
             "188d971ca547c53d01742af4a2cbe")
raw_image = requests.get(image_url).content

@unittest.skip("Open api request limit reached")
class TestPlantRecognition(unittest.TestCase):
    @parameterized.expand([
        param(image_url, None, None),
        param(image_url, None, 0),
        param(image_url, float(120), None),
        param(image_url, None, 1),
        param(image_url, 120.5, 1),
        param(image_url, float(12000), None),
    ])
    def test_normal_case(self, image, timeout, retry):
        """
        正常用例
        """
        # 创建植物识别组件实例
        plant_recognition = appbuilder.PlantRecognition()
        # 执行识别操作并获取结果
        if timeout is None and retry is None:
            out = plant_recognition.run(appbuilder.Message(content={"url": image}))
        elif timeout is None:
            out = plant_recognition.run(appbuilder.Message(content={"url": image}), retry=retry)
        elif retry is None:
            out = plant_recognition.run(appbuilder.Message(content={"url": image}), timeout=timeout)
        else:
            out = plant_recognition.run(appbuilder.Message(content={"url": image}), timeout=timeout, retry=retry)
        
        self.assertEqual(len(out.content["plant_score_list"]), 5)

    @parameterized.expand([
        # timeout为0
        param(image_url, 0, 0, "ValueError", "timeout", 'but the timeout cannot be set to a value '
                                                                'less than or equal to 0.'),
        # timeout为字符串
        param(image_url, "a", 0, "appbuilder.core._exception.InvalidRequestArgumentError", "timeout",
                        'timeout must be float or tuple of float'),
        # timeout为0.1，太短了
        param(image_url, float(0.1), 0, "requests.exceptions.ReadTimeout", "timeout",
                        "Read timed out. (read timeout=0.1)"),
        # retry为字符串
        param(image_url, float(10), "a", "TypeError", "str", "'<' not supported between instances of"
                                                                    " 'str' and 'int'"),
        # image_url错误
        param("https://bj.bcebos.com/v1/appbuilder/xxx", 12.5, 1,
                        "appbuilder.core._exception.AppBuilderServerException", "url",
                        "service_err_message=url format illegal"),
    ])
    def test_abnormal_case(self, image, timeout, retry, err_type, err_param, err_msg):
        """
        异常用例
        """
        try:
            # 创建植物识别组件实例
            plant_recognition = appbuilder.PlantRecognition()
            # 执行识别操作并获取结果
            out = plant_recognition.run(appbuilder.Message(content={"url": image}), timeout=timeout, retry=retry)
            log.info(out.content)
            assert False, "未捕获到错误信息"
        except Exception as e:
            self.assertIsInstance(e, eval(err_type), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type))
            self.assertIn(err_param, str(e), "捕获的异常参数类型不正确, 实际:{}, 预期:{}".format(e, err_param))
            self.assertIn(err_msg, str(e), "捕获的异常消息不正确, 实际:{}, 预期:{}".format(e, err_msg))

    
if __name__ == '__main__':
    unittest.main()