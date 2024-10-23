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


# -*- coding: utf-8 -*-
"""
基于Baidu VDB的retriever
"""
from typing import Dict, Any
from appbuilder.core.component import Component, Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

from .model import *

class BaiduVDBRetriever(Component):
    """
    向量检索组件，用于检索和query相匹配的内容

    Examples:

    .. code-block:: python

        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'

        segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
        vector_index = appbuilder.BaiduVDBVectorStoreIndex.from_params(
                self.instance_id,
                self.api_key,
        )
        vector_index.add_segments(segments)

        query = appbuilder.Message("文心一言")
        time.sleep(5)
        retriever = vector_index.as_retriever()
        res = retriever(query)

    """
    name: str = "BaiduVectorDBRetriever"
    tool_desc: Dict[str, Any] = {
        "description": "a retriever based on Baidu VectorDB"}

    def __init__(self, embedding, table):
        super().__init__()

        self.embedding = embedding
        self.table = table

    @components_run_trace
    def run(self, query: Message, top_k: int = 1):
        """
        根据query进行查询
        
        Args:
            query (Message[str]): 需要查询的内容，类型为Message，包含要查询的文本。
            top_k (int, optional): 查询结果中匹配度最高的top_k个结果，默认为1。
        
        Returns:
            Message[Dict]: 查询到的结果，包含文本和匹配得分。
        
        Raises:
            TypeError: 如果query不是Message类型，或者top_k不是整数类型。
            ValueError: 如果top_k不是正整数，或者query的内容为空字符串，或者长度超过512个字符。
        
        """
        from pymochow.model.table import AnnSearch, HNSWSearchParams
        from pymochow.model.enum import ReadConsistency

        if not isinstance(query, Message):
            raise TypeError("Parameter `query` must be a Message, but got {}"
                            .format(type(query)))
        if not isinstance(top_k, int):
            raise TypeError("Parameter `top_k` must be a int, but got {}"
                            .format(type(top_k)))
        if top_k <= 0:
            raise ValueError("Parameter `top_k` must be a positive integer, but got {}"
                             .format(top_k))

        content = query.content
        if not isinstance(content, str):
            raise ValueError("Parameter `query` content is not a string, got: {}"
                             .format(type(content)))
        if len(content) == 0:
            raise ValueError("Parameter `query` content is empty")
        if len(content) > 512:
            raise ValueError(
                "Parameter `query` content is too long, max length per batch size is 512")

        query_embedding = self.embedding(query)
        anns = AnnSearch(
            vector_field=FIELD_VECTOR,
            vector_floats=query_embedding.content,
            params=HNSWSearchParams(ef=10, limit=top_k),
        )
        res = self.table.search(
            anns=anns, read_consistency=ReadConsistency.STRONG)
        rows = res.rows
        docs = []
        if rows is None or len(rows) == 0:
            return Message(docs)

        for row in rows:
            row_data = row.get("row", {})
            docs.append({
                "text": row_data.get(FIELD_TEXT),
                "meta": row_data.get(FIELD_METADATA),
                "score": row.get("score")
            })

        return Message(docs)
