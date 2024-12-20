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

import requests

import appbuilder
from appbuilder.core.component import ComponentOutput
from appbuilder.core._exception import InvalidRequestArgumentError
from appbuilder.core.components.v2 import ASR
from appbuilder.core.components.v2.asr.component import _convert as convert

@unittest.skip("测试API超限，暂时跳过")
class TestASR(unittest.TestCase):
    def setUp(self):
        self.audio_file_url = "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                              "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                              "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
        self.com = ASR()

    def test_asr_run(self):
        raw_audio = requests.get(self.audio_file_url).content
        inp = appbuilder.Message(content={"raw_audio": raw_audio})
        out = self.com.run(inp)
        self.assertIsNotNone(out)
        print(out)

    def test_asr_tool_eval(self):
        result = self.com.tool_eval(file_url=self.audio_file_url)
        for res in result:
            self.assertIsInstance(res, ComponentOutput)
            print(res)

    def test_asr_tool_eval_error(self):
        result = self.com.tool_eval()
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)

        result = self.com.tool_eval(file_name='test_path')
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)

    def test_convert_with_mp3(self):
        file_type = ["mp3", "wav", "pcm", "m4a"]
        for type in file_type:
            with self.assertRaises(FileNotFoundError):
                path = os.path.join(os.path.dirname(__file__), "test_audio")
                path += ".{}".format(type)
                convert(path, type)

if __name__ == '__main__':
    unittest.main()