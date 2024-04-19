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
from appbuilder.core.assistant.type import assistant_class
from appbuilder.core._client import AssistantHTTPClient


class Files(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    def add_docments(self, file_path: str, purpose: list):
        return self.create(file_path, purpose)

    def create(self, file_path: str, purpose: str = "assistant") -> assistant_class.AssistantFilesCreateResponse:
        headers = self._http_client.auth_header()
        headers["Content-Type"] = "form-data"
        url = self._http_client.service_url("/v2/storage/files")

        if not os.path.exists(file_path):
            raise ValueError("File {} not exists".format(file_path))

        form_data = {
            'file': (os.path.basename(file_path), open(file_path, 'rb')),
        }

        print("form_data", form_data)

        response = self._http_client.session.post(
            url,
            headers=headers,
            files=form_data,
            params={
                'purpose': purpose
            }
        )

        request_id = self._http_client.response_request_id(response)
        data = response.json()
        self._http_client.check_assistant_response(request_id, data)
        resp = assistant_class.AssistantFilesCreateResponse(**data)
        return resp


if __name__ == '__main__':
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"

    file = Files().create("/Users/chengmo/workspace/刘鑫的简历.pdf", "test")
    print(file)
