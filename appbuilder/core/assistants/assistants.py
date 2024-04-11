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
from appbuilder.core.assistants.assistant_config import AssistantConfig
from appbuilder.core.assistants import data_class
from appbuilder.core._client import HTTPClient

class Assistant(object):
    def __init__(self, assistant_config: AssistantConfig, id:str = "", created_at: int = 0, user_storage: str=""):
        self._assistant_config = assistant_config
        self._id = id
        self._created_at = created_at
        self._user_storage = user_storage

    @property
    def id(self):
        return self._id
    
    @property
    def assistant_config(self):
        return self._assistant_config
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def user_storage(self):
        return self._user_storage
    
    def __str__(self) -> str:
        return "Assistant(id={}, assistant_config={})".format(self._id, self._assistant_config)     
    
    def __repr__(self) -> str:
        return self.__str__()

class Assistants(object):
    def __init__(self):
        self._http_client = HTTPClient()
        

    def create(self, assistant_config: AssistantConfig) -> Assistant:
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] =  os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/assistants"

        print(assistant_config.to_base_model())
        req = data_class.AssistantCreateRequest(**assistant_config.to_base_model())

        response = self._http_client.session.post(
            url = url,
            headers = headers,
            json = req.model_dump(),
            timeout = None
        )
        data = response.json()
        print(data)
        resp = data_class.AssistantCreateResponse(**data)

        id = resp.id
        created_at = resp.created_at
        user_storage = resp.user_storage
        assistant_config = AssistantConfig(**data)

        return Assistant(assistant_config, id=id, created_at=created_at, user_storage=user_storage)


    def delete(self, assistant_id: str) -> None:
        pass

    def update(self, assistant_id: str, assistant_config: AssistantConfig) -> Assistant:
        pass

    def retrieve(self, assistant_id: str) -> Assistant:
        pass

    def list(self) -> list:
        pass


if __name__ == '__main__':
    os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
    os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"
    

    assistant_config = AssistantConfig(
        name="test_assistant",
        description="test_desc",
    )

    assistants = Assistants()
    assistant = assistants.create(assistant_config)
    print(assistant)
    print(assistant.id)