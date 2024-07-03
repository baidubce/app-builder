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
from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional
from appbuilder.core._client import HTTPClient
from appbuilder.core.console.knowledge_base import data_class
from appbuilder.core.component import Message, Component
from appbuilder.utils.trace.tracer_wrapper import client_tool_trace


class KnowledgeBase(Component):

    def __init__(self, knowledge_id: Optional[str] = None, knowledge_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.knowledge_id = knowledge_id
        self.knowledge_name = knowledge_name

    @classmethod
    def create_knowledge(cls, knowledge_name: str) -> 'KnowledgeBase':
        payload = json.dumps({"name": knowledge_name})
        http_client = HTTPClient()
        headers = http_client.auth_header()
        headers["Content-Type"] = "application/json"
        create_url = "/v1/ai_engine/agi_platform/v1/datasets/create"
        response = http_client.session.post(url=http_client.service_url(create_url),
                                            headers=headers, data=payload)
        http_client.check_response_header(response)
        http_client.check_console_response(response)
        response = response.json()["result"]
        return KnowledgeBase(knowledge_id=response["id"], knowledge_name=response["name"])

    def upload_file(self, file_path: str) -> data_class.KnowledgeBaseUploadFileResponse:
        if not os.path.exists(file_path):
            raise FileNotFoundError("File {} does not exist".format(file_path))

        headers = self.http_client.auth_header_v2()
        url = self.http_client.service_url_v2("/file")

        with open(file_path, 'rb') as f:
            multipart_form_data = {
                'file': (os.path.basename(file_path), f)
            }

            response = self.http_client.session.post(
                url=url,
                headers=headers,
                files=multipart_form_data,
            )

            self.http_client.check_response_header(response)
            self.http_client.check_console_response(response)
            data = response.json()
            resp = data_class.KnowledgeBaseUploadFileResponse(**data)

        return resp

    def add_document(self,
                     content_type: str,
                     file_ids: list[str] = [],
                     is_enhanced: bool = False,
                     custom_process_rule: Optional[data_class.CustomProcessRule] = None,
                     knowledge_base_id: Optional[str] = None) -> data_class.KnowledgeBaseAddDocumentResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one")

        headers = self.http_client.auth_header_v2()
        headers['content-type'] = 'application/json'

        url = self.http_client.service_url_v2("/knowledge_base/document")

        request = data_class.KnowledgeBaseAddDocumentRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            content_type=content_type,
            file_ids=file_ids,
            is_enhanced=is_enhanced,
            custom_process_rule=custom_process_rule
        )

        response = self.http_client.session.post(
            url=url,
            headers=headers,
            json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()
        
        resp = data_class.KnowledgeBaseAddDocumentResponse(**data)
        return resp

    def delete_document(self, document_id: str, knowledge_base_id: Optional[str] = None) -> data_class.KnowledgeBaseDeleteDocumentResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one")

        headers = self.http_client.auth_header_v2()
        headers['content-type'] = 'application/json'

        url = self.http_client.service_url_v2("/knowledge_base/document")
        request = data_class.KnowledgeBaseDeleteDocumentRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            document_id=document_id
        )
        response = self.http_client.session.delete(
            url=url,
            headers=headers,
            params=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()
        
        resp = data_class.KnowledgeBaseDeleteDocumentResponse(**data)
        return resp

    def get_documents_list(self, limit: int = 10, after: Optional[str] = "", before: Optional[str] = "", knowledge_base_id: Optional[str] = None)->data_class.KnowledgeBaseGetDocumentsListResponse:
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one")

        headers = self.http_client.auth_header_v2()
        headers['content-type'] = 'application/json'

        url = self.http_client.service_url_v2("/knowledge_base/documents")
        request = data_class.KnowledgeBaseGetDocumentsListRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            limit=limit,
            after=after,
            before=before
        )
        response = self.http_client.session.get(
            url=url,
            headers=headers,
            params=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()
        
        resp = data_class.KnowledgeBaseGetDocumentsListResponse(**data)
        return resp
