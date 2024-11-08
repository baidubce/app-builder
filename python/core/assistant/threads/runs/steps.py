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
from appbuilder.utils.trace.tracer_wrapper import assistent_tool_trace

class Steps():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    @assistent_tool_trace
    def list(self, thread_id: str, run_id: str, limit: int = 20,
                   order: str = 'desc', after: str = "", before: str = "") -> thread_type.RunStepListResponse:
        """
        根据thread_id和run_id，列出对应run的历史step记录
        
        Args:
            thread_id (str): 线程ID
            run_id (str): 运行ID
            limit (int, optional): 步骤数量限制，默认为20
            order (str, optional): 排序方式，'asc'表示升序，'desc'表示降序，默认为'desc'
            after (str, optional): 过滤出时间戳晚于此值的步骤，默认为空
            before (str, optional): 过滤出时间戳早于此值的步骤，默认为空
        
        Returns:
            thread_type.RunStepListResponse: 线程运行步骤列表的响应对象
        """
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

    @assistent_tool_trace
    def query(self, thread_id: str, run_id: str, step_id: str) -> thread_type.RunStepResult:
        """
        根据thread_id，run_id和step_id，查询对应step的信息
        
        Args:
            thread_id (str): 线程ID
            run_id (str): 运行ID
            step_id (str): 步骤ID
        
        Returns:
            thread_type.RunStepResult: 步骤运行结果
        """
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