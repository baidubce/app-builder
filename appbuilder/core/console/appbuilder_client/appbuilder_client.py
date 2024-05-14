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

from appbuilder.core.component import Message, Component
from appbuilder.core.console.appbuilder_client import data_class
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.sse_util import SSEClient
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.logger_util import logger


class AppBuilderClient(Component):
    r"""
    AppBuilderClient 组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)平台上
    构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。
        Examples:
        ... code-block:: python
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
                参数:
                    app_id (str: 必须) : 应用唯一ID
                返回：
                    response (obj: `AppBuilderClient`): 智能体实例
        """
        super().__init__(**kwargs)
        if (not isinstance(app_id, str)) or len(app_id) == 0:
            raise ValueError("app_id must be a str, and length is bigger then zero,"
                             "please go to official website which is 'https://cloud.baidu.com/product/AppBuilder'"
                             " to get a valid app_id after your application is published.")
        self.app_id = app_id

    def create_conversation(self) -> str:
        r"""创建会话并返回会话ID，会话ID在服务端用于上下文管理、绑定会话文档等，如需开始新的会话，请创建并使用新的会话ID
                参数:
                    无
                返回：
                    response (str: ): 唯一会话ID
        """
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/v2/app/conversation")
        response = self.http_client.session.post(
            url, headers=headers, json={"app_id": self.app_id}, timeout=None)
        self.http_client.check_response_header(response)
        data = response.json()
        resp = data_class.CreateConversationResponse(**data)
        return resp.conversation_id

    def upload_local_file(self, conversation_id, local_file_path: str) -> str:
        r"""上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式
                参数:
                    conversation_id (str: 必须) : 会话ID
                    local_file_path (str: 必须) : 本地文件路径
                返回：
                    response (str: ): 唯一文件ID
            """

        if len(conversation_id) == 0:
            raise ValueError(
                "conversation_id is empty, you can run self.create_conversation to get a conversation_id")
        multipart_form_data = {
            'file': (os.path.basename(local_file_path), open(local_file_path, 'rb')),
            'app_id': (None, self.app_id),
            'conversation_id': (None, conversation_id),
        }
        headers = self.http_client.auth_header_v2()
        url = self.http_client.service_url_v2(
            "/v2/app/conversation/file/upload")
        response = self.http_client.session.post(
            url, files=multipart_form_data, headers=headers)
        self.http_client.check_response_header(response)
        data = response.json()
        resp = data_class.FileUploadResponse(**data)
        return resp.id

    def run(self, conversation_id: str,
            query: str,
            file_ids: list = [],
            stream: bool = False,
            ) -> Message:
        r""" 动物识别
                参数:
                    query (str: 必须): query内容
                    conversation_id (str, 必须): 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
                    file_ids(list[str], 可选):
                    stream (bool, 可选): 为True时，流式返回，需要将message.content.answer拼接起来才是完整的回答；为False时，对应非流式返回
                返回: message (obj: `Message`): 对话结果.
        """

        if len(conversation_id) == 0:
            raise ValueError(
                "conversation_id is empty, you can run self.create_conversation to get a conversation_id"
            )

        req = data_class.AppBuilderClientRequest(
            app_id=self.app_id,
            conversation_id=conversation_id,
            query=query,
            stream=True if stream else False,
            file_ids=file_ids,
        )

        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/v2/app/conversation/runs")
        response = self.http_client.session.post(
            url, headers=headers, json=req.model_dump(), timeout=None, stream=True)
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

    @staticmethod
    def _iterate_events(request_id, events) -> data_class.AppBuilderClientAnswer:
        for event in events:
            try:
                data = event.data
                if len(data) == 0:
                    data = event.raw
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise AppBuilderServerException(request_id=request_id, message="json decoder failed {}".format(str(e)))
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
                service_err_message="message={}".
                format(data["message"])
            )


class AgentBuilder(AppBuilderClient):
    @deprecated
    def __init__(self, app_id: str):
        """
        初始化方法，用于创建一个新的实例对象。

        为了避免歧义，减少用户上手门槛，推荐使用该类调用AgentBuilder

        Args:
            app_id (str): 应用程序的唯一标识符。

        Returns:
            None

        """
        logger.info("AgentBuilder is deprecated, please use AppBuilderClient instead")
        super().__init__(app_id)


def _transform(inp: data_class.AppBuilderClientResponse, out: data_class.AppBuilderClientAnswer):
    out.answer = inp.answer
    for ev in inp.content:
        event = data_class.Event(
            code=ev.event_code,
            message=ev.event_message,
            status=ev.event_status,
            event_type=ev.event_type,
            content_type=ev.content_type,
            detail=ev.outputs
        )
        out.events.append(event)
