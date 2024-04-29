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

text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
        '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
        '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
        '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
        '，实时视频分享您的生活。')
models = appbuilder.get_model_list("", ["chat"], True)

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestMixcardOcr(unittest.TestCase):
    @parameterized.expand([
        param(models[0], text, None, None),
        param(models[0], text, True, 0.99),
        # 超过1000字符
        param(models[0], "OPPO Reno5引领视频拍摄领域的创新，搭载了先进的视频超级防抖3.0技术，"
                                        "经过多代视频防抖算法的不断积累，这一代产品依然以超级防抖和卓越稳定性为特点。"
                                        "通过简单的操作，用户可以轻松开启视频超级防抖功能。具体的操作路径为：打开手机相机应用，"
                                        "切换到视频模式，然后点击屏幕上方的“超级防抖”标识即可启用这一强大的功能。"
                                        "后置摄像头支持同时使用超级防抖和超级防抖Pro功能。当用户开启视频超级防抖后，"
                                        "屏幕上将显示超级防抖Pro的开关，通过点击即可随时开启或关闭该功能。这为用户提供了更多的灵活性和掌控权"
                                        "，使他们能够根据实际拍摄需求自由选择防抖水平。"
                                        "在实际应用中，前置摄像头同样得到防抖算法的全面加持。"
                                        "这意味着即使在行走的情况下，用户仍能够拍摄出稳定、清晰的视频，"
                                        "而不必担心画面模糊或抖动。这一特性使得用户能够更自如地记录下自己的生活点滴，"
                                        "并在需要时即时分享给亲朋好友。"
                                        "通过OPPO Reno5的视频超级防抖功能，用户可以更专注地捕捉每一个精彩瞬间，"
                                        "而不必担心拍摄过程中的抖动问题。这项技术在实现超级防抖的同时，"
                                        "也注重了画面的稳定性，为用户提供更高水平的视频拍摄体验。"
                                        "其卓越的防抖性能不仅能够在运动或低光环境下取得良好效果，还在日常生活中的各种场景中表现出色。"
                                        "总体而言，OPPO Reno5的视频超级防抖技术不仅仅是一项功能，"
                                        "更是一种为用户带来更加轻松、畅快拍摄体验的创新。通过不断优化和创新，"
                                        "OPPO Reno5致力于满足用户对于高质量、稳定视频拍摄的需求，"
                                        "成为用户记录生活、分享故事的得力伙伴。", None, None)
    ])
    def test_normal_case(self, model_name, text, stream, temperature):
        """
        正常用例
        """
        builder = appbuilder.OralQueryGeneration(model=model_name)
        msg = Message(content=text)
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
        print(content)
        assert "OPPO" in content
        time.sleep(1)

    @parameterized.expand([
        param(
            " ", text, "ValueError", "Model", 'Model[ ] not available! You can query available models through: '
    'appbuilder.get_model_list()'),
        param(
            "aaa", text, "ValueError", "Model", 'Model[aaa] not available! You can query available models '
                                                'through: appbuilder.get_model_list()'
        ),
        param(
            "ERNIE-Bot 4.0", None, "ValueError", "query", "Input should be a valid string"
        )
    ])
    def test_abnormal_case(self, model_name, text, err_type, err_param, err_msg):
        """
        异常用例
        """
        try:
            builder = appbuilder.OralQueryGeneration(model=model_name)
            msg = Message(content=text)
            res = builder(msg)
            content = res.content
            print(content)
            assert False, "未捕获到错误信息"
        except Exception as e:
            print(e)
            # assert isinstance(e, eval(err_type)), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type)
            assert err_param in str(e), "捕获的异常参数类型不正确"
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()