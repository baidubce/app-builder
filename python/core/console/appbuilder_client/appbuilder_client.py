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

"""AppBuilderClient组件"""
import os
import json
import uuid
import queue
from typing import Optional, Union
from appbuilder.core.component import Message, Component
from appbuilder.core.manifest.models import Manifest
from appbuilder.core.console.appbuilder_client import data_class
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core._client import HTTPClient
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.trace.tracer_wrapper import client_run_trace, client_tool_trace


@deprecated(reason="use describe_apps instead")
@client_tool_trace
def get_app_list(
    limit: int = 10,
    after: str = "",
    before: str = "",
    secret_key: Optional[str] = None,
    gateway_v2: Optional[str] = None,
) -> list[data_class.AppOverview]:
    """
    该接口查询用户下状态为已发布的应用列表

    Args:
        limit (int, optional): 返回结果的最大数量，默认值为10。
        after (str, optional): 返回结果中第一个应用的游标值，用于分页查询。默认值为空字符串。
        before (str, optional): 返回结果中最后一个应用的游标值，用于分页查询。默认值为空字符串。
        secret_key (Optional[str], optional): 认证密钥。如果未指定，则使用默认的密钥。默认值为None。
        gateway_v2 (Optional[str], optional): 网关地址。如果未指定，则使用默认的地址。默认值为None。

    Returns:
        list[data_class.AppOverview]: 应用列表。

    """

    client = HTTPClient(secret_key=secret_key, gateway_v2=gateway_v2)
    headers = client.auth_header_v2()
    headers["Content-Type"] = "application/json"
    url = client.service_url_v2("/apps")

    request = data_class.AppBuilderClientAppListRequest(
        limit=limit, after=after, before=before
    )

    response = client.session.get(
        url=url,
        headers=headers,
        params=request.model_dump(),
    )

    client.check_console_response(response)
    client.check_response_header(response)
    data = response.json()
    resp = data_class.AppBuilderClientAppListResponse(**data)
    out = resp.data
    return out


@client_tool_trace
def describe_apps(
    marker: Optional[str] = None,
    maxKeys: int = 10,
    secret_key: Optional[str] = None,
    gateway: Optional[str] = None,
) -> list[data_class.AppOverview]:
    """
    该接口查询用户下状态为已发布的应用列表

    Args:
        maxKeys (int, optional): 返回结果的最大数量，默认值为10，最大为100。
        marker (str, optional): 起始位置，即从哪个游标开始查询，默认值为空字符串。
        secret_key (Optional[str], optional): 认证密钥。如果未指定，则使用默认的密钥。默认值为None。
        gateway (Optional[str], optional): 网关地址。如果未指定，则使用默认的地址。默认值为None。

    Returns:
        DescribeAppsResponse: 应用列表。

    """
    client = HTTPClient(secret_key=secret_key, gateway_v2=gateway)
    headers = client.auth_header_v2()
    headers["Content-Type"] = "application/json"
    url = client.service_url_v2("/app?Action=DescribeApps")
    request = data_class.DescribeAppsRequest(MaxKeys=maxKeys, Marker=marker)
    response = client.session.post(
        url=url,
        json=request.model_dump(),
        headers=headers,
    )

    client.check_response_header(response)
    data = response.json()
    resp = data_class.DescribeAppsResponse(**data)
    out = resp.data
    return out


@client_tool_trace
def get_all_apps():
    """
    获取所有应用列表。

    Args:
        无参数。

    Returns:
        List[App]: 包含所有应用信息的列表，每个元素为一个App对象，
        其中App对象的结构取决于get_app_list函数的返回结果。

    """
    app_list = []
    response_per_time = describe_apps(maxKeys=100)
    list_len_per_time = len(response_per_time)
    if list_len_per_time != 0:
        app_list.extend(response_per_time)
    while list_len_per_time == 100:
        after_id = response_per_time[-1].id
        response_per_time = describe_apps(marker=after_id, maxKeys=100)
        list_len_per_time = len(response_per_time)
        if list_len_per_time != 0:
            app_list.extend(response_per_time)

    return app_list


