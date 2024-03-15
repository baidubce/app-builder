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
import importlib
import os
import random
import string
from typing import Dict, Any
from appbuilder.core.component import Component, Message
from appbuilder.core.components.embeddings.component import Embedding
from appbuilder.core.constants import GATEWAY_URL
from appbuilder.utils.logger_util import logger


class BESVectorStoreIndex:
    """
    BES向量存储检索工具
    """
    base_es_url: str = "/v1/bce/bes/cluster/"

    def __init__(self, cluster_id, user_name, password, embedding=None, index_name=None,
                 index_type="hnsw", prefix="/rpc/2.0/cloud_hub"):

        if embedding is None:
            embedding = Embedding()

        self.embedding = embedding
        self.index_name = index_name if index_name else BESVectorStoreIndex.generate_id()
        self.index_type = index_type
        self.prefix = prefix

        self._es = None
        self._helpers = None
        self.bes_client = self._create_bes_client(cluster_id, user_name, password)

    @property
    def es(self):
        self._lazy_import_es()
        return self._es

    @property
    def helpers(self):
        self._lazy_import_es()
        return self._helpers

    def _lazy_import_es(self):
        if self._es is None or self._helpers is None:
            try:
                from elasticsearch import Elasticsearch, helpers
                self._es = Elasticsearch
                self._helpers = helpers
            except ImportError:
                raise ImportError("Elasticsearch module is not installed. "
                                  "Please install it using 'pip install elasticsearch==7.11.0'.")

    @staticmethod
    def generate_id(length=16):
        """
        生成随机的ID
        """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _create_bes_client(self, cluster_id, user_name, password):
        """
        创建一个bes的client
        """
        secret_key = os.getenv("APPBUILDER_TOKEN")
        if not secret_key.startswith("Bearer"):
            secret_key = "Bearer {}".format(secret_key)

        gateway = os.getenv("GATEWAY_URL") if os.getenv("GATEWAY_URL") else GATEWAY_URL

        connection_params = {
            "hosts": [gateway + self.prefix + self.base_es_url + cluster_id],
            "http_auth": (user_name, password),
            "headers": {'X-Appbuilder-Authorization': f"{secret_key}"}
        }

        bes_client = self.es(**connection_params)

        try:
            bes_client.info()
        except Exception as e:
            logger.error("connecting to bes error: {}".format(e))
            raise ConnectionError(e)

        return bes_client

    def as_retriever(self):
        """
        转化为retriever
        """
        return BESRetriever(embedding=self.embedding, index_name=self.index_name, bes_client=self.bes_client,
                            index_type=self.index_type)

    @staticmethod
    def create_index_mappings(index_type, vector_dims):
        """
        创建索引的mapping
        """
        mappings = {
            'properties': {
                "vector": {
                    "type": "bpack_vector",
                    "dims": vector_dims,
                },
            }
        }
        if index_type == "hnsw":
            mappings["properties"]["vector"]["index_type"] = "hnsw"
            mappings["properties"]["vector"]["space_type"] = "cosine"
            mappings["properties"]["vector"]["parameters"] = {"m": 4, "ef_construction": 200}
        return mappings

    def add_segments(self, segments: Message, metadata=""):
        """
        向bes中插入数据
        参数:
            query (Message[str]): 需要插入的内容
        返回:
        """
        segment_vectors = self.embedding.batch(segments)
        segment_vectors = segment_vectors.content
        vector_dims = len(segment_vectors[0])
        segments = segments.content
        documents = [
            {"_index": self.index_name,
             "_source": {"text": segment, "vector": vector, "metadata": metadata,
                         "id": BESVectorStoreIndex.generate_id()}}
            for segment, vector in zip(segments, segment_vectors)]

        mappings = BESVectorStoreIndex.create_index_mappings(self.index_type, vector_dims)
        self.bes_client.indices.create(index=self.index_name,
                                       body={"settings": {"index": {"knn": True}}, "mappings": mappings})
        self.helpers.bulk(self.bes_client, documents)

    @classmethod
    def from_segments(cls, segments, cluster_id, user_name, password, embedding=None, **kwargs):
        """
        根据段落创建一个bes向量索引
        参数：
            segments: 切分的文本段落
            cluster_id: bes集群ID
            user_name: bes用户名
            password: bes用户密码
            embedding: 文本段落embedding工具
            kwargs: 其他初始化参数
        返回：
            bes索引实例
        """
        if embedding is None:
            embedding = Embedding()

        index_name = kwargs.get("index_name", None)
        index_type = kwargs.get("index_type", "hnsw")
        prefix = kwargs.get("prefix", "/rpc/2.0/cloud_hub")

        vector_index = cls(cluster_id, user_name, password, embedding, index_name, index_type, prefix)
        vector_index.add_segments(segments)
        return vector_index

    def delete_all_segments(self):
        """
        删除索引中的全部内容
        """
        query = {
            'query': {
                'match_all': {}
            }
        }
        resp = self.bes_client.delete_by_query(index=self.index_name, body=query)
        logger.debug("deleted {} documents in index {}".format(resp['deleted'], self.index_name))

    def get_all_segments(self):
        """
        获取索引中的全部内容
        """
        query = {
            'query': {
                'match_all': {}
            }
        }
        return self.bes_client.search(index=self.index_name, body=query)


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

    def run(self, query: Message, top_k: int = 1):
        """
        根据query进行查询
        参数:
            query (Message[str]): 需要查询的内容，
            top_k (bool): 查询结果中匹配度最高的top_k个结果
        返回:
            obj (Message[Dict]): 查询到的结果，包含文本和匹配得分。
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
