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


"""include HTTP and backend server exception.
"""


class BaseRPCException(Exception):
    r"""Base RPC exception.
    """
    pass


class BadRequestException(BaseRPCException):
    r""" BadRequestException represent HTTP Code 400.
    """
    pass


class ForbiddenException(BaseRPCException):
    r"""BadRequestException represent HTTP Code 403.
    """
    pass


class NotFoundException(BaseRPCException):
    r"""NotFoundException represent HTTP Code 404.
    """
    pass


class PreconditionFailedException(BaseRPCException):
    r"""PreconditionFailedException represent HTTP Code 412.
    """
    pass


class InternalServerErrorException(BaseRPCException):
    r"""InternalServerErrorException represent HTTP Code 500.
    """
    pass


class HTTPConnectionException(BaseRPCException):
    r"""HTTPConnectionException represent HTTP Connection error.
    """
    pass


class ModelNotSupportedException(BaseRPCException):
    r"""ModelNotSupportedException represent model is not supported
    """
    pass


class TypeNotSupportedException(BaseRPCException):
    r"""TypeNotSupportedException represent type is not supported
    """
    pass


class AppBuilderServerException(BaseRPCException):
    r"""AppBuilderServerException represent backend server failed response.
    """
    description: str = "Interal Server Error"
    code: int = 500

    def __init__(self, request_id="", code="", message="", service_err_code="", service_err_message=""):
        self.description = "request_id={}, code={}, message={}, service_err_code={}, service_err_message={} ".format(
            request_id, code, message, service_err_code, service_err_message)
        self.code = code if code else self.code

    def __str__(self):
        return self.description

class AssistantServerException(BaseRPCException):
    r"""AssistantSercerException represent assistant server failed response.
    """
    description: str = "Interal Server Error"
    code: int = 500

    def __init__(self, request_id= "", code="", message="", type="", params=""):
        self.description = "request_id={}, code={}, message={}, type={}, params={} ".format(
            request_id, code, message, type, params)
        self.code = code if code else self.code

    def __str__(self):
        return self.description


class InvalidRequestArgumentError(BaseRPCException):
    r"""InvalidRequestArgumentError invalid request param
    """
    pass


class RiskInputException(BaseRPCException):
    r"""RiskInputException
    """
    pass
