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

from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import * 

# 创建一个response类,模拟requests.Response
class Response:
    def __init__(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text
        
    def json(self):
            return json.loads(self.text)

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestCoreClient(unittest.TestCase):
    def setUp(self):
        # 保存原始环境变量
        self.original_appbuilder_token = os.getenv('APPBUILDER_TOKEN')
        self.original_gateway_url = os.getenv('GATEWAY_URL')
    
    def tearDown(self):
        # 恢复环境变量
        if self.original_appbuilder_token is None:
            os.unsetenv('APPBUILDER_TOKEN')
        else:
            os.environ['APPBUILDER_TOKEN'] = self.original_appbuilder_token
        
        if self.original_gateway_url is None:
            os.unsetenv('GATEWAY_URL')
        else:
            os.environ['GATEWAY_URL'] = self.original_gateway_url
            
    def test_core_client_init_non_APPBUILDER_TOKEN(self):
        os.environ['APPBUILDER_TOKEN'] = ''
        with self.assertRaises(ValueError):
            HTTPClient()
            
    def test_core_client_init_non_GATEWAY_URL(self):
        os.environ['GATEWAY_URL'] = 'test'        
        hp=HTTPClient()
        assert hp.gateway.startswith('https://')
        
    def test_core_client_check_response_header(self):
        # 测试各种response报错
        response = Response(
            status_code=400,
            headers={'Content-Type': 'application/json'} , 
            text='{"code": 0, "message": "success"}'
            )
        with self.assertRaises(BadRequestException):
            HTTPClient.check_response_header(response)
        
        response.status_code = 403
        with self.assertRaises(ForbiddenException):
            HTTPClient.check_response_header(response)
        
        response.status_code = 404
        with self.assertRaises(NotFoundException):
            HTTPClient.check_response_header(response)
        
        response.status_code = 428
        with self.assertRaises(PreconditionFailedException):
            HTTPClient.check_response_header(response)
            
        response.status_code = 500
        with self.assertRaises(InternalServerErrorException):
            HTTPClient.check_response_header(response)
        
        response.status_code = 201
        with self.assertRaises(BaseRPCException):
            HTTPClient.check_response_header(response)
        
    def test_core_client_check_response_json(self):
        data={
            'code': 0,
            'message': 'test',
            'requestId':'test'
        } 
        with self.assertRaises(AppBuilderServerException):
            HTTPClient.check_response_json(data)
            
    def test_core_check_console_response(self):
        response = Response(
            status_code=400,
            headers={'Content-Type': 'application/json'} , 
            text=json.dumps({
                'code': 1,
                'message': 'test',
                'requestId':'test'
            })
            )
        with self.assertRaises(AppBuilderServerException):
            HTTPClient.check_console_response(response)
          
            
if __name__ == '__main__':
    unittest.main()
        