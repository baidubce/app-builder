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


class BetaAssistant(object):
    @property
    def assistants(self):
        from appbuilder.core.assistant.assistants import Assistants
        return Assistants()
    
    @property
    def threads(self):
        from appbuilder.core.assistant.threads import Threads
        return Threads()
    
    @property
    def type(self):
        from appbuilder.core.assistant import type
        return type
    
    @property
    def assistant_type(self):
        from appbuilder.core.assistant.type import assistant_type
        return assistant_type
    
    @property
    def thread_type(self):
        from appbuilder.core.assistant.type import thread_type
        return thread_type
    
    @property
    def public_type(self):
        from appbuilder.core.assistant.type import public_type
        return public_type

assistant = BetaAssistant()
