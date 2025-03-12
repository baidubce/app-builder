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
import os
import time
from typing import Dict, Any
from appbuilder.core.component import Component, Message
from appbuilder.core.components.embeddings.component import Embedding
from appbuilder.core.constants import GATEWAY_URL
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .model import *


def _try_import() -> None:
    try:
        import pymochow
    except ImportError:
        raise ImportError(
            "pymochow module is not installed. "
            "Please install it using 'pip install pymochow'."
        )

class TableParams:
    """
    Baidu VectorDB table params.
    See the following documentation for details:
    https://cloud.baidu.com/doc/VDB/s/mlrsob0p6
    
    Args:
        dimension int: The dimension of vector.
        replication int: The number of replicas in the table.
        partition int: The number of partitions in the table.
        index_type (Optional[str]): HNSW, FLAT... Default value is "HNSW"
        metric_type (Optional[str]): L2, COSINE, IP. Default value is "L2"
        drop_exists (Optional[bool]): Delete the existing Table. Default value is False.
        vector_params (Optional[Dict]):
          if HNSW set parameters: `M` and `efConstruction`, for example `{'M': 16, efConstruction: 200}`
          default is HNSW
    """

    def __init__(
        self,
        dimension: int,
        table_name: str = DEFAULT_TABLE_NAME,
        replication: int = DEFAULT_REPLICA,
        partition: int = DEFAULT_PARTITION,
        index_type: str = DEFAULT_INDEX_TYPE,
        metric_type: str = DEFAULT_METRIC_TYPE,
        drop_exists: bool = False,
        vector_params: Dict = None,
    ):
        self.dimension = dimension
        self.table_name = table_name
        self.replication = replication
        self.partition = partition
        self.index_type = index_type
        self.metric_type = metric_type
        self.drop_exists = drop_exists
        self.vector_params = vector_params


