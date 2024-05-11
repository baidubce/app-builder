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
from appbuilder.core._exception import BaseRPCException

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

models = appbuilder.get_model_list("", ["chat"], True)
models = [models[0]]
@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestMixcardOcr(unittest.TestCase):
    @parameterized.expand([
        param(models[0], "吸塑包装盒在工业化生产和物流运输中分别有什么重要性",
                         "paddlespeech-tts", None, None, None, None),
    ])
    def test_normal_case(self, model_name, text, model, speed, pitch, volume, person):
        """
        TestTTS正常用例
        """
        tts = appbuilder.TTS()
        inp = appbuilder.Message(content={"text": text})
        param_dict = {}
        if model is not None:
            param_dict["model"] = model
            if model == "paddlespeech-tts":
                audio_type = "wav"
                param_dict["audio_type"] = audio_type
        if speed is not None:
            param_dict["speed"] = speed
        if pitch is not None:
            param_dict["pitch"] = pitch
        if volume is not None:
            param_dict["volume"] = volume
        if model is not None:
                        param_dict["person"] = person
        try:
            out = tts.run(inp, **param_dict)
            log.info(out.content["audio_binary"])
        except BaseRPCException as e:
            print("错误为 {}".format(e))
        except Exception as e:
            raise Exception("错误为 {}".format(e))
        time.sleep(1)

    @parameterized.expand([
        param("ernie-bot-apaas", "吸塑包装盒在工业化生产和物流运输中分别有什么重要性", "not_exit", 16,
                        5, 5, 0, "ValueError", "model", "unsupported"),
        param("ernie-bot-4", "吸塑包装盒在工业化生产和物流运输中分别有什么重要性", "baidu-tts", 10, 16,
                        10, 106, "ValueError", "value", "must in [0,15]"),
        param("ernie-bot-apaas", "吸塑包装盒在工业化生产和物流运输中分别有什么重要性" * 100,
                        "baidu-tts", None, None, None, None, "1", "2", "3")
    ])
    def test_abnormal_case(self, model_name, text, model, speed, pitch, volume, person, err_type, err_param, err_msg):
        """
        TestTTS正常用例
        """
        try:
            tts = appbuilder.TTS()
            inp = appbuilder.Message(content={"text": text})
            param_dict = {}
            if model is not None:
                param_dict["model"] = model
            if speed is not None:
                param_dict["speed"] = speed
            if pitch is not None:
                param_dict["pitch"] = pitch
            if volume is not None:
                param_dict["volume"] = volume
            if model is not None:
                param_dict["person"] = person
            out = tts.run(inp, **param_dict)
            log.info(out.content["audio_binary"])
            assert False, "未捕获到错误信息"
        except Exception as e:
            print("错误为 {}".format(e))
            # assert isinstance(e, eval(err_type)), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type)
            assert err_param in str(e), "捕获的异常参数类型不正确"
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()