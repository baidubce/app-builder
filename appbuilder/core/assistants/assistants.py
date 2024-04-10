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

from appbuilder.core.assistants.assistant_config import AssistantConfig

class Assistant(object):
    def __init__(self, assistant_config: AssistantConfig):
        self._assistant_config = assistant_config
        self._id = ""
    
    @property
    def id(self):
        return self._id
    

    def create_conversations(self) -> str:
        pass 

    def run(self, conversation_id: str, query:str, file_ids: list = [], stream: bool=False) -> Message:
        pass
        

class Assistants(object):
    def create(self, assistant_config: AssistantConfig) -> Assistant:
        pass 

    def delete(self, assistant_id: str) -> None:
        pass 

    def update(self, assistant_id:str, assistant_config: AssistantConfig) -> Assistant:
        pass 

    def retrieve(self, assistant_id: str) -> Assistant:
        pass 

    def list(self) -> list:
        pass 

