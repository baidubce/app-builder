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

"""Component module include a Component class which is the
base class for customized Component class, define interface method like run() batch() etc.
subclass may choose to implement, also  provide some simple helper method for interact with backend server."""

import os
from enum import Enum

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter, Retry
from typing import Dict, List, Optional, Any

from appbuilder.core._exception import *
from appbuilder.core.message import Message
from appbuilder.core.constants import GATEWAY_URL


class ComponentArguments(BaseModel):
    r""""ComponentArguments define Component meta fields"""
    name: str = ""
    tool_desc: Dict[str, Any] = {}

    def extract_values_to_dict(self):
        r"""extract ComponentArguments fields to dict"""

        inputs = {}
        for field_name, field in self.__fields__.items():
            value = getattr(self, field_name)
            # 获取 display_name 元数据
            variable_name = field.field_info.extra.get('variable_name')
            if variable_name:
                # 使用 Enum 成员的实际值
                if isinstance(value, Message):
                    inputs[variable_name] = str(value.content)
                elif isinstance(value, Enum):
                    inputs[variable_name] = str(value.value)
                else:
                    inputs[variable_name] = str(value)
            else:
                inputs[field_name] = value
        return inputs


class Component:
    r"""Component基类, 其它实现的Component子类需要继承该基类，并至少实现run方法."""

    def __init__(self,
                 meta: Optional[ComponentArguments] = ComponentArguments(),
                 secret_key: Optional[str] = None,
                 gateway: str = ""
                 ):
        r"""Component初始化方法.

            参数:
                meta (obj: `ComponentArguments`, 可选) : component元信息.
                secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
                gateway(str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            返回：
                无
        """
        self.meta = meta
        self.secret_key = secret_key if secret_key else os.getenv("APPBUILDER_TOKEN", "")
        if not self.secret_key:
            raise ValueError("secret_key is empty, please pass a nonempty secret_key "
                             "or set a secret_key in environment variable")

        if not gateway and not os.getenv("GATEWAY_URL"):
            self.gateway = GATEWAY_URL
        else:
            self.gateway = gateway if gateway else os.getenv("GATEWAY_URL", "")

        if not self.gateway.startswith("http"):
            self.gateway = "https://" + self.gateway
        self.s = requests.sessions.Session()
        self.retry = Retry(total=0, backoff_factor=0.1)
        self.s.mount(self.gateway, HTTPAdapter(max_retries=self.retry))

    def __call__(self, *inputs, **kwargs):
        r"""implement __call__ method"""
        return self.run(*inputs, **kwargs)

    def run(self, *inputs, **kwargs):
        r"""
        Defines the computation performed at every call.
        Should be overridden by all subclasses.

        Parameters:
            *inputs(tuple): unpacked tuple arguments
            **kwargs(dict): unpacked dict arguments
        """
        raise NotImplementedError

    def batch(self, *args, **kwargs) -> List[Message]:
        r"""pass"""
        return None

    async def arun(self, *args, **kwargs) -> Optional[Message]:
        r"""pass"""
        return None

    async def abatch(self, *args, **kwargs) -> List[Message]:
        r"""pass"""
        return None

    def _trace(self, **data) -> None:
        r"""pass"""
        pass

    def _debug(self, **data) -> None:
        r"""pass"""
        pass

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

    def auth_header(self):
        r"""auth_header is a helper method return auth info"""

        if self.secret_key.startswith("Bearer "):
            return {"X-Appbuilder-Authorization": self.secret_key}
        else:
            return {"X-Appbuilder-Authorization": "Bearer {}".format(self.secret_key)}

    @staticmethod
    def response_request_id(response: requests.Response):
        r"""response_request_id is a helper method get unique request id"""
        return response.headers.get("X-Appbuilder-Request-Id", "")
