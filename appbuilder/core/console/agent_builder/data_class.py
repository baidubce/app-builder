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
from typing import Union


class HTTPRequest(BaseModel):
    """会话请求参数
        属性:
            query (str): 查询参数
            response_mode (str): streaming或blocking
            conversation_id (str): 会话ID
            file_ids(list[str]): 文件ID
            app_id：应用ID
    """
    query: str = ""
    response_mode: str
    conversation_id: str
    file_ids: list = []
    app_id: str


class OriginalEvent(BaseModel):
    """会话请求参数
        属性:
            event_code (int): 0代表成功，非0为失败
            event_message (str): 错误详情
            node_name (str): 节点名，保留字段
            dependency_nodes（str）:依赖节点名，保留字段
            event_type（str）：事件类型
            event_status（str）:事件状态
            content_type（str）:内容类型
            outputs（dict）：事件输出
    """
    event_code: int = ""
    event_message: str = ""
    node_name: str = ""
    dependency_nodes: list = []
    event_type: str = ""
    event_id: str = ""
    event_status: str = ""
    content_type: str = ""
    outputs: dict = {}


class Result(BaseModel):
    """会话请求参数
        属性:
            answer (str): query结果
            conversation_id (str): 会话ID
            message_id (str): 消息ID
            is_completion（bool）: 会话是否结束
            content（list[OriginalEvent]）: 事件列表
    """
    answer: str = ""
    conversation_id: str = ""
    message_id: str = ""
    is_completion: Union[bool, None] = ""
    content: list = []


class HTTPResponse(BaseModel):
    """会话请求参数
        属性:
            code (int): 响应状态码
            message (str): 状态详情
            trace_id (str): 链路ID
            time（int）: 消息返回时间的时间戳 ，单位为毫秒
            prototype（str）: 与前端交互时会用到的字段
            result: 响应结果
    """
    code: int = 0
    message: str = ""
    trace_id: str = ""
    time: int = 0
    prototype: str = ""
    result: Result = Result()


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
    files: list = []


class RAGDetail(BaseModel):
    """content_type=image，详情内容
            属性:
                text(str): 文本详情
                references(list[dict]): 引用详情
    """
    text: str = ""
    references: list = []


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
                vidoe(str): 视频下载地址
    """
    video: str = ""


class StatusDetail(BaseModel):
    pass


class Event(BaseModel):
    """执行步骤的具体内容
        属性:
            code (int): 响应code码
            message (str): 错误详情
            status (str): 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）
            event_type（str）: 事件类型
            content_type（str）: 内容类型
            detail(dict): 事件详情,
    """
    code: int = 0
    message: str = ""
    status: str = ""
    event_type: str = ""
    content_type: str = ""
    detail: dict = {}


class AgentBuilderAnswer(BaseModel):
    """执行步骤的具体内容
        属性:
            code (int): 响应code码
            message (str): 错误详情
            answer(str): query回答内容
            events( list[Event]): 事件列表
       """
    code: int = 0
    message: str = ""
    answer: str = ""
    events: list = []


class FileUploadResult(BaseModel):
    """文档上传结果
        属性:
            id (str): 文档ID
            conversation_id (str): 对话ID
    """
    id: str = ""
    conversation_id: str = ""


class FileUploadResponse(BaseModel):
    """文档上传结果
           属性:
             code (int): 响应code码
             message (str): 错误详情
             Result (FileUploadResult): 上传结果
    """
    code: int = 0
    message: str = ""
    result: FileUploadResult = FileUploadResult()


class CreateConversationResult(BaseModel):
    """文档上传结果
          属性:
             code (int): 响应code码
             message (str): 错误详情
             conversation_id (str): 对话ID
    """
    conversation_id: str = ""


class CreateConversationResponse(BaseModel):
    """文档上传结果
           属性:
             code (int): 响应code码
             message (str): 错误详情
             Result (FileUploadResult): 上传结果
    """
    code: int = 0
    message: str = ""
    result: CreateConversationResult = CreateConversationResult()
