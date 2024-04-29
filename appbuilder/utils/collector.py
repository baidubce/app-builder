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

import collections

class AssistantKeys(object):
    ASSISTANT = "assistant"
    CONVERSATION = "conversation"
    FILE = "file"
    RUN = "run"
    MESSAGE = "message"


class Collector():
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._collections = collections.OrderedDict()

    def add_to_collection(self, name, value, index_key=None):
        assert isinstance(name, str)
        if name not in self._collections:
            self._collections[name] = collections.OrderedDict()

        if index_key is not None:
            self._collections[name][index_key] = value
        else:
            index = len(self._collections[name])
            self._collections[name][str(index)] = value

    def del_collection(self, name, index_key=None):
        assert isinstance(name, str)
        if name not in self._collections:
            return

        if index_key is not None:
            del self._collections[name][index_key]
        else:
            del self._collections[name]

    def get_collection(self, name, index_key=None, scope=None):
        collection = self._collections.get(name, None)
        if collection is None:
            if index_key is None:
                return []
            else:
                return None

        if index_key is not None:
            return collection.get(index_key, None)
        else:
            return list(collection.values())

    def get_collection_as_dict(self, name, reverse=False):
        if name in self._collections:
            if reverse:
                return collections.OrderedDict(zip(self._collections[name].values(), self._collections[name].keys()))
            else:
                return collections.OrderedDict(self._collections[name])
        else:
            self._collections[name] = collections.OrderedDict()
            return self._collections[name]

    def get_all_collection_keys(self, name=None):
        return list(self._collections.keys())

    def clear_collection(self, name):
        if name in self._collections:
            del self._collections[name]