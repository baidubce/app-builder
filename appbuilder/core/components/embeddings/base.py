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

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments


class EmbeddingBaseComponent(Component):
    """
    EmbeddingBaseComponent
    """
    
    name: str
    version: str
    meta: ComponentArguments
    base_url: str = ""
    model_type: str = "embeddings"


    @abstractmethod
    def run(self, text: Union[Message[str], str]) -> Message[List[float]]:
        """
        Args:
            message: str
        Returns:
            embeddings: List[float]
        """

    async def arun(self, text: Union[Message[str], str]) -> Message[List[float]]:
        """
        Args:
            message: str
        Returns:
            embeddings: List[float]
        """

        # embedding don't need be async, just return it
        return self.run(text)

    @abstractmethod
    def batch(self, texts: Union[Message[List[str]], List[str]]) -> Message[List[List[float]]]:
        """
        Args:
            message: List[str]
        Returns:
            embeddings: List[List[float]]
        """

    def abatch(self, texts: Union[Message[List[str]], List[str]]) -> Message[List[List[float]]]:
        """
        Args:
            message: List[str]
        Returns:
            embeddings: List[List[float]]
        """

        # embedding don't need be async, just return it
        return self.batch(texts)
    

class EmbeddingArgs(ComponentArguments):
    """
    ernie bot embedding配置

    Attributes:
        text (Union[Message[str], str]): 输入文本
    """
    text: Union[Message[str], str]
