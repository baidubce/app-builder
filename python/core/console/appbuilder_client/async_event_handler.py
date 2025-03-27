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


class AsyncAppBuilderEventHandler(object):
    def __init__(self):
        pass

    async def init(
        self,
        appbuilder_client,
        conversation_id,
        query,
        file_ids=None,
        tools=None,
        stream: bool = False,
        event_handler=None,
        action=None,
        **kwargs,
    ):
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
            action (object, optional): 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息。
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
        self._action = action

        self._iterator = (
            self.__run_process__()
            if not self._stream
            else self.__stream_run_process__()
        )

    async def __run_process__(self):
        """
        运行进程，并在每次执行后生成结果。

        Args:
            无参数。

        Returns:
            Generator: 生成器，每次执行后返回结果。

        """
        while not self._is_complete:
            if not self._need_tool_call:
                res = await self._run()
                await self.__event_process__(res)
            else:
                res = await self._submit_tool_output()
                await self.__event_process__(res)
            yield res
        if self._need_tool_call and self._is_complete:
            await self.reset_state()

    async def __async_run_process__(self):
        """
        异步运行进程，并在每次执行后生成结果

        Args:
            无参数

        Returns:
            Generator[Any, None, None]: 生成器，每次执行后返回结果
        """
        while not self._is_complete:
            if not self._need_tool_call:
                res = await self._run()
                await self.__event_process__(res)
            else:
                res = await self._submit_tool_output()
                await self.__event_process__(res)
            yield res
        if self._need_tool_call and self._is_complete:
            await self.reset_state()

    async def __event_process__(self, run_response):
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

        if event.status == "success":
            self._is_complete = True
        elif event.status == "interrupt":
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
        await self._update_run_context(run_context, run_response.content)
        await self.handle_event_type(run_context, run_response.content)
        await self.handle_content_type(run_context, run_response.content)
        if event_status in context_func_map:
            func = context_func_map[event_status]
            func_res = await func(run_context, run_response.content)

            if event_status == "interrupt":
                assert isinstance(func_res, list)
                if len(func_res) == 0:
                    raise ValueError("Tool output is empty")
                else:
                    if not isinstance(func_res[0], data_class.ToolOutput):
                        try:
                            check_tool_output = data_class.ToolOutput(
                                **func_res[0])
                        except Exception as e:
                            logger.error(
                                "func interrupt's output should be list[ToolOutput] or list[dict(can be trans to ToolOutput)]"
                            )
                            raise ValueError(e)
                self._last_tool_output = func_res
        else:
            logger.warning(
                "Unknown status: {}, response data: {}".format(
                    event_status, run_response
                )
            )

    async def __stream_run_process__(self):
        """
        异步流式运行处理函数

        Args:
            无参数

        Returns:
            Generator[Any, None, None]: 返回处理结果的生成器
        """
        while not self._is_complete:
            if not self._need_tool_call:
                res = await self._run()
            else:
                res = await self._submit_tool_output()
            async for msg in self.__stream_event_process__(res):
                yield msg

    async def __stream_event_process__(self, run_response):
        """
        处理流事件，并调用对应的方法

        Args:
            run_response: 包含流事件信息的响应对象

        Returns:
            None

        Raises:
            ValueError: 当处理事件时发生异常或中断时工具输出为空时
        """
        async for msg in run_response.content:
            if len(msg.events) == 0:
                continue
            try:
                event = msg.events[-1]
            except Exception as e:
                raise ValueError(e)

            event_status = event.status

            if event.status == "success":
                self._is_complete = True
            elif event.status == "interrupt":
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
            await self._update_run_context(run_context, msg)
            await self.handle_event_type(run_context, msg)
            await self.handle_content_type(run_context, msg)
            if event_status in context_func_map:
                func = context_func_map[event_status]
                func_res = await func(run_context, msg)

                if event_status == "interrupt":
                    assert isinstance(func_res, list)
                    if len(func_res) == 0:
                        raise ValueError("Tool output is empty")
                    else:
                        if not isinstance(func_res[0], data_class.ToolOutput):
                            try:
                                check_tool_output = data_class.ToolOutput(
                                    **func_res[0])
                            except Exception as e:
                                logger.info(
                                    "func interrupt's output should be list[ToolOutput] or list[dict(can be trans to ToolOutput)]"
                                )
                                raise ValueError(e)
                    self._last_tool_output = func_res
            else:
                logger.warning(
                    "Unknown status: {}, response data: {}".format(
                        event_status, run_response
                    )
                )

            yield msg

    async def _update_run_context(self, run_context, run_response):
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
        run_context.current_status = run_context.current_event.status
        run_context.need_tool_submit = run_context.current_status == "interrupt"
        run_context.is_complete = run_context.current_status == "success"
        try:
            run_context.current_thought = (
                run_context.current_event.detail.get("text", {})
                .get("function_call", {})
                .get("thought", "")
            )
            if run_context.current_thought == "":
                run_context.current_thought = run_response.events[0].detail.get(
                    "text", ""
                )
        except Exception:
            pass

    async def _run(self):
        res = await self._appbuilder_client.run(
            conversation_id=self._conversation_id,
            query=self._query,
            file_ids=self._file_ids,
            stream=self._stream,
            tools=self._tools,
            action=self._action,
        )
        return res

    async def _submit_tool_output(self):
        assert self._last_tool_output is not None
        res = await self._appbuilder_client.run(
            conversation_id=self._conversation_id,
            file_ids=self._file_ids,
            stream=self._stream,
            tool_outputs=self._last_tool_output,
        )
        return res

    async def __anext__(self):
        return await self._iterator.__anext__()

    async def __aiter__(self):
        async for item in self._iterator:
            yield item

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            raise exc_val

        return

    async def reset_state(self):
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

    async def new_dialog(
        self,
        query=None,
        file_ids=None,
        tools=None,
        action=None,
        stream: bool = None,
        event_handler=None,
        **kwargs,
    ):
        """
        重置handler部分参数，用于复用该handler进行多轮对话。

        Args:
            query (str): 用户输入的查询语句。
            file_ids (list, optional): 文件ID列表，默认为None。
            tools (list, optional): 工具列表，默认为None。
            stream (bool, optional): 是否使用流式处理，默认为False。
            action (object, optional): 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息。
            event_handler (callable, optional): 事件处理函数，默认为None。
            **kwargs: 其他可选参数。

        Returns:
            None

        """
        self._query = query or self._query
        self._stream = stream or self._stream

        self._file_ids = file_ids
        self._tools = tools
        self._event_handler = event_handler
        self._kwargs = kwargs
        self._action = action

        # 重置部分状态
        self._is_complete = False
        self._need_tool_call = False
        self._last_tool_output = None
        self._iterator = (
            self.__run_process__()
            if not self._stream
            else self.__stream_run_process__()
        )

    async def until_done(self):
        """
        迭代并遍历内部迭代器中的所有元素，直到迭代器耗尽。

        Args:
            无参数。

        Returns:
            无返回值。

        """
        async for _ in self._iterator:
            pass

    async def handle_content_type(self, run_context, run_response):
        # 用户可重载该方法，用于处理不同类型的content_type
        pass

    async def handle_event_type(self, run_context, run_response):
        # 用户可重载该方法，用于处理不同类型的event_type
        pass

    async def interrupt(self, run_context, run_response):
        # 用户可重载该方法，当event_status为interrupt时，会调用该方法
        pass

    async def preparing(self, run_context, run_response):
        # 用户可重载该方法，当event_status为preparing时，会调用该方法
        pass

    async def running(self, run_context, run_response):
        # 用户可重载该方法，当event_status为running时，会调用该方法
        pass

    async def error(self, run_context, run_response):
        # 用户可重载该方法，当event_status为error时，会调用该方法
        pass

    async def done(self, run_context, run_response):
        # 用户可重载该方法，当event_status为done时，会调用该方法
        pass

    async def success(self, run_context, run_response):
        # 用户可重载该方法，当event_status为success时，会调用该方法
        pass


