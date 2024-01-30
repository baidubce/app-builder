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


"""Base client for interact with backend server"""

import os
from typing import Optional

import requests
from requests.adapters import HTTPAdapter, Retry

from appbuilder.core._exception import *
from appbuilder.core.constants import GATEWAY_URL


class HTTPClient:
    r"""HTTPClient类,实现与后端服务交互的公共方法"""

    def __init__(self,
                 secret_key: Optional[str] = None,
                 gateway: str = ""
                 ):
        r"""HTTPClient初始化方法.

            参数:
                secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
                gateway(str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            返回：
                无
        """
        self.secret_key = secret_key if secret_key else os.getenv("APPBUILDER_TOKEN", "")
        if not self.secret_key:
            raise ValueError("secret_key is empty, please pass a nonempty secret_key "
                             "or set a secret_key in environment variable")
        if not self.secret_key.startswith("Bearer"):
            self.secret_key = "Bearer {}".format(self.secret_key)

        if not gateway and not os.getenv("GATEWAY_URL"):
            self.gateway = GATEWAY_URL
        else:
            self.gateway = gateway if gateway else os.getenv("GATEWAY_URL", "")

        if not self.gateway.startswith("http"):
            self.gateway = "https://" + self.gateway
        self.session = requests.sessions.Session()
        self.retry = Retry(total=0, backoff_factor=0.1)
        self.session.mount(self.gateway, HTTPAdapter(max_retries=self.retry))

    @staticmethod
    def check_response_header(response: requests.Response):
        r"""check_response_header is a helper method for check head status .
            :param response: requests.Response.
            :rtype:
        """
        status_code = response.status_code
        if status_code == requests.codes.ok:
            return
        message = "request_id={} , http status code is {}, body is {}".format(
            __class__.response_request_id(response), status_code, response.text)
        if status_code == requests.codes.bad_request:
            raise BadRequestException(message)
        elif status_code == requests.codes.forbidden:
            raise ForbiddenException(message)
        elif status_code == requests.codes.not_found:
            raise NotFoundException(message)
        elif status_code == requests.codes.precondition_required:
            raise PreconditionFailedException(message)
        elif status_code == requests.codes.internal_server_error:
            raise InternalServerErrorException(message)
        else:
            raise BaseRPCException(message)

    def service_url(self, sub_path: str, prefix: str = None):
        r"""service_url is a helper method for concatenate service url.
            :param sub_path: service unique sub path.
            :param prefix: service prefix.
            :rtype: str.
         """
        # host + fix prefix + sub service path
        prefix = prefix if prefix else "/rpc/2.0/cloud_hub"
        return self.gateway + prefix + sub_path

    @staticmethod
    def check_response_json(data: dict):
        r"""check_response_json is a helper method for check backend server response.
            :param: dict, body response data.
            :rtype: str.
        """
        if "code" in data and "message" in data and "requestId" in data:
            raise AppBuilderServerException(data["requestId"], data["code"], data["message"])

    @staticmethod
    def check_console_response(response: requests.Response):
        r"""check_console_response is a helper method for console check backend server response.
            :param: dict, body response data.
            :rtype: str.
        """
        data = response.json()
        if "code" in data and data.get("code") != 0:
            requestId = __class__.response_request_id(response)
            raise AppBuilderServerException(requestId, data["code"], data["message"])

    def auth_header(self):
        r"""auth_header is a helper method return auth info"""
        return {"X-Appbuilder-Authorization": self.secret_key}

    @staticmethod
    def response_request_id(response: requests.Response):
        r"""response_request_id is a helper method get unique request id"""
        return response.headers.get("X-Appbuilder-Request-Id", "")

    @staticmethod
    def check_param(func):
        def inner(*args, **kwargs):
            retry = kwargs.get("retry", 0)
            if retry < 0 or not isinstance(retry, int):
                raise InvalidRequestArgumentError("retry must be int and bigger then zero")
            timeout = kwargs.get("timeout", None)
            if timeout and not (isinstance(timeout, float) or isinstance(timeout, tuple)):
                raise InvalidRequestArgumentError("timeout must be float or tuple of float")
            return func(*args, **kwargs)

        return inner
