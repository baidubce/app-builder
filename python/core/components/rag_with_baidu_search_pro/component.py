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
from appbuilder.core.components.rag_with_baidu_search_pro.model import ParseRagProResponse
from appbuilder.utils.trace.tracer_wrapper import components_run_trace
from pydantic import BaseModel, Field, conint, confloat
from typing import Optional


class RagWithBaiduSearchProRequest(BaseModel):
    """
    RagWithBaiduSearchPro 的请求

    Attributes:
        message (object): 用户的消息
        stream (bool): 是否流式处理
        instruction (str): 指令
        model (Optional[str]): 模型名称
        temperature (confloat(ge=0, le=1)): 温度，范围在0到1之间
        top_p (confloat(ge=0, le=1)): top_p，范围在0到1之间
        search_top_k (conint(ge=1)): search_top_k，
    """
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

    Args:
        query (str): 用户的 query 输入
    """
    query: str = Field(..., description="用户的 query 输入", max_length=300)


class RagWithBaiduSearchPro(Component):
    """
    RagWithBaiduSearchPro 组件
    """
    name = "rag_with_baidu_search_pro"
    version = "v1"
    meta: RagWithBaiduSearchProArgs

    def __init__(
            self,
            model: str,
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = False,
            instruction: Optional[Message] = None,
            **kwargs
    ):
        super().__init__(
            meta=RagWithBaiduSearchProArgs, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)
        self.model = model
        self.instruction = instruction
        self.server_sub_path = "/v1/ai_engine/copilot_engine/service/v1/baidu_search_rag/general"

    @ttl_lru_cache(seconds_to_live=1 * 60 * 60)  # 1h
    def set_secret_key_and_gateway(self, secret_key: Optional[str] = None, gateway: str = ""):
        """
        设置API密钥和网关地址。
        
        Args:
            secret_key (Optional[str], optional): API密钥，默认为None。如果为None，则不会更新现有的API密钥。
            gateway (str, optional): 网关地址，默认为空字符串。如果为空字符串，则不会更新现有的网关地址。
        
        Returns:
            None
        
        """
        super(RagWithBaiduSearchPro, self).set_secret_key_and_gateway(
            secret_key=secret_key, gateway=gateway)
        self.__class__.model_info = ModelInfo(client=self.http_client)

    @components_run_trace
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
        """
        执行模型推理。
        
        Args:
            message (Message): 待处理的信息对象。
            stream (bool, optional): 是否以流的形式接收响应数据。默认为False。
            instruction (Instruction, optional): 指令信息对象。默认为None。
            model (str, optional): 模型名称。默认为None，表示使用当前实例的模型。
            temperature (float, optional): 温度参数，控制生成文本的随机性。默认为1e-10。
            top_p (float, optional): 累积概率阈值，用于控制生成文本的多样性。默认为1e-10。
            search_top_k (int, optional): 搜索候选结果的数量。默认为4。
            hide_corner_markers (bool, optional): 是否隐藏响应中的边界标记。默认为True。
        
        Returns:
            Message: 处理后的信息对象。
        
        Raises:
            AppBuilderServerException: 如果输入信息或指令过长，将抛出此异常。
        """
        if len(message.content) > 300:
            raise AppBuilderServerException(service_err_message="query is too long, expected <= 300, got {}"
                                            .format(len(message.content)))
        if instruction is not None and len(instruction.content) > 1024:
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
