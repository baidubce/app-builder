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
from typing import Union


class AppBuilderClientRequest(BaseModel):
    """会话请求参数
        属性:
            query (str): 查询参数
            response_mode (str): streaming或blocking
            conversation_id (str): 会话ID
            file_ids(list[str]): 文件ID
            app_id：应用ID
    """
    query: str = ""
    stream: bool
    conversation_id: str
    file_ids: list[str] = []
    app_id: str


class OriginalEvent(BaseModel):
    """会话请求参数
        属性:
            event_code (int): 0代表成功，非0为失败
            event_message (str): 错误详情
            event_type（str）：事件类型
            event_status（str）:事件状态
            content_type（str）:内容类型
            outputs（dict）：事件输出
    """
    event_code: int = ""
    event_message: str = ""
    event_type: str = ""
    event_id: str = ""
    event_status: str = ""
    content_type: str = ""
    outputs: dict = {}


class AppBuilderClientResponse(BaseModel):
    """会话请求参数
        属性:
            request_id (int): 请求ID
            date (str): 消息返回时间的时间戳
            answer (str): 模型回答
            conversation_id（str）: 会话ID
            message_id(str): 消息ID
            is_completion(bool): 是否结束
            content(list): 内容详情
    """
    request_id: str = ""
    date: str = ""
    answer: str = ""
    conversation_id: str = ""
    message_id: str = ""
    content: list[OriginalEvent] = []


class TextDetail(BaseModel):
    """content_type=text，详情内容
            属性:
                text(str): 文本详情
    """
    text: str = ""


class CodeDetail(BaseModel):
    """content_type=code，详情内容
             属性:
                 text(str): 文本详情
                 code: 代码解释器工具生产的代码
                 files: 代码解释器生成的可下载文件地址列表
     """
    text: str = ""
    code: str = ""
    files: list[str] = []


class RAGReference(BaseModel):
    """RAG应用详情
           属性:
               id (int): 对应来源ID
               from (str): 信息来源
               url (str): BaiduSearch 的专用字段
               content（str）: 般用来当做文档名或者链接的title使用，前端展示可以根据情况截断。
               segment_id(str): 片段ID
               document_id(str): 文档ID
               document_name(str): 文档名
       """
    id: str = ""
    from_: str = Field(..., alias='from')
    url: str = ""
    content: str = ""
    segment_id: str = ""
    document_id: str = ""
    dataset_id: str = ""
    document_name: str = ""


class RAGDetail(BaseModel):
    """content_type=rag，详情内容
            属性:
                text(str): 文本详情
                references(list[RAGReference]): 引用详情
    """
    text: str = ""
    references: list[RAGReference] = []


class FunctionCallDetail(BaseModel):
    """content_type=function_call，详情内容
             属性:
                 text(str): 文本详情
     """
    text: Union[str, dict] = ""
    image: str = ""
    audio: str = ""
    video: str = ""


class ImageDetail(BaseModel):
    """content_type=function_call，详情内容
            属性:
                image(str): 图片下载地址
    """
    image: str = ""


class AudioDetail(BaseModel):
    """content_type=audio，详情内容
            属性:
                image(str): 音频下载地址
    """
    audio: str = ""


class VideoDetail(BaseModel):
    """content_type=video，详情内容
            属性:
                video(str): 视频下载地址
    """
    video: str = ""


class StatusDetail(BaseModel):
    pass


class DefaultDetail(BaseModel):
    """content_type为其它时，详情内容
        属性:
            urls(list[str]): 件链接列表
            files(list[str]): 下载文件地址列表
            image(str): 工具生成的图片url
            video(str): 工具生成的语音url
            audio(str):工具生成的音频url
       """
    urls: list[str] = []
    files: list[str] = []
    image: str = ""
    video: str = ""
    audio: str = ""


class Event(BaseModel):
    """执行步骤的具体内容
        属性:
            code (int): 响应code码
            message (str): 错误详情
            status (str): 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）
            event_type（str）: 事件类型
            content_type（str）: 内容类型
            detail(dict): 事件详情
    """
    code: int = 0
    message: str = ""
    status: str = ""
    event_type: str = ""
    content_type: str = ""
    detail: dict = {}


class AppBuilderClientAnswer(BaseModel):
    """执行步骤的具体内容
        属性:
            answer(str): query回答内容
            events( list[Event]): 事件列表
       """
    answer: str = ""
    events: list[Event] = []


class FileUploadResponse(BaseModel):
    """文档上传结果
           属性:
             request_id (str): 请求ID
             id (str): 文件ID
             conversation_id (str): 对话ID
    """
    request_id: str = ""
    id: str = ""
    conversation_id: str = ""


class CreateConversationResponse(BaseModel):
    """文档上传结果
           属性:
             code (int): 响应code码
             request_id (str): 请求ID
             conversation_id (str): 对话ID
    """
    request_id: str = ""
    conversation_id: str = ""
