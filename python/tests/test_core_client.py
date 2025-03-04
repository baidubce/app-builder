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
import asyncio

from appbuilder.core._client import HTTPClient, AsyncHTTPClient
from appbuilder.core._exception import *

# 创建一个response类,模拟requests.Response


class Response:
    def __init__(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text

    def json(self):
        return json.loads(self.text)


class AsyncResponse:
    def __init__(self, status_code, headers, text):
        self.status = status_code
        self.headers = headers
        self.text = text

    def json(self):
        return json.loads(self.text)


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
        hp = HTTPClient()
        assert hp.gateway.startswith('https://')

    def test_core_client_check_response_header(self):
        # 测试各种response报错
        response = Response(
            status_code=400,
            headers={'Content-Type': 'application/json'},
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

        response.status_code = 401
        with self.assertRaises(UnAuthorizedException):
            HTTPClient.check_response_header(response)

        response.status_code = 405
        with self.assertRaises(MethodNotAllowedException):
            HTTPClient.check_response_header(response)

        response.status_code = 409
        with self.assertRaises(ConflictException):
            HTTPClient.check_response_header(response)

        response.status_code = 411
        with self.assertRaises(MissingContentLengthException):
            HTTPClient.check_response_header(response)

        response.status_code = 422
        with self.assertRaises(UnprocessableEntityException):
            HTTPClient.check_response_header(response)

        response.status_code = 424
        with self.assertRaises(DependencyFailedException):
            HTTPClient.check_response_header(response)

        response.status_code = 429
        with self.assertRaises(TooManyRequestsException):
            HTTPClient.check_response_header(response)

        response.status_code = 507
        with self.assertRaises(InsufficientStorageException):
            HTTPClient.check_response_header(response)

        import requests
        http_error = requests.exceptions.HTTPError(response=response)
        with self.assertRaises(InsufficientStorageException):
            HTTPClient.classify_exception(http_error)

    def test_core_client_check_async_response_header(self):
        async def run_test():
            # 测试各种response报错
            response = AsyncResponse(
                status_code=400,
                headers={'Content-Type': 'application/json'},
                text=lambda:asyncio.sleep(0) or '{"code": 0, "message": "success"}'
            )
            with self.assertRaises(BadRequestException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 403
            with self.assertRaises(ForbiddenException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 404
            with self.assertRaises(NotFoundException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 428
            with self.assertRaises(PreconditionFailedException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 500
            with self.assertRaises(InternalServerErrorException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 201
            with self.assertRaises(BaseRPCException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 401
            with self.assertRaises(UnAuthorizedException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 405
            with self.assertRaises(MethodNotAllowedException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 409
            with self.assertRaises(ConflictException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 411
            with self.assertRaises(MissingContentLengthException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 422
            with self.assertRaises(UnprocessableEntityException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 424
            with self.assertRaises(DependencyFailedException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 429
            with self.assertRaises(TooManyRequestsException):
                await AsyncHTTPClient.check_response_header(response)

            response.status = 507
            with self.assertRaises(InsufficientStorageException):
                await AsyncHTTPClient.check_response_header(response)

            import requests
            http_error = requests.exceptions.HTTPError(response=response)
            with self.assertRaises(InsufficientStorageException):
                await AsyncHTTPClient.classify_exception(http_error)
            
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_test())

    def test_core_client_check_response_json(self):
        data = {
            'code': 0,
            'message': 'test',
            'requestId': 'test'
        }
        with self.assertRaises(AppBuilderServerException):
            HTTPClient.check_response_json(data)

    def test_core_check_console_response(self):
        response = Response(
            status_code=400,
            headers={'Content-Type': 'application/json'},
            text=json.dumps({
                'code': 1,
                'message': 'test',
                'requestId': 'test'
            })
        )
        with self.assertRaises(AppBuilderServerException):
            HTTPClient.check_console_response(response)

    def test_classify_exception(self):
        """测试异常分类方法"""
        import requests
        client = HTTPClient()
        
        # 测试 HTTP 错误
        response = Response(
            status_code=requests.codes.internal_server_error,
            headers=client.auth_header(),
            text="Internal Server Error"
        )
        http_error = requests.exceptions.HTTPError(response=response)
        
        with self.assertRaises(InternalServerErrorException):
            client.classify_exception(http_error)
        
        # 测试 AppBuilder 服务器异常
        app_error = AppBuilderServerException(
            request_id="test_id",
            code=500,
            message="Interal Server Error"
        )
        
        with self.assertRaises(AppBuilderServerException) as context:
            client.classify_exception(app_error)
        
        self.assertEqual(context.exception.code, 500)
        
        # 测试其他类型异常
        other_error = ValueError("Test error")
        
        with self.assertRaises(InternalServerException) as context:
            client.classify_exception(other_error)
        
        self.assertEqual(str(context.exception), "Test error")


    def test_AsyncHTTPClient_classify_exception(self):
        """测试异常分类方法"""
        async def run_test():
            import requests
            client = AsyncHTTPClient()
            # 测试 HTTP 错误
            response = AsyncResponse(
                status_code=requests.codes.internal_server_error,
                headers=client.auth_header(),
                text=lambda:asyncio.sleep(0) or '{"code": 0, "message": "success"}'
            )
            http_error = requests.exceptions.HTTPError(response=response)
            
            with self.assertRaises(InternalServerErrorException):
                await client.classify_exception(http_error)
            
            # 测试 AppBuilder 服务器异常
            app_error = AppBuilderServerException(
                request_id="test_id",
                code="500",
                message="Interal Server Error"
            )
            
            with self.assertRaises(AppBuilderServerException) as context:
                await client.classify_exception(app_error)
            
            self.assertEqual(context.exception.code, "500")
            
            # 测试其他类型异常
            other_error = ValueError("Test error")
            
            with self.assertRaises(InternalServerException) as context:
                await client.classify_exception(other_error)
            
            self.assertEqual(str(context.exception), "Test error")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
