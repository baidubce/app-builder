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
from typing import Optional
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.threads.messages import Messages
from appbuilder.core.assistant.threads.runs import Runs
from appbuilder.core._client import AssistantHTTPClient

class Threads():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    @property
    def messages(self) -> Messages:
        return Messages()
    
    @property
    def runs(self) -> Runs:
        return Runs()

    def create(self, messages: Optional[list[thread_type.AssistantMessage]] = []) -> thread_type.ThreadCreateResponse:
        """
        创建一个新的对话线程。
        
        Args:
            messages: 要发送给助手的消息列表。如果不传入此参数，则会创建一个空对话线程。
        
        Returns:
            一个ThreadCreateResponse对象，包含新创建的线程的相关信息。
        
        Raises:
            ValueError: 如果传入的messages参数不是列表类型。
        
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads")
        
        if  not isinstance(messages, list):
            raise ValueError("Threads().create() messages must be a list, but got: {}".format(messages))

        req = thread_type.ThreadCreateRequest(
            messages=messages)

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        response = thread_type.ThreadCreateResponse(**data)
        return response
