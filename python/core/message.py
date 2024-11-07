# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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



import uuid

from pydantic import BaseModel
from typing import Optional, TypeVar, Generic


_T = TypeVar("_T")


class Message(BaseModel, Generic[_T], extra='allow'):
    """
    Message class

    Attributes:
        content: The message content
        name: The message name
        mtype: The message type
        id: The message id
    """
    content: Optional[_T] = {}
    name: Optional[str] = "msg"
    mtype: Optional[str] = "dict"
    id: Optional[str] = str(uuid.uuid4())

    def __init__(self, content: Optional[_T] = None, **data):
        if content is not None:
            data['content'] = content
        super().__init__(**data)
        self.mtype = type(self.content).__name__

    def __str__(self):
        return f"Message(name={self.name}, content={self.content}, mtype={self.mtype})"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, content={self.content!r}, mtype={self.mtype!r})"