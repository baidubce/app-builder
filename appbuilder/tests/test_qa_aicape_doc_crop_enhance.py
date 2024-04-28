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

image_url = "https://bj.bcebos.com/v1/appbuilder/doc_enhance_test.png?" \
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01" \
            "-24T12%3A51%3A09Z%2F-1%2Fhost%2F2020d2433da471b40dafa933d557a1e" \
            "be8abf28df78010f865e45dfcd6dc3951"
raw_image = requests.get(image_url).content

@unittest.skip("Open api request limit reached")
class TestDocCropEnhance(unittest.TestCase):
    @parameterized.expand([
           param(image_url, 0, None, None),
           param(image_url, 0, None, 0),
           param(image_url, 0, float(120), None),
           param(image_url, 0, None, 1),
           param(image_url, 0, 120.5, 1),
           param(image_url, 0, float(12000), None),
           param(image_url, 0, float(12000), None),
           param(image_url, 1, None, None),
           param(image_url, 2, None, None),
           param(image_url, 3, None, None),
           param(image_url, "0", None, None),
           param(image_url, "1", None, None),
           param(image_url, "2", None, None),
           param(image_url, "3", None, None),
    ])
    def test_normal_case(self, image, enhance_type, timeout, retry):
        """
        正常用例
        """
        # 创建二维码识别组件实例
        doc_enhance = appbuilder.DocCropEnhance()
        # 执行识别操作并获取结果
        if timeout is None and retry is None:
            out = doc_enhance.run(appbuilder.Message(content={"url": image}, enhance_type=enhance_type, ))
        elif timeout is None:
            out = doc_enhance.run(appbuilder.Message(content={"url": image}), enhance_type=enhance_type, retry=retry)
        elif retry is None:
            out = doc_enhance.run(appbuilder.Message(content={"url": image}), enhance_type=enhance_type,
                                  timeout=timeout)
        else:
            out = doc_enhance.run(appbuilder.Message(content={"url": image}), enhance_type=enhance_type,
                                  timeout=timeout, retry=retry)
        res = out.content
        self.assertIsNotNone(res["image_processed"])
        self.assertIsNotNone(res["points"])

    @parameterized.expand([
        # timeout为0
       param(image_url, 0, 0, 0, "ValueError", "timeout",
                        'but the timeout cannot be set to a value '
                        'less than or equal to 0.'),
        # timeout为字符串
       param(image_url, 1, "a", 0, "appbuilder.core._exception.InvalidRequestArgumentError", "timeout",
                        'timeout must be float or tuple of float'),
        # timeout为0.1，太短了
       param(image_url, 2, float(0.1), 0, "requests.exceptions.ReadTimeout", "timeout",
                        "Read timed out. (read timeout=0.1)"),
        # retry为字符串
       param(image_url, 3, float(10), "a", "TypeError", "str", "'<' not supported between instances of"
                                                                            " 'str' and 'int'"),
        # image_url错误
       param("https://bj.bcebos.com/v1/appbuilder/xxx", 0, 12.5, 1,
                        "appbuilder.core._exception.AppBuilderServerException", "url",
                        "service_err_message=url format illegal"),
        # enhance_type 为非0, 1, 2, 3
       param(image_url, 10, float(10), 0, "appbuilder.core._exception.InvalidRequestArgumentError",
                        "enhance_type", "enhance_type only support [0, 1, 2, 3]"),
       param(image_url, " ", float(10), 0, "appbuilder.core._exception.InvalidRequestArgumentError",
                        "enhance_type", "enhance_type only support [0, 1, 2, 3]"),
    ])
    def test_abnormal_case(self, image, enhance_type, timeout, retry, err_type, err_param, err_msg):
        """
        异常用例
        """
        try:
            # 创建表格识别组件实例
            doc_enhance = appbuilder.DocCropEnhance()
            # 执行识别操作并获取结果
            out = doc_enhance.run(appbuilder.Message(content={"url": image}), enhance_type=enhance_type,
                                  timeout=timeout, retry=retry)
            res = out.content
            assert False, "未捕获到错误信息"
        except Exception as e:
            self.assertIsInstance(e, eval(err_type), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type))
            self.assertIn(err_param, str(e), "捕获的异常参数类型不正确, 实际:{}, 预期:{}".format(e, err_param))
            self.assertIn(err_msg, str(e), "捕获的异常消息不正确, 实际:{}, 预期:{}".format(e, err_msg))

    
if __name__ == '__main__':
    unittest.main()