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
from typing import Optional, Iterator, Union
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.utils.sse_util import SSEClient


class AssistantEventHandler():
    def __init__(self):
        pass

    def _init(self, response):
        self._response = response
        self._sse_client = SSEClient(response)
        self._event_stream = self._sse_client.events()
        self._iterator = self.__stream__()

    def __stream__(self) -> Iterator[Union[
            thread_type.StreamRunStatus, thread_type.StreamRunMessage, str]]:
        try:
            for event in self._event_stream:
                process_res = self.__stream_event_process__(event)
                yield process_res

        except Exception as e:
            print(e)

    def __stream_event_process__(self, event) -> Union[
            thread_type.StreamRunStatus, thread_type.StreamRunMessage, dict]:
        event_type = event.event
        raw_data = event.data
        if len(raw_data) == 0:
            raw_data = event.raw
        data = json.loads(raw_data)

        if event_type == 'ping':
            self.__timeout_process__(event)
        elif event_type == 'message':
            stream_run_message = thread_type.StreamRunMessage(**data)
            self.before_message_creation(stream_run_message)
            self.message_creation(stream_run_message)
            self.after_message_creation(stream_run_message)
            return stream_run_message 
        elif event_type == 'status':
            stream_run_status = thread_type.StreamRunStatus(**data)
            if stream_run_status.status == 'requires_action':
                self.before_tool_calls(stream_run_status)
                self.tool_calls(stream_run_status)
                self.after_tool_calls(stream_run_status)
            else:
                self.before_status_process(stream_run_status)
                self.status_process(stream_run_status)
                self.after_status_process(stream_run_status)
            return stream_run_status
        
        return data


    def __timeout_process__(self, event):
        # TODO(chengmo): record ping event, add timeout func
        pass

    def __next__(self) -> Optional[str]:
        return self._iterator.__next__()

    def __iter__(self):
        for item in self._iterator:
            yield item

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

    def before_status_process(self):
        pass

    def status_process(self):
        pass

    def after_status_process(self):
        pass


class AssistantStreamManager(AssistantEventHandler):
    def __init__(
        self,
        response,
        event_handler: AssistantEventHandler,
    ) -> None:
        self._response = response
        self._event_handler = event_handler

    def __enter__(self) -> AssistantEventHandler:
        self._event_handler._init(self._response)
        return self._event_handler

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass
