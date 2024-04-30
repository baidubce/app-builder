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


class Response:
    def __init__(self,headers=None,status_code=None,text=None):
        self.status_code=status_code
        self.headers=headers
        self.text = text
    
    def json(self):
        return json.loads(self.text)
        
        

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestCoreConsoleBase(unittest.TestCase):
    def test_ConsoleLLMMessage_init(self):
        clm=str(ConsoleLLMMessage())
        assert isinstance(clm,str),f"Expected {clm}, got {str}"
        
    
    def test_ConsoleCompletionResponse_init_3(self): 
        # stream=False test and response.status_code == 200
        response=Response(
            headers={"X-Appbuilder-Request-Id":"test_id"},
            status_code=200,
            text=json.dumps({
                "code": "test_code",
                'message': "test_message"
                })
            )
        with self.assertRaises(AppBuilderServerException):
            ConsoleCompletionResponse(response=response,stream=False) 
        
        
    # def test_ConsoleCompletionResponse_init_6(self):    
    #     response=Response(
    #         headers={"X-Appbuilder-Request-Id":"test_id"},
    #         status_code=200,
    #         text=json.dumps({
    #             "code": 0,
    #             'message':"test_message",
    #             'requestId':"test_requestId",
    #             'status':"test_status"
    #             'result'
    #             })
    #         )
    #     ConsoleCompletionResponse(response=response,stream=False)
        
        
    
    
    # def test_ConsoleCompletionResponse_to_message(self):
         
          

if __name__ == '__main__':
    unittest.main()