class BaiduVDBVectorStoreIndex:
    """
    Baidu VDB向量存储检索工具
    """
    vdb_uri_prefix = b"/api/v1/bce/vdb/instance/"

    def __init__(
        self,
        instance_id: str,
        api_key: str,
        account: str = DEFAULT_ACCOUNT,
        database_name: str = DEFAULT_DATABASE_NAME,
        table_params: TableParams = TableParams(dimension=384),
        embedding=None,
    ):
        if not isinstance(instance_id, str):
            raise TypeError(
                "Parameter `instance_id` must be a string, but got {}".format(
                    type(instance_id)))
        if not isinstance(api_key, str):
            raise TypeError(
                "Parameter `api_key` must be a string, but got {}".format(
                    type(api_key)))
        if not isinstance(account, str):
            raise TypeError(
                "Parameter `account` must be a string, but got {}".format(
                    type(account)))
        if not isinstance(database_name, str):
            raise TypeError(
                "Parameter `database_name` must be a string, but got {}".format(
                    type(database_name)))
        if not isinstance(table_params, TableParams):
            raise TypeError(
                "Parameter `table_params` must be a TableParams, but got {}".format(
                    type(table_params)))
        if embedding is not None and not isinstance(embedding, Embedding):
            raise TypeError(
                "Parameter `embedding` must be a Embedding, but got {}".format(
                    type(embedding)))

        if embedding is None:
            embedding = Embedding()

        self.embedding = embedding

        self._init_client(instance_id, account, api_key)
        self._create_database_if_not_exists(database_name)
        self._create_table(table_params)

    def _init_client(self, instance_id, account, api_key):
        """
        创建一个vdb的client
        """
        import pymochow
        from pymochow.configuration import Configuration
        from pymochow.auth.bce_credentials import AppBuilderCredentials

        gateway = os.getenv("GATEWAY_URL") if os.getenv(
            "GATEWAY_URL") else GATEWAY_URL
        appbuilder_token = os.getenv("APPBUILDER_TOKEN")
        uri_prefix = self.vdb_uri_prefix + instance_id.encode('utf-8')

        config = Configuration(
            credentials=AppBuilderCredentials(
                account, api_key, appbuilder_token),
            endpoint=gateway,
            uri_prefix=uri_prefix,
            connection_timeout_in_mills=DEFAULT_TIMEOUT_IN_MILLS,
        )
        self.vdb_client = pymochow.MochowClient(config)

    def _create_database_if_not_exists(self, database_name: str) -> None:
        db_list = self.vdb_client.list_databases()

        if database_name in [db.database_name for db in db_list]:
            self.database = self.vdb_client.database(database_name)
        else:
            self.database = self.vdb_client.create_database(database_name)

    def _create_table(self, table_params: TableParams) -> None:
        import pymochow

        if table_params is None:
            raise ValueError(VALUE_NONE_ERROR.format("table_params"))

        try:
            self.table = self.database.describe_table(table_params.table_name)
            if table_params.drop_exists:
                self.database.drop_table(table_params.table_name)
                # wait db release resource
                time.sleep(5)
                self._create_table_in_db(table_params)
        except pymochow.exception.ServerError:
            self._create_table_in_db(table_params)

    def _create_table_in_db(
        self,
        table_params: TableParams,
    ) -> None:
        from pymochow.model.enum import FieldType
        from pymochow.model.schema import Field, Schema, SecondaryIndex, VectorIndex
        from pymochow.model.table import Partition

        index_type = self._get_index_type(table_params.index_type)
        metric_type = self._get_metric_type(table_params.metric_type)
        vector_params = self._get_index_params(index_type, table_params)
        fields = []
        fields.append(
            Field(
                FIELD_ID,
                FieldType.UINT64,
                primary_key=True,
                partition_key=True,
                auto_increment=True,
                not_null=True,
            )
        )
        fields.append(Field(FIELD_METADATA, FieldType.STRING))
        fields.append(Field(FIELD_TEXT, FieldType.STRING))
        fields.append(
            Field(
                FIELD_VECTOR,
                FieldType.FLOAT_VECTOR,
                dimension=table_params.dimension,
                not_null=True,
            )
        )

        indexes = []
        indexes.append(
            VectorIndex(
                index_name=INDEX_VECTOR,
                index_type=index_type,
                field=FIELD_VECTOR,
                metric_type=metric_type,
                params=vector_params,
            )
        )

        schema = Schema(fields=fields, indexes=indexes)
        self.table = self.database.create_table(
            table_name=table_params.table_name,
            replication=table_params.replication,
            partition=Partition(partition_num=table_params.partition),
            schema=Schema(fields=fields, indexes=indexes),
            enable_dynamic_field=True,
        )
        # need wait 10s to wait proxy sync meta
        time.sleep(10)

    @staticmethod
    def _get_index_params(index_type: Any, table_params: TableParams) -> None:
        from pymochow.model.enum import IndexType
        from pymochow.model.schema import HNSWParams

        vector_params = (
            {} if table_params.vector_params is None else table_params.vector_params
        )

        if index_type == IndexType.HNSW:
            return HNSWParams(
                m=vector_params.get("M", DEFAULT_HNSW_M),
                efconstruction=vector_params.get(
                    "efConstruction", DEFAULT_HNSW_EF_CONSTRUCTION
                ),
            )
        return None

    @staticmethod
    def _get_index_type(index_type_value: str) -> Any:
        from pymochow.model.enum import IndexType

        index_type_value = index_type_value or IndexType.HNSW
        try:
            return IndexType(index_type_value)
        except ValueError:
            support_index_types = [
                d.value for d in IndexType.__members__.values()]
            raise ValueError(
                NOT_SUPPORT_INDEX_TYPE_ERROR.format(
                    index_type_value, support_index_types
                )
            )

    @staticmethod
    def _get_metric_type(metric_type_value: str) -> Any:
        from pymochow.model.enum import MetricType

        metric_type_value = metric_type_value or MetricType.L2
        try:
            return MetricType(metric_type_value.upper())
        except ValueError:
            support_metric_types = [
                d.value for d in MetricType.__members__.values()]
            raise ValueError(
                NOT_SUPPORT_METRIC_TYPE_ERROR.format(
                    metric_type_value, support_metric_types
                )
            )

    @property
    def client(self) -> Any:
        """
        获取客户端对象。
        
        Args:
            无参数
        
        Returns:
            Any: 返回客户端对象，具体类型依赖于vdb_client属性的值。
        """
        return self.vdb_client

    def as_retriever(self):
        """
        将对象转化为retriever
        
        Args:
            无
        
        Returns:
            BaiduVDBRetriever: 转化后的retriever对象
        
        """
        return BaiduVDBRetriever(
            embedding=self.embedding,
            table=self.table,
        )

    def add_segments(self, segments: Message, metadata=""):
        """
        向bes中插入数据段
        
        Args:
            segments (Message): 需要插入的数据段。
            metadata (str, optional): 元数据，默认为空字符串。
        
        Returns:
            无返回值
        
        Raises:
            ValueError: 如果segments为空，则抛出此异常。
        
        """
        from pymochow.model.table import Row

        segment_vectors = self.embedding.batch(segments)
        segment_vectors = segment_vectors.content
        vector_dims = len(segment_vectors[0])
        segments = segments.content
        if len(segments) == 0:
            raise ValueError("segments is emtpty")

        rows = []
        for segment, vector in zip(segments, segment_vectors):
            row = Row(text=segment, vector=vector, metadata=metadata)
            rows.append(row)
        if len(rows) >= DEFAULT_BATCH_SIZE:
            self.collection.upsert(rows=rows)
            rows = []

        if len(rows) > 0:
            self.table.upsert(rows=rows)

    @classmethod
    def from_params(
        cls,
        instance_id: str,
        api_key: str,
        account: str = DEFAULT_ACCOUNT,
        database_name: str = DEFAULT_DATABASE_NAME,
        table_name: str = DEFAULT_TABLE_NAME,
        drop_exists: bool = False,
        **kwargs,
    ):
        """
        从参数中实例化类。
        
        Args:
            cls (type): 类对象，即当前函数所属的类。
            instance_id (str): 实例ID。
            api_key (str): API密钥。
            account (str, optional): 账户名，默认为'root'。 Defaults to DEFAULT_ACCOUNT.
            database_name (str, optional): 数据库名，默认为'AppBuilderDatabase'。 Defaults to DEFAULT_DATABASE_NAME.
            table_name (str, optional): 表名，默认为'AppBuilderTable'。 Defaults to DEFAULT_TABLE_NAME.
            drop_exists (bool, optional): 是否删除已存在的表，默认为False。 Defaults to False.
            **kwargs: 其他参数，可选的维度参数dimension默认为384。
        
        Returns:
            cls: 类实例，包含实例ID、账户名、API密钥、数据库名、表参数等属性。
        
        """
        _try_import()
        dimension = kwargs.get("dimension", 384)

        if not isinstance(instance_id, str):
            raise TypeError("instance_id must be a string. but got {}".format(
                type(instance_id)))
        if not isinstance(api_key, str):
            raise TypeError("api_key must be a string. but got {}".format(
                type(api_key)))
        if not isinstance(account, str):
            raise TypeError("account must be a string. but got {}".format(
                type(account)))
        if not isinstance(database_name, str):
            raise TypeError("database_name must be a string. but got {}".format(
                type(database_name)))
        if not isinstance(table_name, str):
            raise TypeError("table_name must be a string. but got {}".format(
                type(table_name)))
        if not isinstance(drop_exists, bool):
            raise TypeError("drop_exists must be a boolean. but got {}".format(
                type(drop_exists)))

        table_params = TableParams(
            dimension=dimension,
            table_name=table_name,
            drop_exists=drop_exists,
        )
        return cls(
            instance_id=instance_id,
            account=account,
            api_key=api_key,
            database_name=database_name,
            table_params=table_params,
        )


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

    def __init__(self, 
                 embedding, 
                 table,
                 **kwargs
                 ):
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
