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

from appbuilder.core.console.base import ConsoleLLMMessage,ConsoleCompletionResponse
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.message import Message

# 创建一个response类,模拟requests.Response
class Response:
    def __init__(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text
        
    def json(self):
            return json.loads(self.text)
       

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreConsoleBase(unittest.TestCase):
    def test_ConsoleLLMMessage_init(self):
        # 测试stream=True
        cr=ConsoleLLMMessage()
        self.assertIsInstance(str(cr), str)
        
    def test_ConsoleCompletionResponse_init(self):
        # 测试初始化,同时测试response.status_code != 200 and 
        response=Response(
            status_code=201,
            headers={},
            text=json.dumps({"message": "test"})
        )
        with self.assertRaises(AppBuilderServerException):
            ConsoleCompletionResponse(response)
            
        # 测试if "code" in data and "message" in data and "requestId" in data
        response=Response(
            status_code=200,
            headers={},
            text=json.dumps({
                "code": "test",
                "requestId":"test",
                "message":"test"
                })
        )
        with self.assertRaises(AppBuilderServerException):
            ConsoleCompletionResponse(response)
            
        # 测试if "code" in data and "message" in data and "status" in data
        response=Response(
            status_code=200,
            headers={},
            text=json.dumps({
                "code": "test",
                "message":"test",
                "status":"test"
                })
        )
        with self.assertRaises(AppBuilderServerException):
            ConsoleCompletionResponse(response)
        
        # if "code" in data and data.get("code") != 0
        response=Response(
            status_code=200,
            headers={},
            text=json.dumps({
                "code": 1,
                "message": "test"
                })
        )
        with self.assertRaises(AppBuilderServerException):
            ConsoleCompletionResponse(response)
            
        # 测试init其余部分
        content = [
            {
                "content_type": "references",
                "outputs": {
                    "references": [
                        {"from": "key"} 
                        # 确认这是一个正确的字典
                    ]
                }
            }
        ]

        # 序列化 content 列表为 JSON 字符串
        content_json = json.dumps(content)

        # 使用序列化后的 JSON 字符串作为响应文本
        response = Response(
            status_code=200,
            headers={},
            text=json.dumps({
                "code": 0,
                "result": {
                    "answer": "test",
                    "conversation_id": "test",
                    "content": content  # 这里直接使用 content 变量
                }
            })
        )
        ccr=ConsoleCompletionResponse(response) 
        
        # test_ConsoleCompletionResponse_message_iterable_wrapper(原代码可能冗余，迭代器未被调用)
        message = Message()
        def message_content():
            resps=[
                {'result': {'answer': 'test', 'conversation_id': 'test', 'content': content}},
                {'result': {'answer': 'test', 'conversation_id': 'test', 'content': content}}
            ]
            for resp in resps:
                yield resp
        message.content = message_content()
        result = ccr.message_iterable_wrapper(message)
  
        #test_ConsoleCompletionResponse_to_message
        message=ccr.to_message()
        
            

if __name__ == '__main__':
    unittest.main()