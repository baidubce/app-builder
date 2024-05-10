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
from appbuilder.utils.sse_util import SSEClient
from appbuilder.utils.logger_util import logger


class StreamRunContext(object):
    def __init__(self) -> None:
        self._current_event = None
        self._current_tool_calls = None
        self._current_run_id = None
        self._current_run_step_id = None
        self._current_thread_id = None
        self._current_assistant_id = None

    @property
    def current_event(self) -> Union[thread_type.StreamRunStatus,
                                     thread_type.StreamRunMessage,
                                     None]:
        return self._current_event

    def set_current_event(self, event):
        if isinstance(event, thread_type.StreamRunStatus) or \
                isinstance(event, thread_type.StreamRunMessage):
            self._current_event = event
        else:
            self._current_event = None

    @property
    def current_tool_calls(self) -> Union[list[thread_type.ToolCall], None]:
        return self._current_tool_calls
    
    def set_current_tool_calls(self, tool_calls):
        if isinstance(tool_calls, list) and len(tool_calls) > 0:
            for call in tool_calls:
                assert isinstance(call, thread_type.ToolCall), \
                    "current_tool_calls should be a list of ToolCall object."
            self._current_tool_calls = tool_calls
        else:
            self._current_tool_calls = None

    @property
    def current_run_id(self) -> Union[str, None]:
        return self._current_run_id
    
    def set_current_run_id(self, run_id):
        if isinstance(run_id, str) and len(run_id) > 0:
            self._current_run_id = run_id
        else:
            self._current_run_id = None

    @property
    def current_run_step_id(self) -> Union[str, None]:
        return self._current_run_step_id
    
    def set_current_run_step_id(self, run_step_id):
        if isinstance(run_step_id, str) and len(run_step_id) > 0:
            self._current_run_step_id = run_step_id
        else:
            self._current_run_step_id = None
    
    @property
    def current_thread_id(self) -> Union[str, None]:
        return self._current_thread_id
    
    def set_current_thread_id(self, thread_id):
        if isinstance(thread_id, str) and len(thread_id) > 0:
            self._current_thread_id = thread_id
        else:
            self._current_thread_id = None
    
    @property
    def current_assistant_id(self) -> Union[str, None]:
        return self._current_assistant_id
    
    def set_current_assistant_id(self, assistant_id):
        if isinstance(assistant_id, str) and len(assistant_id) > 0:
            self._current_assistant_id = assistant_id
        else:
            self._current_assistant_id = None


    def reset_step_context(self):
        self._current_tool_calls = None
        self._current_run_step_id = None
        self._current_event = None


class AssistantEventHandler():
    def __init__(self):
        pass

    def _init(self, response):
        self._response = response
        self._sse_client = SSEClient(response)
        self._event_stream = self._sse_client.events()
        self._iterator = self.__stream__()
        self.stream_run_context = StreamRunContext()

    def __stream__(self) -> Iterator[Union[
            thread_type.StreamRunStatus, thread_type.StreamRunMessage, str]]:
        try:
            for event in self._event_stream:
                self.stream_run_context.reset_step_context()
                process_res = self.__stream_event_process__(event)
                yield process_res
        except Exception as e:
            logger.info(e)

    def __stream_event_process__(self, event) -> Union[
            thread_type.StreamRunStatus, thread_type.StreamRunMessage, dict]:
        event_type = event.event
        raw_data = event.data
        if len(raw_data) == 0:
            raw_data = event.raw

        if event_type == 'ping':
            self.__timeout_process__(event)
        elif event_type == 'message':
            data = json.loads(raw_data)
            stream_run_message = thread_type.StreamRunMessage(**data)
            self.stream_run_context.set_current_event(stream_run_message)
            self.messages(stream_run_message)
            return stream_run_message
        elif event_type == 'status':
            data = json.loads(raw_data)
            stream_run_status = thread_type.StreamRunStatus(**data)
            self.stream_run_context.set_current_event(stream_run_status)

            # stream内置的handler，不建议用户重载
            context_func_map = {
                "tool_calls": self._before_tool_calls,
                "run_begin": self._before_run_begin,
            }
            if stream_run_status.event_type in context_func_map:
                context_func = context_func_map[stream_run_status.event_type]
                context_func(stream_run_status)

            # 用户可以自定义的handler
            type_handler_func_map = {
                "run_begin": self.run_begin,
                "run_end": self.run_end,
                "tool_step_begin": self.tool_step_begin,
                "tool_step_end": self.tool_step_end,
                "run_cancelling": self.run_cancelling,
                "tool_calls": self.tool_calls,
                "message_creation": self.message_creation,
                "tool_submitted_output": self.tool_submitted_output
            }

            if stream_run_status.event_type in type_handler_func_map:
                status_handler_func = type_handler_func_map[stream_run_status.event_type]
                status_handler_func(stream_run_status)
            else:
                logger.warning(
                    f"Unknown status: {stream_run_status.event_type}, "
                    f"data: {stream_run_status}"
                )
            return stream_run_status

        return raw_data

    def __timeout_process__(self, event):
        # TODO(chengmo): record ping event, add timeout func
        pass

    def __next__(self) -> Optional[str]:
        return self._iterator.__next__()

    def __iter__(self):
        for item in self._iterator:
            yield item
    
    def until_done(self):
        for _ in self._iterator:
            ...

    def _before_run_begin(self, stream_run_status):
        self.stream_run_context.set_current_run_id(stream_run_status.details.run_object.id)
        self.stream_run_context.set_current_assistant_id(stream_run_status.details.run_object.assistant_id)
        self.stream_run_context.set_current_thread_id(stream_run_status.details.run_object.thread_id)

    def _before_tool_calls(self, stream_run_status):
        self.stream_run_context.set_current_tool_calls(stream_run_status.details.tool_calls)

    def messages(self, messages_event: thread_type.StreamRunMessage):
        # 用户可以重载此函数，当触发messages事件时，会回调此函数
        pass
    
    def tool_calls(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发tool_calls事件时，会回调此函数
        pass

    def tool_submitted_output(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发tool_submitted_output事件时，会回调此函数
        pass

    def message_creation(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发message_creation事件时，会回调此函数
        pass

    def run_begin(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发run_begin事件时，会回调此函数
        pass

    def run_end(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发run_end事件时，会回调此函数
        pass

    def tool_step_begin(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发tool_step_begin事件时，会回调此函数
        pass

    def tool_step_end(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发tool_step_end事件时，会回调此函数
        pass

    def run_cancelling(self, status_event: thread_type.StreamRunStatus):
        # 用户可以重载此函数，当触发run_cancelling事件时，会回调此函数
        pass


class AssistantStreamManager(AssistantEventHandler):
    def __init__(
        self,
        response,
        event_handler: AssistantEventHandler,
    ) -> None:
        self._response = response
        self._event_handler = event_handler
        self._event_handler._init(self._response)

    def __enter__(self) -> AssistantEventHandler:  
        return self._event_handler

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass
