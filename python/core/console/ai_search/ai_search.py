# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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
from appbuilder.core.component import Message, Component
from appbuilder.core.console.ai_search import data_class
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core._exception import AppBuilderServerException


class AISearch(Component):

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def run(self,
            messages,
            search_source=None,
            resource_type_filter=None,
            search_filter=None,
            search_recency_filter=None,
            search_domain_filter=None,
            model=None,
            instruction=None,
            temperature=None,
            top_p=None,
            prompt_template=None,
            search_mode=None,
            enable_reasoning=None,
            enable_deep_search=None,
            additional_knowledge=None,
            max_completion_tokens=None,
            response_format="auto",
            enable_corner_markers=True,
            enable_followup_queries=False,
            stream=False,
            safety_level=None,
            max_refer_search_items=None,
            config_id=None,
            model_appid=None):
        req = data_class.AISearchRequest(
            messages=messages,
            search_source=search_source,
            resource_type_filter=resource_type_filter,
            search_filter=search_filter,
            search_recency_filter=search_recency_filter,
            search_domain_filter=search_domain_filter,
            model=model,
            instruction=instruction,
            temperature=temperature,
            top_p=top_p,
            prompt_template=prompt_template,
            search_mode=search_mode,
            enable_reasoning=enable_reasoning,
            enable_deep_search=enable_deep_search,
            additional_knowledge=additional_knowledge,
            max_completion_tokens=max_completion_tokens,
            response_format=response_format,
            enable_corner_markers=enable_corner_markers,
            enable_followup_queries=enable_followup_queries,
            stream=stream,
            safety_level=safety_level,
            max_refer_search_items=max_refer_search_items,
            config_id=config_id,
            model_appid=model_appid
        )
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = self.http_client.service_url_v2("/ai_search/chat/completions")
        response = self.http_client.session.post(
            url, headers=headers, json=req.model_dump(exclude_none=True), timeout=None, stream=True
        )
        self.http_client.check_response_header(response)
        request_id = self.http_client.response_request_id(response)
        if stream:
            client = SSEClient(response)
            return Message(content=self._iterate_events(request_id, client.events()))
        else:
            data = response.json()
            resp = data_class.AISearchResponse(**data)
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
            resp = data_class.AISearchResponse(**data)
            yield resp
