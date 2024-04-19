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
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.assistant.type import data_class
from appbuilder.core._client import HTTPClient
from pydantic import BaseModel

class Conversation():
    def __init__(self, id: str, messages: list[data_class.AssistantMessage]):
        self._id = id
        self._messages = messages

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def messages(self) -> list:
        return self._messages
    
    def __str__(self) -> str:
        return "Conversation(id={}, messages={})".format(self._id, self._messages)

    def __repr__(self) -> str:
        return self.__str__()


class Conversations():
    def __init__(self) -> None:
        self._http_client = HTTPClient()

    def create(self, messages: list = []) -> Conversation:
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] =  os.getenv("APPBUILDER_TOKEN", "")
        
        url = "http://10.45.86.48/api/v1/threads"
        
        req = data_class.ConversationCreateRequest(
            messages=messages)

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        data = response.json()
        resp = data_class.ConversationCreateResponse(**data)
        return Conversation(resp.id, messages)

    def delete(self, conversation_id: str) -> None:
        pass

if __name__ == '__main__':
    os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
    os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"
    
    message = data_class.AssistantMessage(content="hello")
    conversations = Conversations().create([message])
    print(conversations)
