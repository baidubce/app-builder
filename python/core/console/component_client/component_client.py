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

"""组件"""
import json
from appbuilder.core.component import Component, Message
from appbuilder.core.console.component_client import data_class
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.logger_util import logger
from appbuilder.utils.trace.tracer_wrapper import client_run_trace
from appbuilder.utils.sse_util import SSEClient


class ComponentClient(Component):
    def __init__(self, **kwargs):
        r"""初始化

        Returns:
            response (obj: `ComponentClient`): 组件实例
        """
        super().__init__(**kwargs)

    @client_run_trace
    def run(
        self,
        component_id: str,
        sys_origin_query: str,
        version: str = None,
        action: str = None,
        stream: bool = False,
        sys_file_urls: dict = None,
        sys_conversation_id: str = None,
        sys_end_user_id: str = None,
        sys_chat_history: list = None,
        **kwargs,
    ) -> Message:
        """ 组件运行
        Args:
            component_id (str): 工作流组件ID或官方组件名称
            sys_origin_query (str): 用户输入的原始查询语句
            version (str): 组件版本号
            action (str): 组件动作
            stream (bool): 是否流式返回
            sys_file_urls (dict): 文件地址
            sys_conversation_id (str): 会话ID
            sys_end_user_id (str): 用户ID
            sys_chat_history (list): 聊天
            kwargs: 其他参数
        Returns:
            message (Message): 对话结果，一个Message对象，使用message.content获取内容。
        """
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"

        url_suffix = f"/components/{component_id}"
        if version is not None:
            url_suffix += f"/version/{version}"
        if action is not None:
            url_suffix += f"?action={action}"
        url = self.http_client.service_url_v2(url_suffix)

        all_params = {
            '_sys_origin_query': sys_origin_query,
            '_sys_file_urls': sys_file_urls,
            '_sys_conversation_id': sys_conversation_id,
            '_sys_chat_history': sys_chat_history,
            '_sys_end_user_id': sys_end_user_id,
            **kwargs
        }
        parameters = data_class.RunRequest.Parameters(**all_params)
        request = data_class.RunRequest(
            stream=stream,
            parameters=parameters,
        )

        response = self.http_client.session.post(
            url,
            headers=headers,
            json=request.model_dump(exclude_none=True, by_alias=True),
            timeout=None,
        )
        request_id = self.http_client.check_response_header(response)

        if stream:
            client = SSEClient(response)
            return Message(content=self._iterate_events(request_id, client.events()))
        else:
            data = response.json()
            resp = data_class.RunResponse(**data)
            return Message(content=resp)

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
            resp = data_class.RunResponse(**data)
            yield resp
