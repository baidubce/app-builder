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
from appbuilder.core.assistants import data_class
from appbuilder.core._client import HTTPClient
from typing import Optional
from typing import Union
from appbuilder.core.assistants.data_class import AssistantMessage

class Messages(object):
    def __init__(self):
        self._http_client = HTTPClient()

    def create(self, conversation_id: str, content: str, role: str = "user", file_ids: Optional[list[str]] = []) -> data_class.AssistantMessageCreateResponse:
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] =  os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/threads/messages"
        
        req = data_class.AssistantMessageCreateRequest(
            thread_id=conversation_id,
            content=content,
            role=role,
            file_ids=file_ids
        )

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )

        data = response.json()
        resp = data_class.AssistantMessageCreateResponse(**data)

        return resp


if __name__ == "__main__":
    os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
    os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"
    
    from appbuilder.core.assistants.conversations.conversations import Conversations
    conversation = Conversations().create()
    message = Messages().create(
        conversation_id = conversation.id, 
        content="hello")
    print(message)
