"""
Matching
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


from typing import List, Union

import numpy as np

from appbuilder.core.message import Message
from appbuilder.core.components.embeddings import EmbeddingBaseComponent

from .base import MatchingBaseComponent, MatchingArgs


class Matching(MatchingBaseComponent):
    """
    Matching

    基于Embedding类型的文本表示模型，输入query和文本列表，对其进行排序或者相似度计算

    Examples:

        .. code-block:: python

            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            # 初始化所需要的组件
            embedding = appbuilder.Embedding()
            matching = appbuilder.Matching(embedding)

            # 定义输入query和文本列表
            query = appbuilder.Message("你好")
            contexts = appbuilder.Message(["世界", "你好"])

            # 根据query，对文本列表做相似度排序
            contexts_matched = matching(query, contexts)
            print(contexts_matched.content)
            # ['你好', '世界']
    """

    name: str = "Matching"
    version: str = "v1"
    meta: MatchingArgs = MatchingArgs

    def __init__(
        self,
        embedding_component: EmbeddingBaseComponent,
    ):
        """
        EmbeddingBaseComponent: 用于计算文本的embedding
        """
        
        self.embedding_component = embedding_component
        super().__init__(self.meta)

    def run(
        self,
        query: Union[Message[str], str],
        contexts: Union[Message[List[str]], List[str]],
        return_score: bool=False,
    ) -> Message[List[str]]:
        """
        Args:
            query: Union[Message[str], str]
            contexts: Union[Message[List[str]], List[str]]
        Returns:
            Message[List[str]]: contexts which has been matched
        """

        query_embedding = self.embedding_component(query)
        contexts_embedding = self.embedding_component.batch(contexts)

        sematic = self.semantics(query_embedding, contexts_embedding)

        combined = list(zip(sematic.content, contexts.content))
        sorted_combined = sorted(combined, reverse=True)

        if return_score:
            return Message([(item[0], item[1]) for item in sorted_combined])
        else:
            return Message([item[1] for item in sorted_combined])

    def _cosine_similarity(self, X, Y):
        """
        Args:
            X: 长度为 1 x n 的矩阵
            Y: 长度为 m x n 的矩阵
        Returns:
            长度为 m x 1 的矩阵，每个元素表示 X 与 Y的对应行m 的余弦相似度
        """

        X_norm = X / np.linalg.norm(X)
        Y_norm = Y / np.linalg.norm(Y, axis=1, keepdims=True)

        similarity = np.dot(Y_norm, X_norm.T)
        return similarity

    def semantics(
        self,
        query_embedding: Union[Message[List[float]], List[float]],
        context_embeddings: Union[Message[List[List[float]]], List[List[float]]],
    ) -> Message[List[float]]:
        """
        输入query和context的embedding，输出他们的相似度
        其中：
            query_embedding是一个长度为 n 的数组，表示仅有一个query
            context_embeddings是一个长度为 m x n 的矩阵，m表示有m个候选context

        Args:
            query_embedding: Union[Message[List[float]], List[float]]
            context_embeddings: Union[Message[List[List[float]]], List[List[float]]]
        Returns:
            Message[float] 
        """

        _query_embedding = query_embedding.content if isinstance(query_embedding, Message) else query_embedding
        _context_embeddings = context_embeddings.content if isinstance(context_embeddings, Message) else context_embeddings

        similarity_matrix = self._cosine_similarity([_query_embedding], _context_embeddings)
        similarity_matrix = similarity_matrix.flatten().tolist()

        return Message(similarity_matrix)
