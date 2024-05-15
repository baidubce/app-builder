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
from io import BytesIO

from appbuilder.core.components.tts.model import TTSRequest
from appbuilder.core.components.tts.component import TTS, _iterate_chunk
from appbuilder.core._exception import AppBuilderServerException

# 模拟response对象        
class MockResponse:
    def __init__(self, data):
        # 将字符串数据转换为字节流
        self.data = BytesIO(data.encode('utf-8'))

    def close(self):
        # 模拟关闭响应
        pass

    def iter_lines(self):
        # 逐行返回数据
        return self.data.readlines()
    
@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreComponentsTTS(unittest.TestCase):
    def test_tts_component_iterate_chunk_success(self):
        data = 'data: SGVsbG8sIFdvcmxkIQ=='  # base64编码的"Hello, World!"
        response = MockResponse(data)
        result = list(_iterate_chunk('test_request', response))
        self.assertEqual(result, [b'Hello, World!'])

    def test_tts_component_iterate_chunk_exception(self):
        # 模拟一个会导致异常的response
        def raise_exception():
            raise ValueError("Test Exception")
        response = MockResponse('')
        response.iter_lines = raise_exception
        with self.assertRaises(AppBuilderServerException):
            list(_iterate_chunk('test_request', response))
    
    def test_tts_model(self):
        tr = TTSRequest()
        # 定义测试参数和对应的期望结果
        test_cases = [
            ({'tex': ''}, ValueError, tr.validate_baidu_tts),
            ({'tex': 'test', 'spd': 16}, ValueError, tr.validate_baidu_tts),
            ({'tex': 'test', 'spd': 15, 'vol': 16}, ValueError, tr.validate_baidu_tts),
            ({'tex': 'test', 'spd': 15, 'vol': 15, 'per': 2}, ValueError, tr.validate_baidu_tts),
            ({'tex': 'test', 'spd': 15, 'vol': 15, 'per': 1, 'aue': 0}, None, tr.validate_baidu_tts),
            ({'tex': 'test', 'spd': 15, 'vol': 15, 'per': 1, 'aue': 2}, ValueError, tr.validate_baidu_tts),
            ({'tex': 'test', 'spd': 15, 'vol': 15, 'per': 1, 'aue': 0}, None, tr.validate_paddle_speech_tts),
            ({'tex': 'test', 'spd': 15, 'vol': 15, 'per': 1, 'aue': 1}, ValueError, tr.validate_paddle_speech_tts)
        ]

        for attrs, expected_exception, method in test_cases:
            # 设置属性
            for attr, value in attrs.items():
                setattr(tr, attr, value)
            # 验证期望结果
            if expected_exception:
                with self.assertRaises(expected_exception):
                    method()
            else:
                method()
                
if __name__ == '__main__':
    unittest.main()