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
import os
import json
from typing import Optional
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.utils.sse_util import SSEClient


class AssistantEventHandler():
    def __init__(self):
        self._sse_client = SSEClient(AssistantHTTPClient().get_sse_url())
        self._sse_client.on('message', self.__handle_event)
        self._sse_client.start()

    def before_tool_calls(self):
        pass

    def tool_calls(self):
        pass

    def after_tool_calls(self):
        pass

    def before_message_creation(self):
        pass

    def message_creation(self):
        pass

    def after_message_creation(self):
        pass


class AssistantStreamManager():
    def __init__(
        self,
        response,
        event_handler: AssistantEventHandler,
    ) -> None:
        self._event_handler = event_handler
        self._response = response

    def __enter__(self) -> AssistantEventHandler:
        self._stream = self._response
        self._event_handler._init(self.__stream)
        return self.__event_handler

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass
