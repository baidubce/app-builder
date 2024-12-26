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

from pydantic import BaseModel
from pydantic import Field
from typing import Optional


class RunRequest(BaseModel):
    """ Component Run方法请求体 """
    class Parameters(BaseModel):
        """ Parameters"""
        class Message(BaseModel):
            """ Message"""
            role: str = Field(..., description="对话角色，枚举：user、assistant")
            content: str = Field(..., description="对话内容")

        sys_origin_query: str = Field(
            ..., description="用户query文字，画布中开始节点的系统参数rawQuery", alias="_sys_origin_query"
        )
        sys_file_urls: Optional[dict] = Field(
            None,
            description='{"xxx.pdf": "http:///"}，画布中开始节点的系统参数fileUrls', alias="sys_file_urls"
        )
        sys_conversation_id: Optional[str] = Field(
            None,
            description="对话id，可通过新建会话接口创建, 画布中开始节点的系统参数conversationId", alias="_sys_conversation_id"
        )
        sys_end_user_id: Optional[str] = Field(
            None, description="终端用户id，画布中开始节点的系统参数end_user_id", alias="_sys_end_user_id"
        )
        sys_chat_history: Optional[list[Message]] = Field(
            None, description="聊天历史记录", alias="_sys_chat_history"
        )

        class Config:
            """
            Config Class
            """

            extra = "allow"

    stream: bool = Field(default=False, description='是否流式返回')
    parameters: Parameters = Field(..., description="调用传参")


class RunResponse(BaseModel):
    """ Component Run方法响应体 """
    class Data(BaseModel):
        """ Data """

        class Content(BaseModel):
            """ Content """

            class Usage(BaseModel):
                """ Usage"""
                prompt_tokens: int = Field(..., description="prompt token消耗")
                completion_tokens: int = Field(..., description="问答返回消耗")
                total_tokens: int = Field(..., description="总token消耗")
                nodes: list[dict] = Field(None, description="工作流节点消耗情况")

            class Metrics(BaseModel):
                """ Metrics"""
                begin_time: str = Field(
                    ..., description="请求开始时间，示例：”2000-01-01T10:00:00.560430“"
                )
                duration: float = Field(
                    ..., description="从请求到当前event总耗时，保留3位有效数字，单位秒s"
                )

            class Event(BaseModel):
                """ Event"""
                id: str = Field(..., description="事件id")
                status: str = Field(...,
                                    description="事件状态，枚举：preparing、running、error、done")
                name: str = Field(
                    ...,
                    description="事件名，相当于调用的深度，深度与前端的渲染逻辑有关系",
                )
                created_time: str = Field(
                    ...,
                    description="当前event发送时间",
                )
                error_code: str = Field(
                    None,
                    description="错误码",
                )
                error_message: str = Field(
                    None,
                    description="错误信息",
                )

            type: str = Field(
                ...,
                description="代表event 类型， text、json、code、files、urls、oral_text、references、image、chart、audio、function_call",
            )
            name: str = Field(..., description="当前内容名称")
            text: dict = Field(
                ...,
                description="代表当前 event 元素的内容，每一种 event 对应的 text 结构固定",
            )
            visible_scope: str = Field(
                ...,
                description="为了界面展示明确的说明字段，枚举: all、llm、user、空",
            )
            usage: Usage = Field(
                None, description="大模型的token使用情况"
            )
            metrics: Metrics = Field(..., description="耗时信息")
            event: Event = Field(..., description="事件信息")

        conversation_id: str = Field(..., description="对话id")
        message_id: str = Field(..., description="消息id")
        trace_id: str = Field(..., description="追踪id")
        user_id: str = Field(..., description="开发者UUID（计费依赖）")
        end_user_id: str = Field(None, description="终端用户id")
        is_completion: bool = Field(..., description="是否完成")
        role: str = Field(..., description="当前消息来源，默认tool")
        content: list[Content] = Field(
            None,
            description="当前组件返回内容的主要payload，List[Content]，每个 Content 包括了当前 event 的一个元素，具体见下文Content对象定义",
        )

    request_id: str = Field(..., description="请求id")
    code: str = Field(None, description="响应码")
    message: str = Field(None, description="响应消息")
    data: Data = Field(..., description="响应数据")
