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
from enum import Enum
from typing import Union
from typing import Optional

from appbuilder.core.assistant.type import (
    AssistantTool,
    AssistantContent,
    AssistantModel,
    ResponseFormat
)


class AssistantMessageRole(str, Enum):
    USER = 'user'

class AssistantMessage(BaseModel):
    content: str
    role: Optional[AssistantMessageRole] = Field(
        default=AssistantMessageRole.USER)
    file_ids: Optional[list[str]] = Field(default=[], max_length=10)


class AssistantMessageCreateRequest(BaseModel):
    thread_id: str
    role: Optional[str] = Field(
        default=AssistantMessageRole.USER)
    content: str
    file_ids: Optional[list[str]] =  Field(default=[], max_length=10)


class AssistantMessageCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    role: str = Field(
        default=AssistantMessageRole.USER)
    content: Optional[list[AssistantContent]] = []
    created_at: int = 0
    thread_id: str = ""
    assistant_id: Optional[str] = ""
    run_id: Optional[str] = ""
    file_ids: Optional[list[str]] = []


class AssistantThread(BaseModel):
    messages: Optional[list[AssistantMessage]] = []
    metadata: Optional[dict] = Field(default={}, max_length=16)

class ThreadCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    created_at: int = 0


class ThreadCreateRequest(BaseModel):
    messages: list[AssistantMessage]


class AssistantThread(BaseModel):
    messages: list[AssistantMessage] = []


class RunActionInfo(BaseModel):
    toolName: str = ""
    actionName: str = ""
    actionContent: str = ""


class FuncitonCall(BaseModel):
    name: str = ""
    arguments: str = ""
    output: str = ""


class ToolCall(BaseModel):
    id: str = ""
    type: str = 'function'
    function: Union[FuncitonCall, None] = None


class SubmitToolOutput(BaseModel):
    tool_calls: Union[list[ToolCall], None] = None


class RequiredAction(BaseModel):
    type: str = ""
    submit_tool_outputs: Union[SubmitToolOutput, None] = None


class LastError(BaseModel):
    type: str = ""
    message: str = ""

class FinalAnswerMessage(BaseModel):
    message_id: Optional[str] = ""
    content: Optional[AssistantContent] = None

class FinalAnswer(BaseModel):
    type: Optional[str] = "message"
    message: Optional[FinalAnswerMessage] = None

class RunResult(BaseModel):
    id: str = ""
    object: str = ""
    assistant_id: str = ""
    thread_id: str = ""

    model: str = ""
    instructions: str = ""
    thought_instructions: str = ""
    chat_instructions: str = ""
    tools: Optional[list[AssistantTool]] = None
    file_ids: Optional[list[str]] = None

    status: str = ""
    required_action: Optional[RequiredAction] = None
    last_error: Optional[LastError] = None
    final_answer: Optional[FinalAnswer] = None
    created_at: int = 0
    started_at: int = 0
    expired_at: int = 0
    cancelled_at: int = 0
    failed_at: int = 0
    completed_at: int = 0


class RunMessageCreation(BaseModel):
    message_id: str = ""


class ToolInfo(BaseModel):
    type: str = ""
    name: str = ""
    arguments: str = ""
    output: str = ""


class RunStepDetail(BaseModel):
    type: str = ""
    message_creation: Union[RunMessageCreation, None] = None
    action_info: Union[RunActionInfo, None] = None
    tool_calls: Union[list[ToolCall], None] = None
    tool_info: Union[list[ToolInfo], None] = None


class RunStepResult(BaseModel):
    id: str = ""
    object: str = ""
    assistant_id: str = ""
    thread_id: str = ""
    run_id: str = ""
    status: str = ""
    created_at: int = 0
    started_at: int = 0
    expired_at: int = 0
    cancelled_at: int = 0
    failed_at: int = 0
    completed_at: int = 0
    last_error: Union[LastError, None] = None
    type: str = 'null'
    step_datail: Union[RunStepDetail, None] = None


class StreamRunDetail(BaseModel):
    type: str = ""
    message_creation: Union[RunMessageCreation, None] = None
    run_object: Union[RunResult, None] = None
    run_step_object: Union[RunStepResult, None] = None
    tool_calls: Union[list[ToolCall], None] = None
    error_info: Union[LastError, None] = None


class StreamRunStatus(BaseModel):
    event: str = "status"
    status: str = ""
    send_id: int = 0
    message: str = ""
    event_type: str = ""
    details: Optional[StreamRunDetail] = None


class StreamRunMessage(BaseModel):
    event: str = "message"
    status: str = ""
    send_id: int = 0
    is_end: int = 0
    message_id: str = ""
    message_index: str = ""
    content: Optional[list[AssistantContent]] = None


class ToolOutput(BaseModel):
    tool_call_id: str = ""
    output: str = ""
    run_id: str = ""


class AssistantRunRequest(BaseModel):
    thread_id: Optional[str] = Field(default="")
    model: AssistantModel = Field(default="ERNIE-4.0-8K")
    assistant_id: Optional[str] = Field(default="")
    metadata: Optional[dict] =  Field(default={}, max_length=16)
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    instructions: Optional[str] = Field(default="", max_length=4096)
    thought_instructions: Optional[str] = Field(default="", max_length=4096)
    chat_instructions: Optional[str] = Field(default="", max_length=4096)
    stream: Optional[bool] = False
    thread: Optional[AssistantThread] = None
    tools: Optional[list[AssistantTool]] = []
    tool_output: Optional[ToolOutput] = None


class AssistantSubmitToolOutputsRequest(BaseModel):
    thread_id: str = Field(default="", min_length=1)
    run_id: str = Field(default="", min_length=1)
    tool_outputs: Optional[list[ToolOutput]] = Field(default=[], min_length=1)


class AssistantRunCancelRequest(BaseModel):
    thread_id: str = Field(default="", min_length=1)
    run_id: str = Field(default="", min_length=1)
