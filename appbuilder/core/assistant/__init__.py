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

from appbuilder.core.assistants.assistants import (
    Assistants,
    Assistant
)

from appbuilder.core.assistants.assistant_config import (
    AssistantConfig
)

from appbuilder.core.assistants.files import (
    AssistantFile,
    Files
)

from appbuilder.core.assistants.messages.messages import (
    Messages,
    AssistantMessage
)

from appbuilder.core.assistants.conversations.conversations import (
    Conversation,
    Conversations
)

from appbuilder.core.assistants.runs.runs import (
    Runs
)

from appbuilder.core.assistants import (
    data_class
)

class BetaAssistant(object):
    @property
    def assistants(self):
        return Assistants()
    
    @property
    def conversations(self):
        return Conversations()
    
    @property
    def files(self):
        return Files()
    
    @property
    def messages(self):
        return Messages()
    

    @property
    def runs(self):
        return Runs()
    


assistants = BetaAssistant()