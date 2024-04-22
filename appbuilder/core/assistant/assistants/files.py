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

# -*- coding: utf-8 -*-


import os
import json
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core._client import AssistantHTTPClient


class Files(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    def create(self, file_path: str, purpose: str = "assistant") -> assistant_type.AssistantFilesCreateResponse:
        """
        上传文件到助理存储中。
        
        Args:
            file_path (str): 要上传的文件路径。
            purpose (str, optional): 上传文件的用途。默认为 "assistant"。
        
        Returns:
            assistant_type.AssistantFilesCreateResponse: 上传文件后返回的响应对象。
        
        Raises:
            ValueError: 如果指定的文件路径不存在，则会引发此异常。
        """
        headers = self._http_client.auth_header()
        headers.pop("Content-Type")
        url = self._http_client.service_url("/v2/storage/files")

        if not os.path.exists(file_path):
            raise ValueError("File {} not exists".format(file_path))

        with open(file_path, 'rb') as f:
            files = [
                ('file',(os.path.basename(file_path), f))
            ]

            response = self._http_client.session.post(
                url,
                headers=headers,
                files=files,
                params={
                    'purpose': purpose
                }
            )

        self._http_client.check_response_header(response)

        request_id = self._http_client.response_request_id(response)
        data = response.json()

        self._http_client.check_assistant_response(request_id, data)
        resp = assistant_type.AssistantFilesCreateResponse(**data)
        return resp
