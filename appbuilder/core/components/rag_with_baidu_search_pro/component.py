# -*- coding: utf-8 -*-
"""
@time :    22.5.24  AM11:52
@File:     _component
@Author :  baiyuchen
@Version:  python3.8
"""
import json
from typing import Optional
from pydantic import Field
from appbuilder.core.component import Component, ComponentArguments
from appbuilder.core.message import Message
from appbuilder.core.utils import ModelInfo, ttl_lru_cache
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.rag_with_baidu_search_pro.parse_rag_pro_response import ParseRagProResponse


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

        req_dict = {
            "message": [{
                "role": "user",
                "content": message.content
            }],
            "instruction": instruction.content if instruction else "",
            "search_top_k": search_top_k,
            "stream": stream,
            "hide_corner_markers": hide_corner_markers,
            "model": self.model,
            "temperature": temperature,
            "top_p": top_p
        }
        payload = json.dumps(req_dict)
        server_url = self.http_client.service_url(sub_path=self.server_sub_path)
        response = self.http_client.session.post(url=server_url, headers=headers, data=payload, stream=stream)
        self.http_client.check_response_header(response)

        return ParseRagProResponse(response, stream).to_message()
