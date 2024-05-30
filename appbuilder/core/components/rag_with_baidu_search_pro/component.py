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
import json
from typing import Optional
from pydantic import Field
from appbuilder.core.component import Component, ComponentArguments
from appbuilder.core.message import Message
from appbuilder.core.utils import ModelInfo, ttl_lru_cache
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.rag_with_baidu_search_pro.parse_rag_pro_response import ParseRagProResponse
from pydantic import BaseModel, Field, conint, confloat
from typing import Optional


class RagWithBaiduSearchProRequest(BaseModel):
    message: object
    stream: bool = False
    instruction: str
    model: Optional[str] = None
    temperature: confloat(ge=0, le=1) = Field(1e-10, description="temperature范围在0到1之间")
    top_p: confloat(ge=0, le=1) = Field(1e-10, description="top_p范围在0到1之间")
    search_top_k: conint(ge=1) = Field(4, description="search_top_k必须是大于等于1的整数")
    hide_corner_markers: bool = True


class RagWithBaiduSearchProArgs(ComponentArguments):
    """
    RagWithBaiduSearchPro 的参数
    """
    query: str = Field(..., description="用户的 query 输入", max_length=300)


class RagWithBaiduSearchPro(Component):
    name = "rag_with_baidu_search_pro"
    version = "v1"
    meta: RagWithBaiduSearchProArgs

    def __init__(
            self,
            model: str,
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = False,
            instruction: Optional[Message] = None
    ):
        super().__init__(
            meta=RagWithBaiduSearchProArgs, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)
        self.model = model
        self.instruction = instruction
        self.server_sub_path = "/v1/ai_engine/copilot_engine/service/v1/baidu_search_rag/general"

    @ttl_lru_cache(seconds_to_live=1 * 60 * 60)  # 1h
    def set_secret_key_and_gateway(self, secret_key: Optional[str] = None, gateway: str = ""):
        super(RagWithBaiduSearchPro, self).set_secret_key_and_gateway(
            secret_key=secret_key, gateway=gateway)
        self.__class__.model_info = ModelInfo(client=self.http_client)

    def run(
            self,
            message,
            stream=False,
            instruction=None,
            model=None,
            temperature=1e-10,
            top_p=1e-10,
            search_top_k=4,
            hide_corner_markers=True
    ):

        if len(message.content) > 300:
            raise AppBuilderServerException(service_err_message="query is too long, expected <= 300, got {}"
                                            .format(len(message.content)))
        if len(instruction.content) > 1024:
            raise AppBuilderServerException(service_err_message="instruction is too long, expected <= 1024, got {}"
                                            .format(len(instruction)))

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        req = RagWithBaiduSearchProRequest(
            message=[
                {
                    "role": "user",
                    "content": message.content
                }
            ],
            stream=stream,
            instruction=instruction.content if instruction else "",
            model=self.model,
            temperature=temperature,
            top_p=top_p,
            search_top_k=search_top_k,
            hide_corner_markers=hide_corner_markers
        )
        server_url = self.http_client.service_url(sub_path=self.server_sub_path)
        response = self.http_client.session.post(url=server_url, headers=headers, json=req.model_dump(), stream=stream)
        self.http_client.check_response_header(response)

        return ParseRagProResponse(response, stream).to_message()
