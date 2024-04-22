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
from appbuilder.core.assistant.type import thread_type
from appbuilder.core._client import AssistantHTTPClient
from typing import Optional


class Messages(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    def create(self, 
               thread_id: str,
               content: str,
               role: Optional[str] = "user",
               file_ids: Optional[list[str]] = []) -> thread_type.AssistantMessageCreateResponse:
        """
        创建一条消息。
        
        Args:
            thread_id (str): 线程ID。
            content (str): 消息内容。
            role (Optional[str], optional): 角色，可选值为"user"或"assistant"。默认为"user"。
            file_ids (Optional[list[str]], optional): 消息中包含的文件ID列表。默认为空列表。
        
        Returns:
            thread_type.AssistantMessageCreateResponse: 消息创建响应对象。
        
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/messages")

        req = thread_type.AssistantMessageCreateRequest(
            thread_id=thread_id,
            content=content,
            role=role,
            file_ids=file_ids
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

        response = thread_type.AssistantMessageCreateResponse(**data)
        return response
