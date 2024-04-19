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
from appbuilder.core.assistant.type import assistant_class
from appbuilder.utils.collector import Collector
from appbuilder.utils.collector import AssistantKeys
from appbuilder.core._client import AssistantHTTPClient


class Assistants(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    def create(self,
               name: str,
               description: str,
               assistant_id: Optional[str] = "",
               model: Optional[str] = "ERNIE-4.0-8K",
               response_format: Optional[str] = 'text',
               instructions: Optional[str] = "",
               thought_instructions: Optional[str] = "",
               chat_instructions: Optional[str] = "",
               tools: Optional[list[assistant_class.AssistantTool]] = [],
               file_ids: Optional[list[str]] = [],
               metadata: Optional[dict] = {},
               ) -> assistant_class.AssistantCreateResponse:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants")

        req = assistant_class.AssistantCreateRequest(
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
        self._http_client.check_assistant_response(data)
        
        resp = assistant_class.AssistantCreateResponse(**data)
        Collector().add_to_collection(AssistantKeys.ASSISTANT, resp, resp.id)
        return resp


if __name__ == '__main__':
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"

    test_file_ids = ["123"] * 11
    assistants = Assistants()
    assistant = assistants.create(
        name="Abc-_123",
        description="test",
    )
    print(assistant)
    print(assistant.id)