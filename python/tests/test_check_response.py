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
from unittest.mock import patch, MagicMock
import requests
import appbuilder
from appbuilder.core._exception import *
from appbuilder.core.component import ComponentOutput
from appbuilder.core._client import HTTPClient, AsyncHTTPClient

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestErrorHandle(unittest.TestCase):
    def test_MethodNotAllowedException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.method_not_allowed
        response.text = "MethodNotAllowed occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(MethodNotAllowedException) as context:
            client.check_response_header(response)


    def test_ConflictException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.conflict
        response.text = "Conflict occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(ConflictException) as context:
            client.check_response_header(response)

    def test_MissingContentLengthException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.length_required
        response.text = "MissingContentLength occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(MissingContentLengthException) as context:
            client.check_response_header(response)

    def test_UnprocessableEntityException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.unprocessable_entity
        response.text = "UnprocessableEntity occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(UnprocessableEntityException) as context:
            client.check_response_header(response)

    def test_DependencyFailedException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.failed_dependency
        response.text = "DependencyFailed occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(DependencyFailedException) as context:
            client.check_response_header(response)

    def test_TooManyRequestsException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.too_many_requests
        response.text = "TooManyRequests occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(TooManyRequestsException) as context:
            client.check_response_header(response)


    def test_InsufficientStorageException(self):
        # 创建一个模拟的Response对象
        client = HTTPClient()
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.insufficient_storage
        response.text = "InsufficientStorage occurred"
        response.headers = client.auth_header()

        # 模拟check_response_header方法
        with patch('appbuilder.core._client.HTTPClient.check_response_header') as mock_check:
            mock_check.return_value = None

        # 初始化HTTPClient
        client = HTTPClient()

        # 尝试调用check_response_header方法，并捕获抛出的异常
        with self.assertRaises(InsufficientStorageException) as context:
            client.check_response_header(response)

    def test_classify_exception(self):
        """测试异常分类方法"""
        client = HTTPClient()
        
        # 测试 HTTP 错误
        response = MagicMock(spec=requests.Response)
        response.status_code = requests.codes.internal_server_error
        response.text = "Internal Server Error"
        response.headers = client.auth_header()
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


    async def test_AsyncHTTPClient_classify_exception(self):
        """测试异常分类方法"""
        client = AsyncHTTPClient()
        # 测试 HTTP 错误
        response = MagicMock(spec=requests.AsyncResponse)
        response.status_code = requests.codes.internal_server_error
        response.text = "Internal Server Error"
        response.headers = client.auth_header()
        http_error = requests.exceptions.HTTPError(response=response)
        
        with self.assertRaises(InternalServerErrorException):
            await client.classify_exception(http_error)
        
        # 测试 AppBuilder 服务器异常
        app_error = AppBuilderServerException(
            request_id="test_id",
            code=500,
            message="Interal Server Error"
        )
        
        with self.assertRaises(AppBuilderServerException) as context:
            await client.classify_exception(app_error)
        
        self.assertEqual(context.exception.code, 500)
        
        # 测试其他类型异常
        other_error = ValueError("Test error")
        
        with self.assertRaises(InternalServerException) as context:
            await client.classify_exception(other_error)
        
        self.assertEqual(str(context.exception), "Test error")

if __name__ == "__main__":
    unittest.main()