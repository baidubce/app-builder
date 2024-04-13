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

from appbuilder import Message
from pydantic import BaseModel
from typing import Union


""" Messages Related Data Class """


class AssitantFileInfo(BaseModel):
    url: str = ""
    url_type: str = ""
    file_name: str = ""
    file_id: str = ""


class AssistantAnnotation(BaseModel):
    type: str = "file_info"
    text: str = ""
    start_index: int = 0
    end_index: int = 0
    file_info: Union[AssitantFileInfo, None] = None


class AssistantText(BaseModel):
    value: str = ""
    annotations: Union[list[str], None] = None


class AssistantContent(BaseModel):
    type: str = "text"
    text: Union[AssistantText, None] = None


class AssistantMessage(BaseModel):
    content: str
    role: str = "user"
    file_ids: list[str] = []


class AssistantMessageCreateRequest(BaseModel):
    thread_id: str
    role: str = 'user'
    content: str
    file_ids: Union[list[str], None] = []


class AssistantMessageCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    name: str = ""
    role: str = ""
    content: Union[list[AssistantContent], None] = []
    metadata: Union[dict, None] = None
    created_at: int = 0
    thread_id: str = ""
    content_type: str = 'text'
    assistant_id: Union[str, None] = ""
    run_id: Union[str, None] = ""
    file_ids: Union[list[str], None] = []


""" Conversation Related Data Class """


class ConversationCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    created_at: int = 0


class ConversationCreateRequest(BaseModel):
    messages: list[AssistantMessage]


class AssistantThread(BaseModel):
    messages: list[AssistantMessage] = []


""" Assistant Related Data Class """


class AssistantFunctionCall(BaseModel):
    name: str
    arguments: str


class AssistantExample(BaseModel):
    role: str = "user"
    content: str
    function_call: AssistantFunctionCall

class AssistantFunctionJsonSchema(BaseModel):
    type: str = 'object'
    properties: Union[dict, None] = None
    required: Union[list[str],None] = None

class AssistantFunction(BaseModel):
    name: str
    description: str
    parameters: Union[AssistantFunctionJsonSchema, None] = None
    responses:  Union[AssistantFunctionJsonSchema, None] = None
    examples: Union[list[list[AssistantExample]], None] = None


class AssistantTool(BaseModel):
    type: str = 'function'
    function: AssistantFunction = None


class AssistantCreateRequest(BaseModel):
    model: str = "ERNIE-4.0-8K"
    name: str
    description: str
    response_format: str = "text"
    instructions: str
    thought_instructions: str
    chat_instructions: str
    tools: list[AssistantTool]
    file_ids: list[str]


class AssistantCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    name: str = ""
    description: str = ""
    model: str = ""
    instructions: str = ""
    tools: Union[list[AssistantTool], None] = None
    metadata: Union[dict, None] = None
    created_at: int = 0
    thought_instructions: str = ""
    chat_instructions: str = ""
    response_format: str = ""
    file_ids: Union[list[str], None] = None
    user_storage: Union[str, None] = None


""" File Related Data Class """


class AssistantFilesCreateResponse(BaseModel):
    id: str = ""
    bytes: int = 0
    object: str = ""
    purpose: str = ""
    create_at: int = 0
    filename: str = ""
    classification_id: str = ""


""" Runs Related Data Class """


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


class FinalAnswer(BaseModel):
    type: str = ""
    message: Union[Message, None] = None


class RunResult(BaseModel):
    id: str = ""
    object: str = ""
    assistant_id: str = ""
    thread_id: str = ""

    model: str = ""
    instructions: str = ""
    tools: Union[list[AssistantTool], None] = None
    file_ids: Union[list[str],None] = None

    status: str = ""
    required_action: Union[RequiredAction, None] = None
    last_error: Union[LastError, None] = None
    final_answer: Union[FinalAnswer, None] = None
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
    type: str
    message_creation: Union[RunMessageCreation, None] = None
    run_object: Union[RunResult, None] = None
    run_step_object: Union[RunStepResult, None] = None
    action_info: Union[RunActionInfo, None] = None
    tool_calls: Union[list[ToolCall], None] = None
    tool_info: Union[list[ToolInfo], None] = None
    error_info: Union[LastError, None] = None


class StreamRunStatus(BaseModel):
    status: str = ""
    send_id: int = 0
    message: str = ""
    event_type: str = ""
    details: Union[StreamRunDetail, None] = None


class StreamRunMessage(BaseModel):
    status: str = ""
    send_id: int = 0
    is_end: int = 0
    message_id: str = ""
    message_index: str = ""
    content: Union[list[AssistantContent],None] = None
    metadata: Union[dict,None] = None



class ToolOutput(BaseModel):
    tool_call_id: str = ""
    output: str = ""


class AssistantRunRequest(BaseModel):
    thread_id: str = ""
    model: str = ""
    assistant_id: str = ""
    metadata: Union[dict, None] = None
    response_format: str = "text"
    instructions: str = ""
    thought_instructions: str = ""
    chat_instructions: str = ""
    stream: bool = False
    thread: Union[AssistantThread, None] = None
    tools: list[AssistantTool] = []
    tool_output: Union[ToolOutput, None] = None


class AssistantSubmitToolOutputsRequest(BaseModel):
    thread_id: str = ""
    run_id: str = ""
    tool_outputs: Union[list[ToolOutput], None] = None


class AssistantRunCancelRequest(BaseModel):
    thread_id: str = ""
    run_id: str = ""
