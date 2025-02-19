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
from appbuilder.core._client import HTTPClient

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


    def test_check_response(self):
        from appbuilder.core.components.v2 import Translation
        from appbuilder.core.components.translate.model import TranslateRequest, TranslateResponse
        import json
        class TestClass(Translation):
            def _translate(self, request: TranslateRequest, timeout: float = None,
                   retry: int = 0, request_id: str = None) -> TranslateResponse:
                """
                根据提供的 TranslateRequest 执行文本翻译。

                Args:
                    request (TranslateRequest): 翻译请求参数。
                    timeout (float, optional): 请求超时时间。
                    retry (int, optional): 重试次数。

                Returns:
                    TranslateResponse: 文本翻译结果的响应体。
                """
                if not request.to_lang or not request.q:
                    raise ValueError("params `to_lang` and `q` must be set")
                if not request.from_lang:
                    request.from_lang = "auto"
                request_data = TranslateRequest.to_json(request)
                if retry != self.http_client.retry.total:
                    self.http_client.retry.total = retry
                headers = self.http_client.auth_header(request_id)
                headers['content-type'] = 'application/json;charset=utf-8'

                url = self.http_client.service_url("/v1/bce/aip/mt/texttrans/v1")

                response = self.http_client.session.post(url, headers=headers, data=request_data, timeout=timeout)

                self.http_client.check_response_header(response)
                data = response.json()
                request_id = self.http_client.response_request_id(response)
                self.http_client.check_response_json(data)
                if "error_code" in data and "error_msg" in data:
                    raise AppBuilderServerException(request_id=request_id, service_err_code=data["error_code"],
                                                    service_err_message=data["error_msg"])

                json_str = json.dumps(data)
                return TranslateResponse(TranslateResponse.from_json(json_str)), data

        obj = TestClass()
        result = obj.tool_eval(q="你好", to_lang="en")
        for res in result:
            assert isinstance(res, ComponentOutput)

if __name__ == "__main__":
    unittest.main()