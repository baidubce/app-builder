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
from appbuilder.core.console.appbuilder_client import data_class


class AppBuilderClientRunContext(object):
    def __init__(self) -> None:
        self.current_event = None
        self.current_tool_calls = None
        self.current_status = None
        self.need_tool_submit = False
        self.is_complete = False
        self.current_thought = ""


class AppBuilderEventHandler(object):
    def __init__(self):
        pass

    def init(self,
                 appbuilder_client,
                 conversation_id,
                 query,
                 file_ids=None,
                 tools=None,
                 stream: bool = False,
                 event_handler=None,
                 **kwargs):
        self._appbuilder_client = appbuilder_client
        self._conversation_id = conversation_id
        self._query = query
        self._file_ids = file_ids
        self._tools = tools
        self._stream = stream
        self._event_handler = event_handler
        self._kwargs = kwargs
        self._is_complete = False
        self._need_tool_call = False
        self._last_tool_output = None

        self._iterator = self.__run_process__() if not self._stream else self.__stream_run_process__()

    def __run_process__(self):
        while not self._is_complete:
            if not self._need_tool_call:
                res = self._run()
                self.__event_process__(res)
            else:
                res = self._submit_tool_output()
                self.__event_process__(res)
            yield res

    def __event_process__(self, run_response):
        try:
            event = run_response.content.events[-1]
        except Exception as e:
            raise ValueError(e)
        
        event_status = event.status
        
        if event.status == 'success':
            self._is_complete = True
        elif event.status == 'interrupt':
            self._need_tool_call = True

        context_func_map = {
            "preparing": self.preparing,
            "running": self.running,
            "error": self.error,
            "done": self.done,
            "interrupt": self.interrupt,
            "success": self.success,
        }
        
        run_context = AppBuilderClientRunContext()
        self._update_run_context(run_context, run_response.content)
        if event_status in context_func_map:
            func = context_func_map[event_status]
            func_res = func(run_context, run_response.content)

            if event_status == "interrupt":
                assert isinstance(func_res, list)
                if len(func_res) == 0:
                    raise ValueError("Tool output is empty")
                else:
                    if not isinstance(func_res[0], data_class.ToolOutput):
                        try:
                            check_tool_output = data_class.ToolOutput(**func_res[0])
                        except Exception as e:
                            logger.info("func tool_calls's output should be list[ToolOutput] or list[dict(can be trans to ToolOutput)]")
                            raise ValueError(e)
                self._last_tool_output =func_res
        else:
            logger.warning(
                "Unknown status: {}, response data: {}".format(event_status, run_response))

    def __stream_run_process__(self):
        while not self._is_complete:
            if not self._need_tool_call:
                res = self._run()
                self.__stream_event_process__(res)
            else:
                res = self._submit_tool_output()
                self.__stream_event_process__(res)
            yield res

    def __stream_event_process__(self, run_response):
        for msg in run_response.content:
            if len(msg.events) == 0:
                continue
            try:
                event = msg.events[-1]
            except Exception as e:
                raise ValueError(e)
            
            event_status = event.status
            
            if event.status == 'success':
                self._is_complete = True
            elif event.status == 'interrupt':
                self._need_tool_call = True

            context_func_map = {
                "preparing": self.preparing,
                "running": self.running,
                "error": self.error,
                "done": self.done,
                "interrupt": self.interrupt,
                "success": self.success,
            }
            
            run_context = AppBuilderClientRunContext()
            self._update_run_context(run_context, msg)
            if event_status in context_func_map:
                func = context_func_map[event_status]
                func_res = func(run_context, msg)

                if event_status == "interrupt":
                    assert isinstance(func_res, list)
                    if len(func_res) == 0:
                        raise ValueError("Tool output is empty")
                    else:
                        if not isinstance(func_res[0], data_class.ToolOutput):
                            try:
                                check_tool_output = data_class.ToolOutput(**func_res[0])
                            except Exception as e:
                                logger.info("func tool_calls's output should be list[ToolOutput] or list[dict(can be trans to ToolOutput)]")
                                raise ValueError(e)
                    self._last_tool_output =func_res
            else:
                logger.warning(
                    "Unknown status: {}, response data: {}".format(event_status, run_response))

    def _update_run_context(self, run_context, run_response):
        run_context.current_event = run_response.events[-1]
        run_context.current_tool_calls = run_context.current_event.tool_calls
        run_context.current_status =  run_context.current_event.status
        run_context.need_tool_submit = run_context.current_status == 'interrupt'
        run_context.is_complete = run_context.current_status == 'success'
        try:
            run_context.current_thought = run_context.current_event.detail.get(
                "text", {}).get(
                    "function_call", {}).get(
                        "thought", "")
        except Exception as e:
            pass

    def _run(self):
        res = self._appbuilder_client.run(
            conversation_id=self._conversation_id,
            query=self._query,
            file_ids=self._file_ids,
            stream=self._stream,
            tools=self._tools
        )
        return res

    def _submit_tool_output(self):
        assert self._last_tool_output is not None
        res = self._appbuilder_client.run(
            conversation_id=self._conversation_id,
            file_ids=self._file_ids,
            stream=self._stream,
            tool_outputs=self._last_tool_output
        )
        return res

    def __next__(self):
        return self._iterator.__next__()

    def __iter__(self):
        for item in self._iterator:
            yield item

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            raise exc_val
        return

    def until_done(self):
        for _ in self._iterator:
            pass

    def interrupt(self, run_context, run_response):
        return self.tool_calls(run_context, run_response)

    def preparing(self, run_context, run_response):
        pass

    def running(self, run_context, run_response):
        pass
    
    def error(self, run_context, run_response):
        pass

    def done(self, run_context, run_response):
        pass

    def success(self, run_context, run_response):
        pass