class AppBuilderClient(Component):
    r"""
    AppBuilderClient 组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)平台上
    构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。

    Examples:

    .. code-block:: python

        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'
        # 可在Console 应用页面获取
        app_id = "app_id"
        client = appbuilder.AppBuilderClient("app_id")
        conversation_id = client.create_conversation()
        file_id = client.upload_local_file(conversation_id, "/path/to/file")
        message = client.run(conversation_id, "今天你好吗？")
        # 打印对话结果
        print(message.content)

    """

    def __init__(self, app_id: str, **kwargs):
        r"""初始化智能体应用

        Args:
            app_id (str: 必须) : 应用唯一ID

        Returns:
            response (obj: `AppBuilderClient`): 智能体实例
        """
        super().__init__(**kwargs)
        if (not isinstance(app_id, str)) or len(app_id) == 0:
            raise ValueError(
                "app_id must be a str, and length is bigger then zero,"
                "please go to official website which is 'https://cloud.baidu.com/product/AppBuilder'"
                " to get a valid app_id after your application is published."
            )
        self.app_id = app_id
        self._mcp_context = None

    @client_tool_trace
    def create_conversation(self) -> str:
        r"""创建会话并返回会话ID

        会话ID在服务端用于上下文管理、绑定会话文档等，如需开始新的会话，请创建并使用新的会话ID

        Args:
            无

        Returns:
            response (str): 唯一会话ID

        """
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/app/conversation")
        response = self.http_client.session.post(
            url, headers=headers, json={"app_id": self.app_id}, timeout=None
        )
        self.http_client.check_response_header(response)
        data = response.json()
        resp = data_class.CreateConversationResponse(**data)
        return resp.conversation_id

    @client_tool_trace
    def upload_local_file(self, conversation_id, local_file_path: str) -> str:
        r"""上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式

        该接口用于在对话中上传文件供大模型处理，文件的有效期为7天并且不超过对话的有效期。一次只能上传一个文件。

        Args:
            conversation_id (str) : 会话ID
            local_file_path (str) : 本地文件路径

        Returns:
            response (str): 唯一文件ID
        """
        return self.upload_file(conversation_id, local_file_path=local_file_path)

    @client_tool_trace
    def upload_file(self, conversation_id, local_file_path: str=None, file_url: str=None) -> str:
        r"""上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式

        该接口用于在对话中上传文件供大模型处理，文件的有效期为7天并且不超过对话的有效期。一次只能上传一个文件。

        Args:
            conversation_id (str) : 会话ID
            local_file_path (str) : 本地文件路径
            file_url(str): 待上传的文件url

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
                raise FileNotFoundError(f"{filepath} and {file_url} does not exist")

        headers = self.http_client.auth_header_v2()
        url = self.http_client.service_url_v2("/app/conversation/file/upload")

        multipart_form_data = {
            "app_id": (None, self.app_id),
            "conversation_id": (None, conversation_id),
        }
        if local_file_path:
            multipart_form_data["file"] = (
                os.path.basename(local_file_path),
                open(local_file_path, "rb"),
            )
        else:
            multipart_form_data["file_url"] = (None, file_url)
        response = self.http_client.session.post(
            url, files=multipart_form_data, headers=headers
        )

        self.http_client.check_response_header(response)
        data = response.json()
        resp = data_class.FileUploadResponse(**data)
        return resp.id

    @client_run_trace
    def run(
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
        r"""运行智能体应用

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
        response = self.http_client.session.post(
            url, headers=headers, json=req.model_dump(), timeout=None, stream=True
        )
        self.http_client.check_response_header(response)
        request_id = self.http_client.response_request_id(response)
        if stream:
            client = SSEClient(response)
            return Message(content=self._iterate_events(request_id, client.events()))
        else:
            data = response.json()
            resp = data_class.AppBuilderClientResponse(**data)
            out = data_class.AppBuilderClientAnswer()
            AppBuilderClient._transform(resp, out)
            return Message(content=out)

    @client_run_trace
    def feedback(
        self,
        conversation_id: str,
        message_id: str,
        type: str,
        flag: list[str] = None,
        reason: str = None,
    ):
        r"""点踩点赞

        Args:
            conversation_id (str): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
            message_id (str): 消息ID，对话后会返回消息ID
            type (str): 点赞点踩枚举值 cancel：取消评论, upvote：点赞, downvote：点踩
            flag(list[str]): 点踩原因枚举值:答非所问、内容缺失、没有帮助、逻辑问题、偏见歧视、事实错误
            reason(str): 对于点赞点踩额外补充的原因。

        Returns:
            request_id (str): 请求ID
        """

        if len(conversation_id) == 0:
            raise ValueError(
                "conversation_id is empty, you can run self.create_conversation to get a conversation_id"
            )

        req = data_class.FeedbackRequest(
            app_id=self.app_id,
            conversation_id=conversation_id,
            message_id=message_id,
            type=type,
            flag=flag,
            reason=reason,
        )

        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/app/conversation/feedback")
        response = self.http_client.session.post(
            url, headers=headers, json=req.model_dump(exclude_none=True), timeout=None, stream=True
        )
        self.http_client.check_response_header(response)
        request_id = self.http_client.response_request_id(response)
        return request_id

    def run_with_handler(
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
        r"""运行智能体应用，并通过事件处理器处理事件

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
        event_handler.init(
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

    def run_multiple_dialog_with_handler(
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
                yield from self.run_with_handler(
                    conversation_id=conversation_id,
                    query=query,
                    file_ids=file_id,
                    tools=tool,
                    stream=stream,
                    event_handler=event_handler,
                    action=action,
                    **kwargs,
                )
            else:
                event_handler.new_dialog(
                    query=query,
                    file_ids=file_id,
                    tools=tool,
                    stream=stream,
                    action=action,
                )
                yield event_handler
        event_handler.reset_state()

    @staticmethod
    def _iterate_events(request_id, events):
        for event in events:
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

    @staticmethod
    def _check_console_response(request_id: str, data):
        if data["code"] != 0:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data["code"],
                service_err_message="message={}".format(data["message"]),
            )

    @staticmethod
    def _transform(
        inp: data_class.AppBuilderClientResponse, out: data_class.AppBuilderClientAnswer
    ):
        out.answer = inp.answer
        out.message_id = inp.message_id
        for ev in inp.content:
            event = data_class.Event(
                code=ev.event_code,
                message=ev.event_message,
                status=ev.event_status,
                event_type=ev.event_type,
                content_type=ev.content_type,
                detail=ev.outputs,
                usage=ev.usage,
                tool_calls=ev.tool_calls,
            )
            out.events.append(event)


class AgentBuilder(AppBuilderClient):
    r"""AgentBuilder是继承自AppBuilderClient的一个子类，用于构建和管理智能体应用。
    支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)平台上
    构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。

    Examples:

    .. code-block:: python

        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'
        # 可在Console 应用页面获取
        app_id = "app_id"
        client = appbuilder.AppBuilderClient("app_id")
        conversation_id = client.create_conversation()
        file_id = client.upload_local_file(conversation_id, "/path/to/file")
        message = client.run(conversation_id, "今天你好吗？")
        # 打印对话结果
        print(message.content)

    """

    @deprecated(
        reason="AgentBuilder is deprecated, please use AppBuilderClient instead",
        version="1.0.0",
    )
    def __init__(self, app_id: str):
        r"""初始化方法，用于创建一个新的实例对象。

        为了避免歧义，减少用户上手门槛，推荐使用该类调用AgentBuilder

        Args:
            app_id (str): 应用程序的唯一标识符。

        Returns:
            response (obj: `AgentBuilder`): 智能体实例

        """
        super().__init__(app_id)
