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

from appbuilder import Message
from appbuilder.core.assistants import data_class
from appbuilder.core._client import HTTPClient
from typing import Optional
import json


class AssistantMessage(Message):
    def __init__(self, content, role: str = "user", file_ids: list[str] = [], **data):
        if content is not None:
            data['content'] = content
        super().__init__(**data)
        self.role = role
        self.file_ids = file_ids

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "role": self.role,
            "file_ids": self.file_ids
        }

    def __str__(self):
        return f"Message(name={self.name}, content={self.content}, role={self.role}, file_ids={self.file_ids})"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, content={self.content!r}, role={self.role!r}, file_ids={self.file_ids!r})"


class Messages(object):
    def __init__(self):
        self._client = HTTPClient()

    def create(self, conevrsion_id: str, content: str, role: Optional[str] = "user", file_ids: Optional[list[str]] = []) -> AssistantMessage:
        pass


if __name__ == "__main__":
    message = AssistantMessage("test", role="user", file_ids=[])
    print(message)
    print(json.dumps(message.to_dict(), ensure_ascii=False, indent=4))
    print(json.dumps([message.to_dict()]))
