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

from appbuilder.core.message import Message
from appbuilder.core.components.embeddings import EmbeddingBaseComponent
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace

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

    @components_run_trace
    def run(
        self,
        query: Union[Message[str], str],
        contexts: Union[Message[List[str]], List[str]],
        return_score: bool=False,
    ) -> Message[List[str]]:
        """
        根据给定的查询和上下文，返回匹配的上下文列表。
        
        Args:
            query (Union[Message[str], str]): 查询字符串或Message对象，包含查询字符串。
            contexts (Union[Message[List[str]], List[str]]): 上下文字符串列表或Message对象，包含上下文字符串列表。
            return_score (bool, optional): 是否返回匹配得分。默认为False。
        
        Returns:
            Message[List[str]]: 匹配的上下文列表。如果return_score为True，则返回包含得分和上下文的元组列表；否则仅返回上下文列表。
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

    def _dot_product(self, v1, v2):
        """
        计算两个向量的点积。
        
        Args:
            v1 (list): 第一个向量，元素为数值类型。
            v2 (list): 第二个向量，元素为数值类型，长度应与v1相同。
        
        Returns:
            float: 向量v1和v2的点积结果。
        
        Raises:
            ValueError: 如果v1和v2的长度不相等。
        """

        return sum(x1 * x2 for x1, x2 in zip(v1, v2))

    def _vector_norm(self, v):
        """
        计算向量的欧几里得范数（L2范数）。
        
        Args:
            v (list of float): 输入的向量，其中每个元素都是浮点数。
        
        Returns:
            float: 向量的欧几里得范数。
        
        """
        return sum(x**2 for x in v) ** 0.5

    def _cosine_similarity(self, X, Y):
        """
        计算向量X与矩阵Y中每一行的余弦相似度。
        
        Args:
            X (list or numpy.ndarray): 待计算的单个向量，长度为n的列表或一维numpy数组。
            Y (list of lists or numpy.ndarray): 包含多个向量的矩阵，每个向量长度为n的列表的列表或二维numpy数组。
        
        Returns:
            list: 包含X与Y中每一行向量余弦相似度的列表。
        
        """
        if len(X) == 1:
            X = X[0]

        norm_X = self._vector_norm(X)
        similarities = []
        
        for row in Y:
            dot_prod = self._dot_product(X, row)
            norm_row = self._vector_norm(row)
            if norm_X != 0 and norm_row != 0:
                similarity = dot_prod / (norm_X * norm_row)
            else:
                similarity = 0  
            
            similarities.append(similarity)
        
        return similarities

    def semantics(
        self,
        query_embedding: Union[Message[List[float]], List[float]],
        context_embeddings: Union[Message[List[List[float]]], List[List[float]]],
    ) -> Message[List[float]]:
        """
        计算query和context的相似度
        
        Args:
            query_embedding (Union[Message[List[float]], List[float]]): query的embedding，长度为n的数组
            context_embeddings (Union[Message[List[List[float]]], List[List[float]]]): context的embedding，长度为m x n的矩阵，其中m表示候选context的数量
        
        Returns:
            Message[List[float]]: query和所有候选context的相似度列表
        
        """
        _query_embedding = query_embedding.content if isinstance(query_embedding, Message) else query_embedding
        _context_embeddings = context_embeddings.content if isinstance(context_embeddings, Message) else context_embeddings

        similarity_scores = self._cosine_similarity([_query_embedding], _context_embeddings)
        similarity_scores = list(similarity_scores)

        return Message(similarity_scores)
