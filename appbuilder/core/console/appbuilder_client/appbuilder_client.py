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
from typing import Optional
from appbuilder.core.component import Message, Component
from appbuilder.core.console.appbuilder_client import data_class
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core._client import HTTPClient
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.logger_util import logger
from appbuilder.utils.trace.tracer_wrapper import client_run_trace, client_tool_trace


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
    response_per_time = get_app_list(limit=100)
    list_len_per_time = len(response_per_time)
    if list_len_per_time != 0:
        app_list.extend(response_per_time)
    while list_len_per_time == 100:
        after_id = response_per_time[-1].id
        response_per_time = get_app_list(after=after_id, limit=100)
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
        if len(conversation_id) == 0:
            raise ValueError("conversation_id is empty, you can run self.create_conversation to get a conversation_id")

        filepath = os.path.abspath(local_file_path)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} does not exist")

        multipart_form_data = {
            "file": (os.path.basename(local_file_path), open(local_file_path, "rb")),
            "app_id": (None, self.app_id),
            "conversation_id": (None, conversation_id),
        }
        headers = self.http_client.auth_header_v2()
        url = self.http_client.service_url_v2("/app/conversation/file/upload")
        response = self.http_client.session.post(
            url, files=multipart_form_data, headers=headers
        )
        self.http_client.check_response_header(response)
        data = response.json()
        resp = data_class.FileUploadResponse(**data)
        return resp.id

    @client_run_trace
    def run(self, conversation_id: str,
            query: str = "",
            file_ids: list = [],
            stream: bool = False,
            tools: list[data_class.Tool] = None,
            tool_outputs: list[data_class.ToolOutput] = None,
            tool_choice: data_class.ToolChoice = None,
            end_user_id: str = None,
            **kwargs
            ) -> Message:
        r"""运行智能体应用
        
        Args:
            query (str): query内容
            conversation_id (str): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
            file_ids(list[str]): 文件ID列表
            stream (bool): 为True时，流式返回，需要将message.content.answer拼接起来才是完整的回答；为False时，对应非流式返回
            tools(list[data_class.Tools]): 一个Tools组成的列表，其中每个Tools对应一个工具的配置, 默认为None
            tool_outputs(list[data_class.ToolOutput]): 工具输出列表，格式为list[ToolOutput], ToolOutputd内容为本地的工具执行结果，以自然语言/json dump str描述，默认为None
            tool_choice(data_class.ToolChoice): 控制大模型使用组件的方式，默认为None
            end_user_id (str): 用户ID，用于区分不同用户
            kwargs: 其他参数
            
        Returns: 
            message (obj: `Message`): 对话结果，一个Message对象，使用message.content获取内容。
        """

        if len(conversation_id) == 0:
            raise ValueError(
                "conversation_id is empty, you can run self.create_conversation to get a conversation_id"
            )

        if query == "" and (tool_outputs is None or len(tool_outputs) == 0):
            raise ValueError("AppBuilderClient Run API: query and tool_outputs cannot both be empty")

        req = data_class.AppBuilderClientRequest(
            app_id=self.app_id,
            conversation_id=conversation_id,
            query=query,
            stream=True if stream else False,
            file_ids=file_ids,
            tools=tools,
            tool_outputs=tool_outputs,
            tool_choice=tool_choice,
            end_user_id=end_user_id,
        )

        headers = self.http_client.auth_header_v2()
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
            _transform(resp, out)
            return Message(content=out)

    def run_with_handler(self,
                        conversation_id: str,
                        query: str = "",
                        file_ids: list = [],
                        tools: list[data_class.Tool] = None,
                        stream: bool = False,
                        event_handler = None,
                        **kwargs):
        r"""运行智能体应用，并通过事件处理器处理事件

        Args:
            conversation_id (str): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
            query (str): 查询字符串
            file_ids (list): 文件ID列表
            tools(list[data_class.Tools], 可选): 一个Tools组成的列表，其中每个Tools对应一个工具的配置, 默认为None
            stream (bool): 是否流式响应
            event_handler (EventHandler): 事件处理器
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
            **kwargs
        )

        return event_handler

    @staticmethod
    def _iterate_events(request_id, events) -> data_class.AppBuilderClientAnswer:
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
            _transform(inp, out)
            yield out

    @staticmethod
    def _check_console_response(request_id: str, data):
        if data["code"] != 0:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data["code"],
                service_err_message="message={}".format(data["message"]),
            )


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


def _transform(
    inp: data_class.AppBuilderClientResponse, out: data_class.AppBuilderClientAnswer
):
    out.answer = inp.answer
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
