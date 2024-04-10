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

from appbuilder.core.assistants.assistant_config import AssistantConfig
from appbuilder import Message

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

class RunResult():
    id: str
    object: str
    assistant_id: str
    conversation_id: str
    assistant_config: AssistantConfig
    status: str
    required_action: RequiredAction
    last_error: LastError
    final_answer: FinalAnswer
    created_at: int
    started_at: int
    expired_at: int
    cancelled_at: int
    failed_at: int
    completed_at: int


class StreamrRunResult():
    id: str
    object: str
    assistant_id: str
    conversation_id: str
    assistant_config: AssistantConfig
    status: str
    required_action: str
    last_error: str
    final_answer: str
    created_at: int
    started_at: int
    expired_at: int
    cancelled_at: int
    failed_at: int
