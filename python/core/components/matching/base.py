"""
base
"""

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


from abc import abstractmethod
from typing import List, Union

from appbuilder.core.message import Message
from appbuilder.core.component import Component
from appbuilder.core.component import ComponentArguments


class MatchingArgs(ComponentArguments):
    """Matching Args"""

    query: Union[str, Message[str]]
    contexts: Union[List[str], Message[List[str]]]


class MatchingBaseComponent(Component):
    """
    MatchingBaseComponent
    """

    name: str
    version: str
    meta: MatchingArgs

    @abstractmethod
    def run(
        self,
        query: Union[Message[str], str],
        contexts: Union[Message[List[str]], List[str]],
    ) -> Message[List[str]]:
        """
        Args:
            query: Union[Message[str], str]
            contexts: Union[Message[List[str]], List[str]]
        Returns:
            Message[List[str]]: contexts which has been Matched
        """
