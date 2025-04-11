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
from typing import Optional, Union, List
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


class ImageURL(BaseModel):
    """ ImageURL """
    url: str = Field(..., description="图片可下载url地址或base64编码后的图片内容p")

class ImageContentBlock(BaseModel):
    """ ImageContentBlock """
    type: str = Field(..., description="值固定为image_url")
    image_url: ImageURL = Field(
        ..., description="图片地址，支持图片格式包括jpeg、 jpg、 png、 webp"
    )


class TextContentBlock(BaseModel):
    """ TextContentBlock """
    type: str = Field(..., description="值固定为text")
    text: str = Field(..., description="文本内容")


class AISearchMessage(BaseModel):
    """ AISearchMessage """
    role: str = Field(..., description="对话角色，枚举：user、assistant")
    content: Union[str, List[Union[TextContentBlock, ImageContentBlock]]] = Field(
        ..., description="对话内容"
    )

class AISearchChatRequest(BaseModel):
    """ AISearchChatRequest """
    messages: list[AISearchMessage] = Field(..., description="对话历史。array的长度需要是奇数, role必须是user-assistant-user交替，以user开始以user结束。")
    stream: bool = Field(default=False, description='是否流式返回')
    model: str = Field(..., description="模型名称")
    instruction: str = Field(..., description="指令")
    temperature: float = Field(
        None,
        description="模型采样参数。较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定。",
    )
    top_p: float = Field(
        None,
        description="模型采样参数。影响输出文本的多样性，取值越大，生成文本的多样性越强。",
    )
    enable_corner_markers: bool = Field(
        default=False,
        description="是否返回角标，用于标记模型输出内容的参考来源。",
    )
    search_mode: str = Field(
        None,
        description="控制是否开启联网搜索。默认为 auto。auto：自动判断是否需要搜索、required： 必须执行搜索、disabled： 禁用搜索功能。",
    )
    search_recency_filter: str = Field(
        None,
        description="网页时效性范围限制。week:7天、month：30天、semiyear：180天、year：365天",
    )
    search_domain_filter: List[str] = Field(
        None, description="站点过滤，只返回列表中站点的网页"
    )
    enable_followup_queries: bool = Field(
        default=False,
        description="是否开启追问。针对用户问题和大模型回答结果，大模型给出推荐的追问。",
    )
    response_format: str = Field(
        None,
        description="输出内容样式。默认值 auto。可选值：auto：模型自动判断是纯文本输出还是图文混排输出。ext：文本输出。rich_text: 图文混排输出。如：在美食和旅游两个场景下，输出文本中嵌入markdown语法的图片内容。 比如: ...北京美食包括北京烤鸭等![北京烤鸭](image_url)。",
    )
    enable_reasoning: bool = Field(
        False,
        description="是否开启深度思考，仅对DeepSeek-R1模型生效，开启后，输出答案前会输出思考内容。默认值：False",
    )
    enable_deep_search: bool = Field(False, "是否开启深搜索。默认值：False")
    
