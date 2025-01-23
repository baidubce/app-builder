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
from typing import Optional, Union
from appbuilder.core.component import ComponentOutput, Content


class RunRequest(BaseModel):
    """ Component Run方法请求体 """
    class Parameters(BaseModel, extra="allow"):
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
            description='{"xxx.pdf": "http:///"}，画布中开始节点的系统参数fileUrls', alias="_sys_file_urls"
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

    stream: bool = Field(default=False, description='是否流式返回')
    parameters: Parameters = Field(..., description="调用传参")


class ContentWithEvent(Content):
    """ ContentWithEvent """

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

    event: Event = Field(None, description="事件信息")

class RunResponse(BaseModel):
    """ Component Run方法响应体 """
    conversation_id: str = Field(None, description="对话id")
    message_id: str = Field(None, description="消息id")
    trace_id: str = Field(None, description="追踪id")
    user_id: str = Field(None, description="开发者UUID（计费依赖）")
    end_user_id: str = Field(None, description="终端用户id")
    status: str = Field(None, description="对话状态，有interrupt, running, error, done四种枚举值")
    role: str = Field(None, description="当前消息来源，默认tool")
    content: list[ContentWithEvent] = Field(
        None,
        description="当前组件返回内容的主要payload，List[ContentWithEvent]，每个 Content 包括了当前 event 的一个元素",
    )
    request_id: str = Field(None, description="请求id")
    code: Union[str, int] = Field(None, description="响应码")
    message: str = Field(None, description="响应消息")
