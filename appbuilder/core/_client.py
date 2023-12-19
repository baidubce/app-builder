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

import requests

from appbuilder.core._exception import *


class BaseClient:
    r"""
    BaseClient class provide common method for interact with backend server.
    """

    def __init__(self, secret_key: str = "", gateway: str = ""):
        r"""__init__ method.
            :param secret_key: authorization token, if not set get from env variable.
            :param gateway: backend server host.
            :rtype:
         """

        self.secret_key = secret_key if secret_key else os.getenv("APPBUILDER_TOKEN", "")

        if not self.secret_key:
            raise ValueError("secret_key is empty, please pass a nonempty secret_key "
                             "or set a secret_key in environment variable")

        self.gateway = gateway if gateway else os.getenv("GATEWAY_URL", "")

        # self.gateway = gateway or os.getenv("GATEWAY_URL", "https://api.xbuilder.baidu.com")
        if not self.gateway.startswith("http"):
            self.gateway = "https://" + gateway

    @staticmethod
    def check_response_header(response: requests.Response):
        r"""check_response_header is a helper method for check head status .
            :param response: requests.Response.
            :rtype:
        """
        status_code = response.status_code
        if status_code == requests.codes.ok:
            return
        request_id = response.headers.get("X-App-Engine-Request-Id", "")
        message = "request_id={} , http status code is {}".format(request_id, status_code)
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

    def service_url(self, sub_path: str, prefix=None):
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
