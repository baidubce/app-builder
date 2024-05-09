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
import json
from typing import Optional
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.utils.sse_util import SSEClient

class Steps():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    def list(self, thread_id: str, run_id: str, limit: int = 20,
                   order: str = 'desc', after: str = "", before: str = "") -> thread_type.RunStepListResponse:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/steps/list")
        req = thread_type.AssistantRunStepListRequest(
            thread_id=thread_id,
            run_id=run_id,
            limit=limit,
            order=order,
            after=after,
            before=before
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
        resp = thread_type.RunStepListResponse(**data)
        return resp

    def query(self, thread_id: str, run_id: str, step_id: str) -> thread_type.RunStepResult:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/steps/query")
        req = thread_type.AssistantRunStepQueryRequest(
            thread_id=thread_id,
            run_id=run_id,
            step_id=step_id
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
        resp = thread_type.RunStepResult(**data)
        return resp