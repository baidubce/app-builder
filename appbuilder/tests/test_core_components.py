# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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
from io import BytesIO
import collections.abc


from appbuilder.core.components.asr.component import ASR
from appbuilder.core.components.dish_recognize.component import DishRecognition
from appbuilder.core.components.doc_crop_enhance.component import DocCropEnhance
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter, ChunkSplitter, TitleSplitter
from appbuilder.core.components.embeddings.component import Embedding
from appbuilder.core.components.extract_table.component import ExtractTableFromDoc
from appbuilder.core.components.tts.component import TTS, _iterate_chunk
from appbuilder.core.components.table_ocr.component import TableOCR

from appbuilder.core.components.tts.model import TTSRequest

from appbuilder.core.components.dish_recognize.model import *

from appbuilder.core.message import Message
from appbuilder.core.components.doc_parser.base import ParseResult, ParaNode, Position
from appbuilder.core.components.embeddings.base import EmbeddingBaseComponent
from appbuilder.core.components.llms.base import *  

from appbuilder.core._exception import *  



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
    
    def test_doc_crop_enhance_component(self):
        message=Message()
        dce=DocCropEnhance()
        with self.assertRaises(InvalidRequestArgumentError):
            dce.run(message=message,enhance_type=10)
            
    def test_doc_splitter_doc_splitter_DocSplitter(self):
        # test_if not self.splitter_type
        ds=DocSplitter(splitter_type='')
        dr=ParseResult()
        message=Message()
        message.content=dr
        with self.assertRaises(ValueError):
            ds.run(message=message)
        
        #test_splitter_type must be split_by_chunk or split_by_title
        ds=DocSplitter(splitter_type='test')
        with self.assertRaises(ValueError):
            ds.run(message=message)
        
    def test_doc_splitter_doc_splitter_ChunkSplitter(self):
        # test if not isinstance(paser_res, ParseResult)
        cs=ChunkSplitter()
        message=Message()
        with self.assertRaises(ValueError):
            cs.run(message=message)
    
    def test_doc_splitter_doc_splitter_TitleSplitter_run(self):
        # test if not isinstance(paser_res, ParseResult)
        ts=TitleSplitter()
        message=Message()
        with self.assertRaises(ValueError):
            ts.run(input_message=message)
            
    def test_doc_splitter_doc_splitter_TitleSplitter(self):
        pos = Position(
            pageno=1,
            box=[10, 20, 30, 40]
        )
        node=ParaNode(
            node_id=1,
            text='test',
            para_type= 'test',
            parent=None,
            children=[] ,
            position=[pos],
            table =None 
        )
        # test if node.para_type == "head_tail" and test segment.content
        node_head_tail=copy.deepcopy(node)
        node_head_tail.para_type='head_tail'
        message=Message()
        pr=ParseResult(
            para_node_tree=[node,node,node_head_tail]
        )
        message.content=pr
        ts=TitleSplitter()
        ts.run(input_message=message)
        
    def test_embeddings_base(self):
        ebc=EmbeddingBaseComponent()
        message=[1,2,3]
        ebc.abatch(texts=message)
        
    def test_embeddings_component_init(self):
        # test_embeddings_component_init
        with self.assertRaises(ModelNotSupportedException):
            emb=Embedding()
            emb.accepted_models.append('test')
            emb.__init__('test')
            
    
    def test_embeddings_component(self):
        #test_embeddings_component_check_response_json
        emb=Embedding()
        data={
            'error_code':'error_code',
            'error_msg': 'error_msg'
        }
        with self.assertRaises(AppBuilderServerException):
            emb._check_response_json(data=data)
                    
        # test_embeddings_component_batchify
        texts=['test','test']
        with self.assertRaises(ValueError):
            emb._batchify(texts=texts,batch_size=17)
            
    def test_extract_table_component_ExtractTableFromDoc(self):
        # test_input_check
        etf=ExtractTableFromDoc()
        message=Message()
        with self.assertRaises(ValueError):
            etf._input_check(message=message,table_max_size=29,doc_node_num_before_table=5)
        with self.assertRaises(ValueError):
            etf._input_check(message=message,table_max_size=31,doc_node_num_before_table=11)
        with self.assertRaises(ValueError):
            etf._input_check(message=message,table_max_size=31,doc_node_num_before_table=5)

        #test_post_process
        resp={
            'result':{
                'mdtables':[[
                    {'para': 'test'},
                    {'para':'描述一表：\n|数据A|数据B表|数据A|数据B表|数据A|数据B表'}
                ]]
            }
        }
        etf.table_max_size=10
        etf._post_process(resp=resp)
        
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
                
    def test_table_ocr_component_get_table_markdown(self):
        # test_get_table_markdown
        to=TableOCR()
        table={
            "body":[
                {'row_end': 1, 'col_end': 2,'row_start': 0, 'col_start': 0,'words':'words'},
            ]
        }
        tables=[table]
        md=to.get_table_markdown(tables)
            
    def test_table_ocr_component_tool_eval(self):
        # test_tool_eval 未测试完全
        to=TableOCR()
        url='https://www.baidu.com/'
        res=to.tool_eval(name="test_name", streaming=True, file_names=["test"],file_urls={'test':url})
        with self.assertRaises(AppBuilderServerException):
            next(res)
        res=to.tool_eval(name="test_name", streaming=True, files=["test"],file_urls={'test':url})
        with self.assertRaises(AppBuilderServerException):
            next(res)
            
    def test_llms_base(self):
        # test LLMMessage deepcopy
        lm=LLMMessage()
        lm.__dict__={
            "content":collections.abc.Iterator,
            'test':'test'
            }
        new_lm=copy.deepcopy(lm)
        
        
                       
        
if __name__ == "__main__":
    unittest.main()