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
from appbuilder.core.assistant.type import thread_class
from appbuilder.core._client import AssistantHTTPClient

class Threads():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    def create(self, messages: Optional[list[thread_class.AssistantMessage]] = []) -> thread_class.ThreadCreateResponse:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads")
        
        req = thread_class.ThreadCreateRequest(
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

        response = thread_class.ThreadCreateResponse(**data)
        return response


if __name__ == '__main__':
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"
    message = thread_class.AssistantMessage(content="hello")
    conversations = Threads().create([message])
    print(conversations)
