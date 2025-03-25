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
import uuid
from typing import Optional

import requests
from requests.adapters import HTTPAdapter, Retry
from aiohttp import ClientResponse

from appbuilder.utils.logger_util import logger
from appbuilder import get_default_header

from appbuilder.core._exception import *
from appbuilder.core._session import InnerSession, AsyncInnerSession
from appbuilder.core.constants import (
    GATEWAY_URL,
    GATEWAY_URL_V2,
    CONSOLE_OPENAPI_VERSION,
    CONSOLE_OPENAPI_PREFIX,
    SECRET_KEY_PREFIX,
)
from appbuilder.utils.logger_util import logger


class HTTPClient:
    r"""HTTPClient类,实现与后端服务交互的公共方法"""

    def __init__(
        self, secret_key: Optional[str] = None, gateway: str = "", gateway_v2: str = ""
    ):
        r"""HTTPClient初始化方法.

        参数:
            secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway(str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            gateway_v2(str, 可选): 后端OpenAPI网关服务地址，当前仅AgentBuilder使用。默认从环境变量中获取: os.getenv("GATEWAY_URL_V2", "")
        返回：
            无
        """
        self._init_secret_key(secret_key)

        # Component
        self._init_gateway_url(gateway)

        # Console OpenAPI
        self._init_gateway_url_v2(gateway_v2)

        self.session = InnerSession()
        self.retry = Retry(total=0, backoff_factor=0.1)
        self.session.mount(self.gateway, HTTPAdapter(max_retries=self.retry))

    def _init_gateway_url(self, gateway: str):
        if not gateway and not os.getenv("GATEWAY_URL"):
            self.gateway = GATEWAY_URL
        else:
            self.gateway = gateway if gateway else os.getenv("GATEWAY_URL", "")
        if not self.gateway.startswith("http"):
            self.gateway = "https://" + self.gateway

    def _init_gateway_url_v2(self, gateway_v2: str):
        if not gateway_v2 and not os.getenv("GATEWAY_URL_V2"):
            self.gateway_v2 = GATEWAY_URL_V2
        else:
            self.gateway_v2 = (
                gateway_v2 if gateway_v2 else os.getenv("GATEWAY_URL_V2", "")
            )
        if not self.gateway_v2.startswith("http"):
            self.gateway_v2 = "https://" + self.gateway_v2

        self.console_openapi_verion = os.getenv(
            "CONSOLE_OPENAPI_VERSION", CONSOLE_OPENAPI_VERSION
        )
        self.console_openapi_prefix = os.getenv(
            "CONSOLE_OPENAPI_PREFIX", CONSOLE_OPENAPI_PREFIX
        )

    def _init_secret_key(self, secret_key: str):
        self.secret_key = (
            secret_key if secret_key else os.getenv("APPBUILDER_TOKEN", "")
        )
        if not self.secret_key:
            raise ValueError(
                "secret_key is empty, please pass a nonempty secret_key "
                'or set a secret_key in environment variable "APPBUILDER_TOKEN"'
            )
        secret_key_prefix = os.getenv("SECRET_KEY_PREFIX", SECRET_KEY_PREFIX)

        if not self.secret_key.startswith(secret_key_prefix):
            self.secret_key = "{} {}".format(
                secret_key_prefix, self.secret_key)

        logger.debug("AppBuilder Secret key: {}\n".format(self.secret_key))

    @staticmethod
    def check_response_header(response: requests.Response):
        r"""check_response_header is a helper method for check head status .
        :param response: requests.Response.
        :rtype:
        """
        status_code = response.status_code
        if status_code == requests.codes.ok:
            response_headers = "\n\t".join([f"{key} : {value}" for key, value in response.headers.items()])
            message = "\nrequest_id : {} \nhttp status : {}\nresponse headers : \n\t{}".format(
                __class__.response_request_id(response), status_code, response_headers
            )
            logger.debug(message)
            return
        message = "request_id={} , http status code is {}, body is {}".format(
            __class__.response_request_id(response), status_code, response.text
        )
        if status_code == requests.codes.bad_request:
            logger.error(message)
            raise BadRequestException(message)
        elif status_code == requests.codes.unauthorized:
            logger.error(message)
            raise UnAuthorizedException(message)
        elif status_code == requests.codes.forbidden:
            logger.error(message)
            raise ForbiddenException(message)
        elif status_code == requests.codes.not_found:
            logger.error(message)
            raise NotFoundException(message)
        elif status_code == requests.codes.method_not_allowed:
            logger.error(message)
            raise MethodNotAllowedException(message)
        elif status_code == requests.codes.conflict:
            logger.error(message)
            raise ConflictException(message)
        elif status_code == requests.codes.length_required:
            logger.error(message)
            raise MissingContentLengthException(message)
        elif status_code == requests.codes.precondition_required:
            logger.error(message)
            raise PreconditionFailedException(message)
        elif status_code == requests.codes.unprocessable_entity:
            logger.error(message)
            raise UnprocessableEntityException(message)
        elif status_code == requests.codes.failed_dependency:
            logger.error(message)
            raise DependencyFailedException(message)
        elif status_code == requests.codes.too_many_requests:
            logger.error(message)
            raise TooManyRequestsException(message)
        elif status_code == requests.codes.internal_server_error:
            logger.error(message)
            raise InternalServerErrorException(message)
        elif status_code == requests.codes.insufficient_storage:
            logger.error(message)
            raise InsufficientStorageException(message)
        else:
            logger.error(message)
            raise BaseRPCException(message)

    def service_url(self, sub_path: str, prefix: str = None):
        r"""service_url is a helper method for concatenate service url.
        :param sub_path: service unique sub path.
        :param prefix: service prefix.
        :rtype: str.
        """
        # host + fix prefix + sub service path
        prefix = prefix if prefix else "/rpc/2.0/cloud_hub"
        final_url = self.gateway + prefix + sub_path
        logger.debug("Service url: {}\n".format(final_url))
        return final_url

    def service_url_v2(self, sub_path: str, client_token: str = None):
        r"""service_url is a helper method for concatenate service url for OpenAPI, only used by AppBuilderClient.
        :param sub_path: service unique sub path.
        :rtype: str.
        """
        # console_prefix =
        final_url = (
            self.gateway_v2
            + self.console_openapi_prefix
            + self.console_openapi_verion
            + sub_path
        )
        if client_token:
            if "?" in final_url:
                final_url += "&clientToken=" + client_token
            else:
                final_url += "?clientToken=" + client_token
        logger.debug("Service url: {}\n".format(final_url))
        return final_url

    @staticmethod
    def check_response_json(data: dict):
        r"""check_response_json is a helper method for check backend server response.
        :param: dict, body response data.
        :rtype: str.
        """
        if "code" in data and "message" in data and "requestId" in data:
            raise AppBuilderServerException(
                data["requestId"], data["code"], data["message"]
            )

    @staticmethod
    def check_console_response(response: requests.Response):
        r"""check_console_response is a helper method for console check backend server response.
        :param: dict, body response data.
        :rtype: str.
        """
        data = response.json()
        if "code" in data and data.get("code") != 0:
            requestId = __class__.response_request_id(response)
            raise AppBuilderServerException(
                requestId, data["code"], data["message"])

    def auth_header(self, request_id: Optional[str] = None):
        r"""auth_header is a helper method return auth info"""
        auth_header = get_default_header()
        new_request_id = str(uuid.uuid4())
        auth_header["X-Appbuilder-Request-Id"] = (
            request_id if request_id else new_request_id
        )
        auth_header["X-Bce-Request-Id"] = request_id if request_id else new_request_id
        auth_header["X-Appbuilder-Authorization"] = self.secret_key
        logger.debug("Request header: {}\n".format(auth_header))
        return auth_header

    def auth_header_v2(self, request_id: Optional[str] = None, mcp_context = None):
        r"""auth_header_v2 is a helper method return auth info for OpenAPI, only used by AppBuilderClient"""
        auth_header = get_default_header(mcp_context)
        new_request_id = str(uuid.uuid4())
        auth_header["X-Appbuilder-Request-Id"] = (
            request_id if request_id else new_request_id
        )
        auth_header["X-Bce-Request-Id"] = request_id if request_id else new_request_id
        auth_header["Authorization"] = self.secret_key
        logger.debug("Request header: {}\n".format(auth_header))
        return auth_header

    @staticmethod
    def response_request_id(response: requests.Response):
        r"""response_request_id is a helper method get unique request id"""
        return response.headers.get("X-Appbuilder-Request-Id", "")

    @staticmethod
    def check_param(func):
        def inner(*args, **kwargs):
            retry = kwargs.get("retry", 0)
            if retry < 0 or not isinstance(retry, int):
                raise InvalidRequestArgumentError(
                    'Rqeuest argument "retry" format error. Expected retry >=0. Got {}'.format(
                        retry
                    )
                )
            timeout = kwargs.get("timeout", None)
            if timeout and not (
                isinstance(timeout, float) or isinstance(timeout, tuple)
            ):
                raise InvalidRequestArgumentError(
                    'Request argument "timeout" format error, Expected timeout be float or tuple of float'
                )
            return func(*args, **kwargs)

        return inner

    @staticmethod
    def classify_exception(e):
        """classify exception type and raise"""
        from requests.exceptions import HTTPError
        
        # 定义需要直接抛出的异常类型列表
        custom_exceptions = (
            AppBuilderServerException,
            NoFileUploadedExecption,
            InvalidRequestArgumentError,
            RetryableExecption,
            RiskInputException,
            InternalServerException,
            AssistantServerException
        )
        
        if isinstance(e, HTTPError):
            __class__.check_response_header(e.response)
        elif isinstance(e, custom_exceptions):  # 检查异常是否属于自定义的类型
            raise e
        else: #未定义的错误使用InternalServerException兜底
            raise InternalServerException(str(e))


