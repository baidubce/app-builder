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
基于baidu ES的retriever
"""
from typing import Dict, Any
from appbuilder.core.component import Component, Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

from .model import *

class BESRetriever(Component):
    """
    向量检索组件，用于检索和query相匹配的内容

    Examples:

    .. code-block:: python

        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'

        segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
        vector_index = appbuilder.BESVectorStoreIndex.from_segments(segments, self.cluster_id, self.username,
                                                                    self.password)
        query = appbuilder.Message("文心一言")
        time.sleep(5)
        retriever = vector_index.as_retriever()
        res = retriever(query)

    """
    name: str = "BaiduElasticSearchRetriever"
    tool_desc: Dict[str, Any] = {"description": "a retriever based on Baidu ElasticSearch"}
    base_es_url: str = "/v1/bce/bes/cluster/"

    def __init__(self, embedding, index_name, bes_client, index_type="hnsw"):
        super().__init__()

        self.embedding = embedding
        self.index_name = index_name
        self.bes_client = bes_client
        self.index_type = index_type

    @components_run_trace
    def run(self, query: Message, top_k: int = 1):
        """
        根据query进行查询
        
        Args:
            query (Message[str]): 需要查询的内容，以Message对象的形式传递。
            top_k (int, optional): 查询结果中匹配度最高的top_k个结果。默认为1。
        
        Returns:
            obj (Message[Dict]): 查询到的结果，包含文本、元数据以及匹配得分，以Message对象的形式返回。
        
        """
        query_embedding = self.embedding(query)
        vector_query = {"vector": query_embedding.content, "k": top_k}
        if self.index_type == "linear":
            vector_query["linear"] = True
        else:
            vector_query["ef"] = 10

        query_body = {
            "size": top_k,
            "query": {"knn": {"vector": vector_query}}
        }
        res = self.bes_client.search(index=self.index_name, body=query_body)
        docs = []
        for r in res["hits"]["hits"]:
            docs.append({"text": r["_source"]["text"], "meta": r["_source"]["metadata"], "score": r["_score"]})

        return Message(docs)
