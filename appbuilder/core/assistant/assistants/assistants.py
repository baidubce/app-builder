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
from appbuilder.core.assistant.type import assistant_type
from appbuilder.utils.collector import Collector
from appbuilder.utils.collector import AssistantKeys
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.core.assistant.assistants.files import Files


class Assistants(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    @property
    def files(self):
        return Files()


    def create(self,
               name: str,
               description: str,
               assistant_id: Optional[str] = "",
               model: Optional[str] = "ERNIE-4.0-8K",
               response_format: Optional[str] = 'text',
               instructions: Optional[str] = "你是百度制作的AI助手",
               thought_instructions: Optional[str] = "",
               chat_instructions: Optional[str] = "",
               tools: Optional[list[assistant_type.AssistantTool]] = [],
               file_ids: Optional[list[str]] = [],
               metadata: Optional[dict] = {},
               ) -> assistant_type.AssistantCreateResponse:
        """
        创建助手实例
        
        Args:
            name (str): 助手名称
            description (str): 助手描述
            assistant_id (Optional[str], optional): 助手ID. Defaults to "".
            model (Optional[str], optional): 模型名称. Defaults to "ERNIE-4.0-8K".
            response_format (Optional[str], optional): 响应格式. Defaults to 'text'.
            instructions (Optional[str], optional): 指令. Defaults to "".
            thought_instructions (Optional[str], optional): 思考指令. Defaults to "".
            chat_instructions (Optional[str], optional): 聊天指令. Defaults to "".
            tools (Optional[list[assistant_type.AssistantTool]], optional): 工具列表. Defaults to [].
            file_ids (Optional[list[str]], optional): 文件ID列表. Defaults to [].
            metadata (Optional[dict], optional): 元数据. Defaults to {}.
        
        Returns:
            assistant_type.AssistantCreateResponse: 助手创建响应
        
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants")

        req = assistant_type.AssistantCreateRequest(
            name=name,
            description=description,
            assistant_id=assistant_id,
            model=model,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            tools=tools,
            file_ids=file_ids,
            metadata=metadata,
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

        resp = assistant_type.AssistantCreateResponse(**data)
        Collector().add_to_collection(AssistantKeys.ASSISTANT, resp, resp.id)
        return resp