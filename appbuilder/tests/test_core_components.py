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
import json
import copy
import appbuilder
import collections.abc


from appbuilder.core.components.asr.component import ASR
from appbuilder.core.components.dish_recognize.component import DishRecognition
from appbuilder.core.components.dish_recognize.model import DishRecognitionRequest
from appbuilder.core.message import Message
from appbuilder.core.components.llms.base import LLMMessage  
from appbuilder.core._exception import AppBuilderServerException,InvalidRequestArgumentError


# 创建ShortSpeechRecognitionRequest对象
class Request: 
    def __init__(self, format: str, rate: int, dev_pid: int, cuid: str, speech: bytes):
        """
        初始化函数，用于设置参数。
    
        Args:
            format (str): 音频格式，例如 "wav"。
            rate (int): 采样率，单位是 Hz。
            dev_pid (int): 设备 PID。
            cuid (str): 客户端 ID。
            speech (bytes): 语音字节流。
    
        Returns:
            None. 无返回值。
        """
        self.format = format  
        self.rate = rate  
        self.dev_pid = dev_pid 
        self.cuid = cuid  
        self.speech = speech
    
# 创建一个response类,模拟requests.Response
class Response:
    def __init__(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text
        
    def json(self):
            return json.loads(self.text)
        
@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreComponents(unittest.TestCase):
    def test_asr_component_ASR(self):
        # test_retry != self.http_client.retry.total
        asr=ASR()
        asr.http_client.retry.total=1
        request = Request(
            format="wav", rate=16000, dev_pid=15372, cuid="test", speech=b"")
        with self.assertRaises(AppBuilderServerException):
            asr._recognize(request=request)

    def test_dish_recognize_component(self):
        dr=DishRecognition()
        request=DishRecognitionRequest(image=b"test")
        dr.http_client.retry.total=1
        with self.assertRaises(AppBuilderServerException):
            dr._recognize(request=request)
        
            
    def test_llms_base(self):
        # test LLMMessage deepcopy
        lm=LLMMessage()
        lm.__dict__={
            "content":collections.abc.Iterator,
            'test':'test'
            }
        new_lm=copy.deepcopy(lm)
        
    def test_components_raise(self):
        # test ASR
        asr=appbuilder.ASR()
        tool=asr.tool_eval(name='test',streaming=False,file_urls={'test_1':'test'},file_name='test')
        with self.assertRaises(InvalidRequestArgumentError):
            next(tool)
            
        # test GeneralOCR
        go=appbuilder.GeneralOCR()
        tool=go.tool_eval(name='test',streaming=False,file_urls={'test_1':'test'},img_name='test')
        with self.assertRaises(InvalidRequestArgumentError):
            next(tool)
            
        # test HandwriteOCR
        hwo=appbuilder.HandwriteOCR()
        from appbuilder.core.components.handwrite_ocr.model import HandwriteOCRRequest
        hwor=HandwriteOCRRequest()
        with self.assertRaises(ValueError):
            hwo._recognize(request=hwor)
            
        # test_llms_base_ResultProcessor
        from appbuilder.core.components.llms.base import ResultProcessor,CompletionBaseComponent
        with self.assertRaises(TypeError):
            ResultProcessor.process(key='test',result_list=[])
            
            
        
        
if __name__ == "__main__":
    unittest.main()