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
import json
import os
from typing import Union
from aiohttp import FormData
from appbuilder.core.component import Message, Component
from appbuilder.core.console.appbuilder_client import data_class, AppBuilderClient
from appbuilder.core.manifest.models import Manifest
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.sse_util import AsyncSSEClient


class AsyncAppBuilderClient(Component):
    def __init__(self, app_id, **kwargs):
        super().__init__(is_aysnc=True, **kwargs)
        if (not isinstance(app_id, str)) or len(app_id) == 0:
            raise ValueError(
                "app_id must be a str, and length is bigger then zero,"
                "please go to official website which is 'https://cloud.baidu.com/product/AppBuilder'"
                " to get a valid app_id after your application is published."
            )
        self.app_id = app_id
        self._mcp_context = None

    async def create_conversation(self) -> str:
        r"""异步创建会话并返回会话ID

        会话ID在服务端用于上下文管理、绑定会话文档等，如需开始新的会话，请创建并使用新的会话ID

        Args:
            无

        Returns:
            response (str): 唯一会话ID

        """
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/app/conversation")
        response = await self.http_client.session.post(
            url, headers=headers, json={"app_id": self.app_id}, timeout=None
        )
        await self.http_client.check_response_header(response)
        data = await response.json()
        resp = data_class.CreateConversationResponse(**data)
        return resp.conversation_id

    async def run(
        self,
        conversation_id: str,
        query: str = "",
        file_ids: list = [],
        stream: bool = False,
        tools: list[Union[data_class.Tool, Manifest, data_class.MCPTool]] = None,
        tool_outputs: list[data_class.ToolOutput] = None,
        tool_choice: data_class.ToolChoice = None,
        end_user_id: str = None,
        action: data_class.Action = None,
        **kwargs,
    ) -> Message:
        r"""异步运行智能体应用

        Args:
            query (str): query内容
            conversation_id (str): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
            file_ids(list[str]): 文件ID列表
            stream (bool): 为True时，流式返回，需要将message.content.answer拼接起来才是完整的回答；为False时，对应非流式返回
            tools(list[Union[data_class.Tool,Manifest,data_class.MCPTool]]): 一个Tool或Manifest组成的列表，其中每个Tool(Manifest)对应一个工具的配置, 默认为None
            tool_outputs(list[data_class.ToolOutput]): 工具输出列表，格式为list[ToolOutput], ToolOutputd内容为本地的工具执行结果，以自然语言/json dump str描述，默认为None
            tool_choice(data_class.ToolChoice): 控制大模型使用组件的方式，默认为None
            end_user_id (str): 用户ID，用于区分不同用户
            action(data_class.Action): 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息。
            kwargs: 其他参数

        Returns:
            message (Message): 对话结果，一个Message对象，使用message.content获取内容。
        """

        if len(conversation_id) == 0:
            raise ValueError(
                "conversation_id is empty, you can run self.create_conversation to get a conversation_id"
            )

        if query == "" and (tool_outputs is None or len(tool_outputs) == 0):
            raise ValueError(
                "AppBuilderClient Run API: query and tool_outputs cannot both be empty"
            )

        if not tool_outputs:
            self._mcp_context = None
        formatted_tools = []
        if tools:
            formatted_tools = [
                data_class.ToAppBuilderTool(tool)[0] for tool in tools
            ]
            for tool in tools:
                _, is_mcp_tool = data_class.ToAppBuilderTool(tool)
                if is_mcp_tool and self._mcp_context is None:
                    self._mcp_context = "client"

        req = data_class.AppBuilderClientRequest(
            app_id=self.app_id,
            conversation_id=conversation_id,
            query=query,
            stream=True if stream else False,
            file_ids=file_ids,
            tools=formatted_tools,
            tool_outputs=tool_outputs,
            tool_choice=tool_choice,
            end_user_id=end_user_id,
            action=action,
        )

        headers = self.http_client.auth_header_v2(mcp_context=self._mcp_context)
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/app/conversation/runs")
        response = await self.http_client.session.post(
            url, headers=headers, json=req.model_dump(), timeout=None
        )
        await self.http_client.check_response_header(response)
        request_id = await self.http_client.response_request_id(response)
        if stream:
            client = AsyncSSEClient(response)
            return Message(content=self._iterate_events(request_id, client.events()))
        else:
            data = await response.json()
            resp = data_class.AppBuilderClientResponse(**data)
            out = data_class.AppBuilderClientAnswer()
            AppBuilderClient._transform(resp, out)
            return Message(content=out)

    async def upload_local_file(self, conversation_id, local_file_path: str) -> str:
        r"""异步运行，上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式

        该接口用于在对话中上传文件供大模型处理，文件的有效期为7天并且不超过对话的有效期。一次只能上传一个文件。

        Args:
            conversation_id (str) : 会话ID
            local_file_path (str) : 本地文件路径

        Returns:
            response (str): 唯一文件ID

        """
        return await self.upload_local_file(conversation_id, local_file_path)

    async def upload_file(self, conversation_id, local_file_path: str=None, file_url: str=None) -> str:
        r"""异步运行，上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式

        该接口用于在对话中上传文件供大模型处理，文件的有效期为7天并且不超过对话的有效期。一次只能上传一个文件。

        Args:
            conversation_id (str) : 会话ID
            local_file_path (str) : 本地文件路径
            file_url (str) : 文件URL

        Returns:
            response (str): 唯一文件ID

        """
        if len(conversation_id) == 0:
            raise ValueError(
                "conversation_id is empty, you can run self.create_conversation to get a conversation_id"
            )

        if local_file_path is None and file_url is None:
            raise ValueError(
                "local_file_path and file_url cannot both be empty"
            )
        if local_file_path:
            filepath = os.path.abspath(local_file_path)
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"{filepath} does not exist")

        multipart_form_data = FormData()
        multipart_form_data.add_field(name="app_id", value=self.app_id)
        multipart_form_data.add_field(
            name="conversation_id", value=conversation_id)

        if local_file_path:
            multipart_form_data.add_field(
                name="file",
                value=open(local_file_path, "rb"),
                filename=os.path.basename(local_file_path),
            )
        else:
            multipart_form_data.add_field(name="file_url", value=file_url)

        headers = self.http_client.auth_header_v2()
        url = self.http_client.service_url_v2("/app/conversation/file/upload")
        response = await self.http_client.session.post(
            url, data=multipart_form_data, headers=headers
        )
        await self.http_client.check_response_header(response)
        data = await response.json()
        resp = data_class.FileUploadResponse(**data)
        return resp.id

    async def run_with_handler(
        self,
        conversation_id: str,
        query: str = "",
        file_ids: list = [],
        tools: list[Union[data_class.Tool, Manifest, data_class.MCPTool]] = None,
        stream: bool = False,
        event_handler=None,
        action=None,
        **kwargs,
    ):
        r"""异步运行智能体应用，并通过事件处理器处理事件

        Args:
            conversation_id (str): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
            query (str): 查询字符串
            file_ids (list): 文件ID列表
            tools(list[Union[data_class.Tool,Manifest,data_class.MCPTool]], 可选): 一个Tool或Manifest组成的列表，其中每个Tool(Manifest)对应一个工具的配置, 默认为None
            stream (bool): 是否流式响应
            event_handler (EventHandler): 事件处理器
            action(data_class.Action) 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息。
            kwargs: 其他参数

        Returns:
            EventHandler: 事件处理器
        """
        assert event_handler is not None, "event_handler is None"
        await event_handler.init(
            appbuilder_client=self,
            conversation_id=conversation_id,
            query=query,
            file_ids=file_ids,
            tools=tools,
            stream=stream,
            action=action,
            **kwargs,
        )

        return event_handler

    async def run_multiple_dialog_with_handler(
        self,
        conversation_id: str,
        queries: iter = None,
        file_ids: iter = None,
        tools: iter = None,
        stream: bool = False,
        event_handler=None,
        actions: iter = None,
        **kwargs,
    ):
        r"""运行智能体应用，并通过事件处理器处理事件

        Args:
            conversation_id (str): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
            queries (iter): 查询字符串可迭代对象
            file_ids (iter): 文件ID列表
            tools(iter, 可选): 一个Tool或Manifest组成的列表，其中每个Tool(Manifest)对应一个工具的配置, 默认为None
            stream (bool): 是否流式响应
            event_handler (EventHandler): 事件处理器
            actions(iter) 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息。

            kwargs: 其他参数
        Returns:
            EventHandler: 事件处理器
        """
        assert event_handler is not None, "event_handler is None"
        assert queries is not None, "queries is None"

        iter_queries = iter(queries)
        iter_file_ids = iter(file_ids) if file_ids else iter([])
        iter_tools = iter(tools) if tools else iter([])
        iter_actions = iter(actions) if actions else iter([])

        for index, query in enumerate(iter_queries):
            file_id = next(iter_file_ids, None)
            tool = next(iter_tools, None)
            action = next(iter_actions, None)

            if index == 0:
                await event_handler.init(
                    appbuilder_client=self,
                    conversation_id=conversation_id,
                    query=query,
                    file_ids=file_id,
                    tools=tool,
                    stream=stream,
                    action=action,
                    **kwargs,
                )
                yield event_handler
            else:
                await event_handler.new_dialog(
                    query=query,
                    file_ids=file_id,
                    tools=tool,
                    stream=stream,
                    action=action,
                )
                yield event_handler
        await event_handler.reset_state()

    @staticmethod
    async def _iterate_events(request_id, events):
        async for event in events:
            try:
                data = event.data
                if len(data) == 0:
                    data = event.raw
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise AppBuilderServerException(
                    request_id=request_id,
                    message="json decoder failed {}".format(str(e)),
                )
            inp = data_class.AppBuilderClientResponse(**data)
            out = data_class.AppBuilderClientAnswer()
            AppBuilderClient._transform(inp, out)
            yield out
