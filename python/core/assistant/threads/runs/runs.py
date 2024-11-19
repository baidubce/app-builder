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
from typing import Optional, Union
from appbuilder.core.assistant.threads.runs.steps import Steps
from appbuilder.core.assistant.threads.runs.stream_helper import AssistantStreamManager
from appbuilder.core.assistant.threads.runs.stream_helper import AssistantEventHandler
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core.assistant.type import public_type
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.utils.sse_util import SSEClient
from appbuilder.utils.trace.tracer_wrapper import assistent_tool_trace, assistant_run_trace, assistent_stream_run_trace, assistent_stream_run_with_handler_trace



class Runs():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    @property
    def steps(self) -> Steps:
        """
        返回步骤对象
        
        Args:
            无
        
        Returns:
            Steps: 返回一个新的Steps对象
        
        """
        return Steps()
    
    @assistant_run_trace
    def run(self,
            assistant_id: str,
            thread_id: Optional[str] = "",
            thread: Optional[thread_type.AssistantThread] = None,
            model: Optional[str] = None,
            response_format: Optional[str] = "text",
            instructions: Optional[str] = None,
            thought_instructions: Optional[str] = None,
            chat_instructions: Optional[str] = None,
            tools: Optional[list[assistant_type.AssistantTool]] = [],
            metadata: Optional[dict] = {},
            tool_output: Optional[thread_type.ToolOutput] = None,
            model_parameters: Optional[public_type.AssistantModelParameters] = None,
            user_info: Optional[public_type.AssistantUserInfo] = None,
            user_loc: Optional[public_type.AssistantUserLoc] = None,
            ) -> thread_type.RunResult:
        """
        Args:
            assistant_id (str): 助手id
            thread_id (Optional[str], optional): 对话id. Defaults to "".
            thread (Optional[thread_type.AssistantThread], optional): 对话信息. Defaults to None.
            model (Optional[str], optional): 模型名称. Defaults to None.
            response_format (Optional[str], optional): 返回格式. Defaults to "text".
            instructions (Optional[str], optional): 指令信息. Defaults to None.
            thought_instructions (Optional[str], optional): 思考指令信息. Defaults to None.
            chat_instructions (Optional[str], optional): 闲聊指令信息. Defaults to None.
            tools (Optional[list[assistant_type.AssistantTool]], optional): 工具列表. Defaults to [].
            metadata (Optional[dict], optional): 元数据. Defaults to {}.
            tool_output (Optional[thread_type.ToolOutput], optional): 工具输出. Defaults to None.
            model_parameters (Optional[public_type.AssistantModelParameters], optional): 模型运行参数. Defaults to None.
            user_info (Optional[public_type.AssistantUserInfo], optional): 用户身份信息. Defaults to None.
            user_loc (Optional[public_type.AssistantUserLoc], optional): 用户定位信息. Defaults to None.
        Returns:
            thread_type.RunResult: 运行结果

        Raises:
            ValueError: thread_id和thread不能同时为空,model_parameters的各个参数不在规定范围内

        Note:
            1. 如果thread_id没有传，则thread必须要传值
            2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
            3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs")

        if thread_id == "" and thread is None:
            raise ValueError("Runs().run() argument thread_id && thread can't be empty at the same time")
        
        if model_parameters:
            chat_temperature = model_parameters.chat_parameters.temperature
            chat_top_p = model_parameters.chat_parameters.top_p
            chat_penalty_score = model_parameters.chat_parameters.penalty_score
            thought_temperature = model_parameters.thought_parameters.temperature
            thought_top_p = model_parameters.thought_parameters.top_p
            thought_penalty_score = model_parameters.thought_parameters.penalty_score

            if chat_temperature < 0 or chat_temperature > 1 or thought_temperature < 0 or thought_temperature > 1:
                raise ValueError("chat_temperature and thought_temperature must be in range [0, 1]")
            if chat_top_p < 0 or chat_top_p > 1 or thought_top_p < 0 or thought_top_p > 1:
                raise ValueError("chat_top_p and thought_top_p must be in range [0, 1]")
            if chat_penalty_score < 1 or chat_penalty_score > 2 or thought_penalty_score < 1 or thought_penalty_score > 2:
                raise ValueError("chat_penalty_score and thought_penalty_score must be in range [1, 2]")
            
        req = thread_type.AssistantRunRequest(
            thread_id=thread_id,
            thread=thread,
            model=model,
            assistant_id=assistant_id,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            model_parameters = model_parameters,
            stream=False,
            tools=tools,
            metadata=metadata,
            tool_output=tool_output,
            user_info=user_info,
            user_loc=user_loc
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunResult(**data)
        return resp
    

    def _stream(self,
                   assistant_id: str,
                   thread_id: Optional[str] = "",
                   thread: Optional[thread_type.AssistantThread] = None,
                   model: Optional[str] = None,
                   response_format: Optional[str] = "text",
                   instructions: Optional[str] = None,
                   thought_instructions: Optional[str] = None,
                   chat_instructions: Optional[str] = None,
                   tools: Optional[list[assistant_type.AssistantTool]] = [],
                   metadata: Optional[dict] = {},
                   tool_output: Optional[thread_type.ToolOutput] = None,
                   model_parameters: Optional[public_type.AssistantModelParameters] = None,
                   user_info: Optional[public_type.AssistantUserInfo] = None,
                   user_loc: Optional[public_type.AssistantUserLoc] = None,
                   ):
        """
        启动一个流式运行的对话，用于处理对话流中的消息。
        
        Args:
            assistant_id (str): 助理ID。
            thread_id (Optional[str], optional): 线程ID，用于恢复历史对话。默认为空字符串。
            thread (Optional[thread_type.AssistantThread], optional): 线程对象，用于恢复历史对话。默认为None。
            model (Optional[str], optional): 使用的模型名称。默认为None。
            response_format (Optional[str], optional): 响应格式，支持"text"和"json"两种格式。默认为"text"。
            instructions (Optional[str], optional): 指令文本。默认为 None。
            thought_instructions (Optional[str], optional): 思考指令文本。默认为 None。
            chat_instructions (Optional[str], optional): 聊天指令文本。默认为 None。
            tools (Optional[list[assistant_type.AssistantTool]], optional): 使用的工具列表。默认为空列表。
            metadata (Optional[dict], optional): 元数据字典。默认为空字典。
            tool_output (Optional[thread_type.ToolOutput], optional): 工具输出对象。默认为None。
            model_parameters (Optional[public_type.AssistantModelParameters], optional): 模型运行参数. Defaults to None.
        
        Returns:
            Iterator[thread_type.AssistantRunEvent]: 返回一个迭代器，用于遍历流式运行中的事件。
        
        Raises:
            ValueError: 如果thread_id和thread参数同时为空，则会引发ValueError异常。model_parameters的各个参数不在规定范围内。
        
        Note:
            1. 如果thread_id没有传，则thread必须要传值。
            2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user。
            3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs")

        """
        注意：
            1. 若thread_id没有传，则thread必须要传值
            2. 若这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
            3. 若这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user
        """
        if thread_id == "" and thread is None:
            raise ValueError("Runs().run() argument thread_id and thread can't be empty at the same time")
        
        if model_parameters:
    
            chat_temperature = model_parameters.chat_parameters.temperature
            chat_top_p = model_parameters.chat_parameters.top_p
            chat_penalty_score = model_parameters.chat_parameters.penalty_score
            thought_temperature = model_parameters.thought_parameters.temperature
            thought_top_p = model_parameters.thought_parameters.top_p
            thought_penalty_score = model_parameters.thought_parameters.penalty_score

            if chat_temperature < 0 or chat_temperature > 1 or thought_temperature < 0 or thought_temperature > 1:
                raise ValueError("chat_temperature and thought_temperature must be in range [0, 1]")
            if chat_top_p < 0 or chat_top_p > 1 or thought_top_p < 0 or thought_top_p > 1:
                raise ValueError("chat_top_p and thought_top_p must be in range [0, 1]")
            if chat_penalty_score < 1 or chat_penalty_score > 2 or thought_penalty_score < 1 or thought_penalty_score > 2:
                raise ValueError("chat_penalty_score and thought_penalty_score must be in range [1, 2]")

        req = thread_type.AssistantRunRequest(
            thread_id=thread_id,
            thread=thread,
            model=model,
            assistant_id=assistant_id,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            stream=True,
            model_parameters=model_parameters,
            tools=tools,
            metadata=metadata,
            tool_output=tool_output,
            user_info=user_info,
            user_loc=user_loc
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            stream=True,
            timeout=None
        )
        return response

    @assistent_stream_run_trace
    def stream_run(self,
                   assistant_id: str,
                   thread_id: Optional[str] = "",
                   thread: Optional[thread_type.AssistantThread] = None,
                   model: Optional[str] = None,
                   response_format: Optional[str] = "text",
                   instructions: Optional[str] = None,
                   thought_instructions: Optional[str] = None,
                   chat_instructions: Optional[str] = None,
                   tools: Optional[list[assistant_type.AssistantTool]] = [],
                   metadata: Optional[dict] = {},
                   tool_output: Optional[thread_type.ToolOutput] = None,
                   model_parameters: Optional[public_type.AssistantModelParameters] = None,
                   user_info: Optional[public_type.AssistantUserInfo] = None,
                   user_loc: Optional[public_type.AssistantUserLoc] = None,
                   ) -> Union[thread_type.StreamRunStatus, thread_type.StreamRunMessage, None]:
        """
        启动一个流式运行的对话，用于处理对话流中的消息。

        Args:
            assistant_id (str): 助理ID。
            thread_id (Optional[str], optional): 线程ID，用于恢复历史对话。默认为空字符串。
            thread (Optional[thread_type.AssistantThread], optional): 线程对象，用于恢复历史对话。默认为None。
            model (Optional[str], optional): 使用的模型名称。默认为None。
            response_format (Optional[str], optional): 响应格式，支持"text"和"json"两种格式。默认为"text"。
            instructions (Optional[str], optional): 指令文本。默认为 None。
            thought_instructions (Optional[str], optional): 思考指令文本。默认为 None。
            chat_instructions (Optional[str], optional): 聊天指令文本。默认为 None。
            tools (Optional[list[assistant_type.AssistantTool]], optional): 使用的工具列表。默认为空列表。
            metadata (Optional[dict], optional): 元数据字典。默认为空字典。
            tool_output (Optional[thread_type.ToolOutput], optional): 工具输出对象。默认为None。
            model_parameters (Optional[public_type.AssistantModelParameters], optional): 模型参数对象。默认为None。

        Returns:
            Union[thread_type.StreamRunStatus, thread_type.StreamRunMessage, None]: 返回一个迭代器，每次迭代返回一个处理结果对象，可能是 StreamRunStatus 或 StreamRunMessage。

        Raises:
            ValueError: 如果thread_id和thread参数同时为空，则会引发ValueError异常。

        Note:
            1. 如果thread_id没有传，则thread必须要传值。
            2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user。
            3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user。
        """

        response = self._stream(
            assistant_id=assistant_id,
            thread_id=thread_id,
            thread=thread,
            model=model,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            model_parameters=model_parameters,
            tools=tools,
            metadata=metadata,
            tool_output=tool_output,
            user_info=user_info,
            user_loc=user_loc
        )
        self._http_client.check_response_header(response)
        sse_client = SSEClient(response)
        return self._iterate_events(sse_client.events())

    @assistent_stream_run_with_handler_trace
    def stream_run_with_handler(self,
                   assistant_id: str,
                   thread_id: Optional[str] = "",
                   thread: Optional[thread_type.AssistantThread] = None,
                   model: Optional[str] = None,
                   response_format: Optional[str] = "text",
                   instructions: Optional[str] = None,
                   thought_instructions: Optional[str] = None,
                   chat_instructions: Optional[str] = None,
                   tools: Optional[list[assistant_type.AssistantTool]] = [],
                   metadata: Optional[dict] = {},
                   tool_output: Optional[thread_type.ToolOutput] = None,
                   event_handler: Optional[AssistantEventHandler] = None,
                   model_parameters: Optional[public_type.AssistantModelParameters] = None,
                   user_info: Optional[public_type.AssistantUserInfo] = None,
                   user_loc: Optional[public_type.AssistantUserLoc] = None,
                   ) -> AssistantStreamManager:
        """
        使用带有事件处理器的流运行助手
        
        Args:
            assistant_id (str): 助手的唯一标识符
            thread_id (Optional[str], optional): 会话线程的标识符，默认为空字符串. 默认为 "".
            thread (Optional[thread_type.AssistantThread], optional): 会话线程对象，默认为None. 默认为 None.
            model (Optional[str], optional): 模型标识符，默认为None. 默认为 None.
            response_format (Optional[str], optional): 响应格式，可选值为"text"或"json"，默认为"text". 默认为 "text".
            instructions (Optional[str], optional): 主要指令，默认为空字符串. 默认为 None.
            thought_instructions (Optional[str], optional): 思维指令，默认为空字符串. 默认为 None.
            chat_instructions (Optional[str], optional): 聊天指令，默认为空字符串. 默认为 None.
            tools (Optional[list[assistant_type.AssistantTool]], optional): 助手工具列表，默认为空列表. 默认为 [].
            metadata (Optional[dict], optional): 元数据字典，默认为空字典. 默认为 {}.
            tool_output (Optional[thread_type.ToolOutput], optional): 工具输出对象，默认为None. 默认为 None.
            event_handler (Optional[AssistantEventHandler], optional): 事件处理器对象，默认为None. 默认为 None.
            model_parameters (Optional[public_type.AssistantModelParameters], optional): 模型参数对象，默认为None. 默认为 None.
            user_info (Optional[public_type.AssistantUserInfo], optional): 用户信息对象，默认为None. 默认为 None.
            user_loc (Optional[public_type.AssistantUserLoc], optional): 用户位置信息对象，默认为None. 默认为 None.
        
        Returns:
            AssistantStreamManager: 返回的流管理器对象
        
        Raises:
            HTTPError: 如果HTTP响应状态码不为200，则抛出HTTPError异常
        
        """
        response = self._stream(
            assistant_id=assistant_id,
            thread_id=thread_id,
            thread=thread,
            model=model,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            model_parameters=model_parameters,
            tools=tools,
            metadata=metadata,
            tool_output=tool_output,
            user_info=user_info,
            user_loc=user_loc
        )
        self._http_client.check_response_header(response)

        return AssistantStreamManager(
            response=response,
            event_handler=event_handler or AssistantEventHandler()
        )

    def _iterate_events(self, events):
        """
        根据给定的事件列表，生成对应的事件处理结果

        Args:
            events (list): 事件列表，每个元素为一个包含 'event' 和 'data' 属性的字典对象

        Returns:
            generator: 返回一个生成器，每次迭代返回一个处理结果对象，可能是 StreamRunStatus 或 StreamRunMessage

        """
        for event in events:
            try:
                event_class = event.event
                if event_class == "ping":
                    # TODO(chengmo): record ping event, add timeout func
                    continue

                data = event.data
                if len(data) == 0:
                    data = event.raw
                data = json.loads(data)

                if event_class == "status":
                    result = thread_type.StreamRunStatus(**data)
                elif event_class == "message":
                    result = thread_type.StreamRunMessage(**data)

            except Exception as e:
                print(e)

            yield result


    @assistent_tool_trace
    def submit_tool_outputs(self,
                            run_id: str,
                            thread_id: str,
                            tool_outputs: Optional[list[thread_type.ToolOutput]]) -> thread_type.RunResult:
        """
        向服务端提交工具输出

        Args:
            run_id (str): 运行ID
            thread_id (str): 线程ID
            tool_outputs (Optional[list[thread_type.ToolOutput]]): 工具输出列表，可选

        Returns:
            thread_type.RunResult: 运行结果

        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url(
            "/v2/threads/runs/submit_tool_outputs")

        req = thread_type.AssistantSubmitToolOutputsRequest(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunResult(**data)
        return resp

    @assistent_tool_trace
    def cancel(self, run_id: str, thread_id: str, sync: bool = False) -> thread_type.RunResult:
        """
        取消指定线程的运行
        
        Args:
            run_id (str): 运行的ID
            thread_id (str): 线程的ID
            sync (bool, optional): 是否同步执行. 默认为False.
        
        Returns:
            thread_type.RunResult: 取消运行的结果
        
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/cancel")

        req = thread_type.AssistantRunCancelRequest(
            run_id=run_id,
            thread_id=thread_id,
            sync = sync
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunResult(**data)
        return resp

    @assistent_tool_trace
    def list(self, thread_id: str, limit: int = 20,
             order: str = 'desc', after: str = "", before: str = "") -> thread_type.RunListResponse:
        """
        列出对应thread的历史run记录
        
        Args:
            thread_id (str): 线程ID
            limit (int, optional): 列表数量限制，默认为20
            order (str, optional): 排序方式，'asc'为升序，'desc'为降序，默认为'desc'
            after (str, optional): 返回在指定时间之后的运行列表，默认为空字符串
            before (str, optional): 返回在指定时间之前的运行列表，默认为空字符串
        
        Returns:
            thread_type.RunListResponse: 列出对应thread的历史run记录
        
        Raises:
            无
        
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/list")

        req = thread_type.AssistantRunListRequest(
            thread_id=thread_id,
            limit=limit,
            order=order,
            after=after,
            before=before
        )
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunListResponse(**data)
        return resp

    @assistent_tool_trace
    def query(self, thread_id: str, run_id: str) -> thread_type.RunResult:
        """
        根据thread_id和run_id，查询run的详情
        
        Args:
            thread_id (str): 线程ID。
            run_id (str): 运行ID。
        
        Returns:
            thread_type.RunResult: 查询到的运行结果。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/query")

        req = thread_type.AssistantRunQueryRequest(
            thread_id=thread_id,
            run_id=run_id
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )

        self._http_client.check_response_header(response)
        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        resp = thread_type.RunResult(**data)
        return resp
    