class AsyncToolCallEventHandler(AsyncAppBuilderEventHandler):
    def __init__(self, mcp_client=None, functions=[]):
        super().__init__()
        self.mcp_client = mcp_client
        self.functions = functions
        self.result = ""

    async def init(
        self,
        appbuilder_client,
        conversation_id,
        query,
        file_ids=None,
        tools=None,
        stream: bool = False,
        event_handler=None,
        action=None,
        **kwargs,
    ):
        await super().init(
            appbuilder_client,
            conversation_id,
            query,
            file_ids,
            tools,
            stream,
            event_handler,
            action,
            **kwargs,
        )
        self.result = ""

    async def reset_state(self):
        await super().reset_state()
        self.result = ""

    async def new_dialog(
        self,
        query=None,
        file_ids=None,
        tools=None,
        action=None,
        stream=None,
        event_handler=None,
        **kwargs,
    ):
        await super().new_dialog(
            query, file_ids, tools, action, stream, event_handler, **kwargs
        )
        self.result = ""

    async def interrupt(self, run_context, run_response):
        thought = run_context.current_thought
        logger.debug("Agent 中间思考: {}\n".format(thought))

        tool_output = []
        for tool_call in run_context.current_tool_calls:
            function_name = tool_call.function.name
            function_arguments = tool_call.function.arguments
            result = ""
            function_map = {f.__name__: f for f in self.functions}
            if function_name in function_map:
                result = function_map[function_name](
                    **tool_call.function.arguments)
                logger.debug("ToolCall结果: {}\n".format(result))
            elif self.mcp_client:
                logger.debug(
                    "MCP工具名称: {}, MCP参数:{}\n".format(
                        function_name, function_arguments
                    )
                )
                mcp_server_result = await self.mcp_client.call_tool(
                    function_name, function_arguments
                )
                logger.debug("MCP ToolCall结果: {}\n".format(mcp_server_result))
                for i, content in enumerate(mcp_server_result.content):
                    if content.type == "text":
                        result = result + mcp_server_result.content[i].text
            else:
                logger.warning(f"Tool not found: {function_name}")
            tool_output.append(
                {
                    "tool_call_id": tool_call.id,
                    "output": result,
                }
            )
        return tool_output

    async def running(self, run_context, run_response):
        if self._stream and run_response.answer and run_response.answer != "":
            logger.debug("Agent 流式回答: {}".format(run_response.answer))
            self.result += run_response.answer

    async def success(self, run_context, run_response):
        if not self._stream:
            logger.debug("Agent 非流式回答: {}".format(run_response.answer))
            self.result = run_response.answer
