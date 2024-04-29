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

"""Component模块包括组件基类，用户自定义组件需要继承Component类，并至少实现run方法"""
import json

from enum import Enum

from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from appbuilder.core.utils import ttl_lru_cache
from appbuilder.core._client import HTTPClient
from appbuilder.core.message import Message


class ComponentArguments(BaseModel):
    r""""ComponentArguments define Component meta fields"""
    name: str = ""
    tool_desc: Dict[str, Any] = {}

    def extract_values_to_dict(self):
        r"""extract ComponentArguments fields to dict"""

        inputs = {}
        for name, info in self.model_fields.items():
            value = getattr(self, name)
            # 获取 display_name 元数据
            if not info.json_schema_extra:
                continue
            variable_name = info.json_schema_extra.get('variable_name')
            if not variable_name:
                inputs[name] = value
                continue
            # 使用 Enum 成员的实际值
            if isinstance(value, Message):
                inputs[variable_name] = str(value.content)
            elif isinstance(value, Enum):
                inputs[variable_name] = str(value.value)
            else:
                inputs[variable_name] = str(value)
        return inputs


class Component:
    r"""Component基类, 其它实现的Component子类需要继承该基类，并至少实现run方法."""

    manifests = []

    def __init__(
        self,
        meta: Optional[ComponentArguments] = ComponentArguments(),
        secret_key: Optional[str] = None,
        gateway: str = "",
        lazy_certification: bool = False,
    ):
        r"""Component初始化方法.

            参数:
                meta (obj: `ComponentArguments`, 可选) : component元信息.
                secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
                gateway(str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
                lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
            返回：
                无
        """
        self.meta = meta
        self.secret_key = secret_key
        self.gateway = gateway
        self._http_client = None
        self.lazy_certification = lazy_certification
        if not self.lazy_certification:
            self.set_secret_key_and_gateway(self.secret_key, self.gateway)
 
    def set_secret_key_and_gateway(self, secret_key: Optional[str] = None, gateway: str = ""):
        self.secret_key = secret_key
        self.gateway = gateway
        self._http_client = HTTPClient(self.secret_key, self.gateway)

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = HTTPClient(self.secret_key, self.gateway)
        return self._http_client

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

    def tool_desc(self) -> List[str]:
        return [json.dumps(manifest, ensure_ascii=False) for manifest in self.manifests]

    def tool_name(self) -> List[str]:
        return [manifest["name"] for manifest in self.manifests]

    def tool_eval(self, **kwargs):
        if len(self.manifests) > 0:
            raise NotImplementedError
