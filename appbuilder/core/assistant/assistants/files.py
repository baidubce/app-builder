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
from appbuilder.core.assistants import data_class
from appbuilder.core._client import HTTPClient

class AssistantFile(object):
    def __init__(self, id:str, bytes:int=0, purpose:str="", create_at:int=0, filename:str="", classification_id:str="", **kwargs):
        self._id = id
        self._bytes = bytes
        self._purpose = purpose
        self._create_at = create_at
        self._filename = filename
        self._classification_id = classification_id

    @property
    def id(self):
        return self._file_id
    
    @property
    def bytes(self):
        return self._bytes
    
    @property
    def purpose(self):
        return self._purpose
    
    @property
    def create_at(self):
        return self._create_at
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def classification_id(self):
        return self._classification_id
    
    def __str__(self) -> str:
        return f"id: {self._id}, bytes: {self._bytes}, purpose: {self._purpose}, create_at: {self._create_at}, filename: {self._filename}, classification_id: {self._classification_id}"

    def __repr__(self) -> str:
        return self.__str__()

class Files(object):
    def __init__(self):
        self._http_client = HTTPClient()

    def add_docments(self, file_path:str, purpose:list):
        return self.create(file_path, purpose)

    def create(self, file_path:str, purpose:str="") -> AssistantFile:
        headers = self._http_client.auth_header()
        headers["Authorization"] =  os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/files"

        form_data = {
            'file': (os.path.basename(file_path), open(file_path, 'rb')),
        }
        response = self._http_client.session.post(
            url,
            headers=headers,
            files = form_data,
            params={
                'purpose': purpose
            }
        )
        
        data = response.json()
        print(data)

        resp = data_class.AssistantFilesCreateResponse(**data)
        return AssistantFile(**resp.__dict__)
        

    def delete(self, file_id:str):
        pass

    def retrieve(self, file_id:str) -> AssistantFile:
        pass

    def list(self) -> list:
        pass


if __name__ == '__main__':
    os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
    os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"
    
    file = Files().create("/Users/chengmo/workspace/刘鑫的简历.pdf", "test")
    print(file)
