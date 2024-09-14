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

    def create_langchain_tool(self, tool_name="", **kwargs):
        try:
            from langchain_core.tools import StructuredTool
        except ImportError:
            raise ImportError(
                "Please install langchain to use create_langchain_tool.")
        
        # NOTE(chengmo): 可以支持LangChain的组件，必须要求具备mainfest
        if self.manifests == []:
            raise ValueError("Compnent {} No manifests found. Cannot convert it into LangChain Tool".format(type(self)))

        langchain_tool_json_schema = {}
        # NOTE(chengmo): 虽然现阶段，组件的mainfest列表中最多只有一个元素，但是需要兼容后期可能的多Tool的情况
        if len(self.manifests) > 1:
            if tool_name == "":
                raise ValueError("Multiple tools found, please use 'tool_name' specify which one to use.")

            for manifest in self.manifests:
                if manifest["name"] == tool_name:
                    langchain_tool_json_schema = manifest
                    break
            
            if langchain_tool_json_schema == {}:
                raise ValueError("Tool {} not found in mainfest.".format(tool_name))
        else:
            langchain_tool_json_schema = self.manifests[0]

        # NOTE(chengmo): 当前AB-SDK的Tool有两种情况
        # 1、存在tool_eval方法，则直接调用tool_eval方法，并设置stream=True, 汇总结果，封装成Message返回
        # 2、不存在tool_eval方法，则调用run方法，并设置 stream=False, 封装成Message返回
        has_tool_eval = self._has_implemented_tool_eval()
        langchain_tool_func = None
        if has_tool_eval:
            langchain_tool_func = self._langchain_tool_eval_implement
        else:
            langchain_tool_func = self._langchain_run_implement

        # NOTE(chengmo): name 及 description 都从mainfest中获取
        langchain_tool_name = langchain_tool_json_schema["name"]
        langchain_tool_description = langchain_tool_json_schema["description"]

        # NOTE(chengmo): 从mainfest中获取参数的json_schema，并转换成Pydantic的BaseModel
        from appbuilder.utils.json_schema_to_model import json_schema_to_pydantic_model
        try:
            import copy
            schema = copy.deepcopy(langchain_tool_json_schema["parameters"])
            schema["title"] = langchain_tool_name
            langchain_tool_model = json_schema_to_pydantic_model(
                schema,
                name_override=langchain_tool_name)
        except Exception as e:
            raise RuntimeError("Failed to generate Pydantic model for tool schema: {}".format(e))

        return StructuredTool.from_function(
            func=langchain_tool_func,
            name=langchain_tool_name,
            description=langchain_tool_description,
            args_schema=langchain_tool_model,
            return_direct=False
        )
    
    def _has_implemented_tool_eval(self):
        has_tool_eval = False
        try:
            # 调用self.tool_eval方法，如果抛出NotImplementedError异常，则说明没有实现tool_eval方法
            self.tool_eval(**{'name':"", "streaming":False})
        except NotImplementedError:
            has_tool_eval = False
        else:
            has_tool_eval = True
        
        return has_tool_eval

    def _langchain_run_implement(self, **kwargs):
        # NOTE(chengmo): 调用run方法，并设置 stream=False, 封装成Message返回
        kwargs["stream"] = False
        return self.run(**kwargs)

    def _langchain_tool_eval_implement(self, **kwargs):
        # NOTE(chengmo): 调用tool_eval方法，并设置 stream=True, 封装成Message返回
        kwargs["stream"] = True
        kwargs["streaming"] = True
        res = self.tool_eval(**kwargs)

        final_result = ""
        
        # TODO(chengmo): 在组件标准化管理前，复用DTE对流式组件的处理逻辑
        for step in res:
            if isinstance(step, str):
                final_result += step
            else:
                final_result += step.get("text", "")
        return final_result

        
        
