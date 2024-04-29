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
import time

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

image_url = ("https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUa"
             "sgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bf"
             "e25c372b7e56e6")
raw_image = requests.get(image_url).content

@unittest.skip("Open api request limit reached")
class TestAnimalRecognition(unittest.TestCase):
    @parameterized.expand([
        param(image_url, "图片里内容是什么?", None, None),
        param(image_url, "图片里内容是什么?", None, 0),
        param(image_url, "图片里内容是什么?", float(120), None),
        param(image_url, "图片里内容是什么?", None, 1),
        param(image_url, "图片里内容是什么?", 120.5, 1),
        param(image_url, "图片里内容是什么?", float(12000), None),
    ])
    def test_normal_case_url(self, image, question, timeout, retry):
        """
        正常用例
        """
        # 创建图像内容理解组件实例
        image_understand = appbuilder.ImageUnderstand()
        # 执行识别操作并获取结果
        if timeout is None and retry is None:
            out = image_understand.run(appbuilder.Message(content={"url": image, "question": question}))
        elif timeout is None:
            out = image_understand.run(appbuilder.Message(content={"url": image, "question": question}),
                                       retry=retry)
        elif retry is None:
            out = image_understand.run(appbuilder.Message(content={"url": image, "question": question}),
                                       timeout=timeout)
        else:
            out = image_understand.run(appbuilder.Message(content={"url": image, "question": question}),
                                       timeout=timeout, retry=retry)
        self.assertIn("图像内容可以表述为", out.content["description"])
        time.sleep(1)

    @parameterized.expand([
        # timeout为0
        param(image_url, "图片里内容是什么?", 0, 0, "ValueError", "timeout",
                        'but the timeout cannot be set to a value less than or equal to 0.'),
        # timeout为字符串
        param(image_url, "图片里内容是什么?", "a", 0,
                        "appbuilder.core._exception.InvalidRequestArgumentError", "timeout",
                        'timeout must be float or tuple of float'),
        # timeout为0.1，太短了
        param(image_url, "图片里内容是什么?", float(0.1), 0,
                        "requests.exceptions.ReadTimeout", "timeout",
                        "Read timed out. (read timeout=0.1)"),
        # retry为字符串
        param(image_url, "图片里内容是什么?", float(10), "a", "TypeError", "str",
                        "'<' not supported between instances of 'str' and 'int'"),
        # image_url错误
        # param("https://bj.bcebos.com/v1/appbuilder/xxx", "图片里内容是什么?", 12.5, 1,
        #                 "ValueError", "Unknown",
        #                 'Unknown field for ImageUnderstandTask: error_code'),
        # 问题长度超出100
        param(image_url, "图片里内容是什么?" * 20, 0, 0, "ValueError", "length",
                        'question length bigger than 100'),
    ])
    def test_abnormal_case(self, image, question, timeout, retry, err_type, err_param, err_msg):
        """
        异常用例
        """
        try:
            # 图像内容理解组件实例
            image_understand = appbuilder.ImageUnderstand()
            # 执行识别操作并获取结果
            out = image_understand.run(appbuilder.Message(content={"url": image, "question": question}),
                                       timeout=timeout, retry=retry)
            log.info(out.content)
            assert False, "未捕获到错误信息"
        except Exception as e:
            self.assertIsInstance(e, eval(err_type), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type))
            self.assertIn(err_param, str(e), "捕获的异常参数类型不正确, 预期 参数:{}, 实际:{}".format(err_param, str(e)))
            self.assertIn(err_msg, str(e), "捕获的异常消息不正确， 预期:{}, 实际:{}".format(err_msg, str(e)))

if __name__ == '__main__':
    unittest.main()