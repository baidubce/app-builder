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
from appbuilder.utils.sse_util import SSEClient
from appbuilder.utils.logger_util import logger

class AppBuilderClientStreamRunContext(object):
    def __init__(self)->None:
        self._current_event = None
        self._current_tool_calls = None
        self._current_request_id = None
        self._current_status = None
        self._need_tool_submit = False
    

    def update_step_context(self):
        pass

class AppBuilderEventHandler(object):
    def __init__(self, response) -> None:
        self._response = response
        self._sse_client = SSEClient(response)  
        self._event_stream = self._sse_client.events()
        self._iterator = self.__stream__()
        self.stream_run_context = AppBuilderClientStreamRunContext()
        self._is_complete = False

    def __stream__(self):
        try:
            for event in self._event_stream:
                self.stream_run_context.update_step_context()
                process_res = self.__stream_event_process__(event)
                yield process_res
        except Exception as e:
            logger.error(e)

    def __stream_event_process__(self, event):
        pass

    def __timeout_process__(self, event):
        pass

    def __tool_call_retry_max_count_process__(self):
        pass

    def __next__(self):
        pass

    def __iter__(self):
        pass

    def until_done(self):
        for _ in self._iterator:
            pass
    
    def befor_tool_calls(self, stream_run_context):
        pass

    def tool_calls(self):
        pass

    def run_begin(self):
        pass

    def run_end(self):
        pass

    def answers(self):
        pass



class AppBuilderRunManager(AppBuilderEventHandler):
    def __init__(
            self,
            response,
            event_handler: AppBuilderEventHandler = None,
    ) -> None:
        self._response = response
        self._event_handler = event_handler
        self._event_handler._init(self._response)
    
    def __enter__(self):
        return self._event_handler
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_val
        pass
        return
        self._event_handler._finish()