class AsyncHTTPClient(HTTPClient):
    def __init__(self, secret_key=None, gateway="", gateway_v2=""):
        super().__init__(secret_key, gateway, gateway_v2)
        self.session = AsyncInnerSession()

    @staticmethod
    async def check_response_header(response: ClientResponse):
        r"""check_response_header is a helper method for check head status .
        :param response: requests.Response.
        :rtype:
        """
        status_code = response.status
        if status_code == requests.codes.ok:
            return
        message = "request_id={} , http status code is {}, body is {}".format(
            await __class__.response_request_id(response), status_code, await response.text()
        )
        if status_code == requests.codes.bad_request:
            logger.error(message)
            raise BadRequestException(message)
        elif status_code == requests.codes.unauthorized:
            logger.error(message)
            raise UnAuthorizedException(message)
        elif status_code == requests.codes.forbidden:
            logger.error(message)
            raise ForbiddenException(message)
        elif status_code == requests.codes.not_found:
            logger.error(message)
            raise NotFoundException(message)
        elif status_code == requests.codes.method_not_allowed:
            logger.error(message)
            raise MethodNotAllowedException(message)
        elif status_code == requests.codes.conflict:
            logger.error(message)
            raise ConflictException(message)
        elif status_code == requests.codes.length_required:
            logger.error(message)
            raise MissingContentLengthException(message)
        elif status_code == requests.codes.precondition_required:
            logger.error(message)
            raise PreconditionFailedException(message)
        elif status_code == requests.codes.unprocessable_entity:
            logger.error(message)
            raise UnprocessableEntityException(message)
        elif status_code == requests.codes.failed_dependency:
            logger.error(message)
            raise DependencyFailedException(message)
        elif status_code == requests.codes.too_many_requests:
            logger.error(message)
            raise TooManyRequestsException(message)
        elif status_code == requests.codes.internal_server_error:
            logger.error(message)
            raise InternalServerErrorException(message)
        elif status_code == requests.codes.insufficient_storage:
            logger.error(message)
            raise InsufficientStorageException(message)
        else:
            logger.error(message)
            raise BaseRPCException(message)

    @staticmethod
    async def response_request_id(response: ClientResponse):
        r"""response_request_id is a helper method to get the unique request id"""
        return response.headers.get("X-Appbuilder-Request-Id", "")

    @staticmethod
    async def classify_exception(e):
        """classify exception type and raise"""
        from requests.exceptions import HTTPError
        # 定义需要直接抛出的异常类型列表
        custom_exceptions = (
            AppBuilderServerException,
            NoFileUploadedExecption,
            InvalidRequestArgumentError,
            RetryableExecption,
            RiskInputException,
            InternalServerException,
            AssistantServerException
        )
        
        if isinstance(e, HTTPError):
            await __class__.check_response_header(e.response)
        elif isinstance(e, custom_exceptions):  # 检查异常是否属于自定义的类型
            raise e
        else: #未定义的错误使用InternalServerException兜底
            raise InternalServerException(str(e))

class AssistantHTTPClient(HTTPClient):
    def service_url(self, sub_path: str, prefix: str = None):
        """
        根据给定的子路径和前缀，返回完整的服务URL。

        Args:
            sub_path (str): 子路径，例如 "/api/v1/user"。
            prefix (str, optional): URL前缀，例如 "http://example.com"。默认为None。

        Returns:
            str: 完整的服务URL，例如 "http://example.com/api/v1/user"。
        """
        prefix = prefix if prefix else ""
        return self.gateway + prefix + sub_path

    def auth_header(self, request_id: Optional[str] = None):
        """
        返回一个包含认证信息的字典

        Args:
            无参数。
        """
        r"""auth_header is a helper method return auth info"""
        auth_header = get_default_header()
        auth_header["Authorization"] = self.secret_key
        new_request_id = str(uuid.uuid4())
        auth_header["X-Appbuilder-Request-Id"] = (
            request_id if request_id else new_request_id
        )
        auth_header["X-Bce-Request-Id"] = request_id if request_id else new_request_id
        auth_header["X-Appbuilder-Authorization"] = self.secret_key
        auth_header["Content-Type"] = "application/json"
        logger.debug("Request header: {}\n".format(auth_header))
        return auth_header

    @staticmethod
    def check_assistant_response(request_id, data):
        """
        检查助手的响应结果，如果返回了错误信息，则抛出 AssistantServerException 异常。

        Args:
            request_id (str): 请求 ID。
            data (dict): 助手返回的响应数据。

        Returns:
            None

        Raises:
            AssistantServerException: 如果助手返回了错误信息，则抛出该异常。

        """
        if "error" in data:
            raise AssistantServerException(
                request_id=request_id,
                code=data["error"]["code"],
                message=data["error"]["message"],
                type=data["error"]["type"],
                params=(
                    data["error"]["param"]
                    if "param" in data["error"]
                    else data["error"]["params"]
                ),
            )