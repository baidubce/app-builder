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

r"""landmark recognize component."""
import base64

from appbuilder.core.component import Component
from appbuilder.core.component import ComponentArguments
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException

from typing import Dict, List, Optional, Any
from langchain_community.tools import BaseTool
from copy import deepcopy

class LangChainToolWrapper(Component):
    def __init__(
            self,
            meta: Optional[ComponentArguments] = ComponentArguments(),
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = False,
            langchain_tool: BaseTool() = None,
    ):
        self.langchain_tool = langchain_tool
        tmp_meta = self._parse_langchain_schema()
        super().__init__(meta=tmp_meta, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

    
    def run(self, message: Message) -> Message:
        params = self._before_langchain_tool_run(message)
        response = self.langchain_tool.run(params)
        return self._after_langchain_tool_run(response)

    def _parse_langchain_schema(self) -> None:
        # convert langchain tool schema to component schema
        component_argument = ComponentArguments(
            tool_desc={
                "description": self.langchain_tool.__doc__,
            }
        )
        return component_argument

    def _before_langchain_tool_run(self, message: Message):
        # convert message to tool params
        params = deepcopy(message.content)
        return params

    def _after_langchain_tool_run(self, response: str):
        # convert tool response to message
        return Message(content=response)
