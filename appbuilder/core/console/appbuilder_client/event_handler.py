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
        """
        初始化方法。
        
        Args:
            无参数。
        
        Returns:
            None
        
        """
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
        """
        初始化类实例并设置相关参数。
        
        Args:
            appbuilder_client (object): AppBuilder客户端实例对象。
            conversation_id (str): 对话ID。
            query (str): 用户输入的查询语句。
            file_ids (list, optional): 文件ID列表，默认为None。
            tools (list, optional): 工具列表，默认为None。
            stream (bool, optional): 是否使用流式处理，默认为False。
            event_handler (callable, optional): 事件处理函数，默认为None。
            **kwargs: 其他可选参数。
        
        Returns:
            None
        
        """
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
        """
        运行进程，并在每次执行后生成结果。
        
        Args:
            无参数。
        
        Returns:
            Generator: 生成器，每次执行后返回结果。
        
        """
        while not self._is_complete:
            if not self._need_tool_call:
                res = self._run()
                self.__event_process__(res)
            else:
                res = self._submit_tool_output()
                self.__event_process__(res)
            yield res
        
        self.reset_state()

    def __event_process__(self, run_response):
        """
        处理事件响应。
        
        Args:
            run_response (RunResponse): 运行时响应对象。
        
        Returns:
            None
        
        Raises:
            ValueError: 当解析事件时发生异常或工具输出为空时。
        """
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
                            logger.error("func interrupt's output should be list[ToolOutput] or list[dict(can be trans to ToolOutput)]")
                            raise ValueError(e)
                self._last_tool_output =func_res
        else:
            logger.warning(
                "Unknown status: {}, response data: {}".format(event_status, run_response))

    def __stream_run_process__(self):
        """
        流式运行处理函数
        
        Args:
            无参数。
        
        Returns:
            Generator[Any, None, None]: 返回处理结果的生成器。
        
        """
        while not self._is_complete:
            if not self._need_tool_call:
                res = self._run()
            else:
                res = self._submit_tool_output()
            for msg in self.__stream_event_process__(res):
                yield msg    

    def __stream_event_process__(self, run_response):
        """
        处理流事件，并调用对应的方法
        
        Args:
            run_response: 包含流事件信息的响应对象
        
        Returns:
            None
        
        Raises:
            ValueError: 当处理事件时发生异常或中断时工具输出为空时
        """
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
                                logger.info("func interrupt's output should be list[ToolOutput] or list[dict(can be trans to ToolOutput)]")
                                raise ValueError(e)
                    self._last_tool_output =func_res
            else:
                logger.warning(
                    "Unknown status: {}, response data: {}".format(event_status, run_response))
            
            yield msg

    def _update_run_context(self, run_context, run_response):
        """
        更新运行上下文。
        
        Args:
            run_context (dict): 运行上下文字典。
            run_response (object): 运行响应对象。
        
        Returns:
            None
        
        """
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

    def reset_state(self):
        """
        重置该对象的状态，将所有实例变量设置为默认值。
        
        Args:
            无
        
        Returns:
            无
        
        """
        self._appbuilder_client = None
        self._conversation_id = None
        self._query = None
        self._file_ids = None
        self._tools = None
        self._stream = False
        self._event_handler = None
        self._kwargs = None
        self._last_tool_output = None
        self._is_complete = False
        self._need_tool_call = False
        self._iterator = None

    def until_done(self):
        """
        迭代并遍历内部迭代器中的所有元素，直到迭代器耗尽。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        for _ in self._iterator:
            pass

    def interrupt(self, run_context, run_response):
        # 用户可重载该方法，当event_status为interrupt时，会调用该方法
        pass

    def preparing(self, run_context, run_response):
        # 用户可重载该方法，当event_status为preparing时，会调用该方法
        pass

    def running(self, run_context, run_response):
        # 用户可重载该方法，当event_status为running时，会调用该方法
        pass
    
    def error(self, run_context, run_response):
        # 用户可重载该方法，当event_status为error时，会调用该方法
        pass

    def done(self, run_context, run_response):
        # 用户可重载该方法，当event_status为done时，会调用该方法
        pass

    def success(self, run_context, run_response):
        # 用户可重载该方法，当event_status为success时，会调用该方法
        pass
