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
class AssistantMessage(BaseModel):
    content: str
    role: str = "user"
    file_ids: list[str] = []


""" Conversation Related Data Class """
class ConversationCreateResponse(BaseModel):
    id: str
    object: str
    created_at: int


class ConversationCreateRequest(BaseModel):
    messages: list[AssistantMessage]


""" Assistant Related Data Class """
class AssistantFunctionCall(BaseModel):
    name: str
    arguments: str

class AssistantExample(BaseModel):
    role: str = "user"
    content: str
    function_call: AssistantFunctionCall

class AssistFunction(BaseModel):
    name: str
    description: str
    parameters: str
    responses: str
    examples: list[list[AssistantExample]]

class AssistantTool(BaseModel):
    type: str
    function: AssistFunction = None

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
    id: str
    object: str
    name: str
    description: str
    model: str
    instructions: str
    tools: list[AssistantTool]
    meta_data: Union[dict, None] = None
    created_at: int
    thought_instructions: str
    chat_instructions: str
    response_format: str
    file_ids: list[str]
    user_storage: Union[str, None] = None



""" File Related Data Class """

class AssistantFilesCreateResponse(BaseModel):
    id: str
    bytes: int
    object: str
    purpose: str
    create_at: int
    filename: str
    classification_id: str



""" Runs Related Data Class """


class FunctionCall():
    name: str
    arguments: str


class ToolCall():
    id: str
    type: str
    function: FunctionCall


class SubmitToolOutput():
    tool_calls: list


class RequiredAction():
    type: str
    submit_tool_outputs: SubmitToolOutput


class LastError():
    type: str
    message: str


class FinalAnswer():
    type: str
    message: Message


# class RunResult():
#     id: str
#     object: str
#     assistant_id: str
#     conversation_id: str
#     assistant_config: AssistantConfig
#     status: str
#     required_action: RequiredAction
#     last_error: LastError
#     final_answer: FinalAnswer
#     created_at: int
#     started_at: int
#     expired_at: int
#     cancelled_at: int
#     failed_at: int
#     completed_at: int


# class StreamrRunResult():
#     id: str
#     object: str
#     assistant_id: str
#     conversation_id: str
#     assistant_config: AssistantConfig
#     status: str
#     required_action: str
#     last_error: str
#     final_answer: str
#     created_at: int
#     started_at: int
#     expired_at: int
#     cancelled_at: int
#     failed_at: int
