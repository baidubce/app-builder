# appbuilder.core.components.retriever.baidu_vdb package

## Submodules

## appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever module

基于Baidu VDB的retriever

### *class* appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.BaiduVDBRetriever(embedding, table)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

向量检索组件，用于检索和query相匹配的内容

Examples:

```python
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
```

#### name *: str* *= 'BaiduVectorDBRetriever'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message), top_k: int = 1)

根据query进行查询

* **参数:**
  * **query** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**str* *]*) – 需要查询的内容，类型为Message，包含要查询的文本。
  * **top_k** (*int* *,* *optional*) – 查询结果中匹配度最高的top_k个结果，默认为1。
* **返回:**
  查询到的结果，包含文本和匹配得分。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[Dict]
* **抛出:**
  * **TypeError** – 如果query不是Message类型，或者top_k不是整数类型。
  * **ValueError** – 如果top_k不是正整数，或者query的内容为空字符串，或者长度超过512个字符。

#### tool_desc *: Dict[str, Any]* *= {'description': 'a retriever based on Baidu VectorDB'}*

### *class* appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.BaiduVDBVectorStoreIndex(instance_id: str, api_key: str, account: str = 'root', database_name: str = 'AppBuilderDatabase', table_params: ~appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.TableParams = <appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.TableParams object>, embedding=None)

基类：`object`

Baidu VDB向量存储检索工具

#### add_segments(segments: [Message](appbuilder.core.md#appbuilder.core.message.Message), metadata='')

向bes中插入数据段

* **参数:**
  * **segments** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 需要插入的数据段。
  * **metadata** (*str* *,* *optional*) – 元数据，默认为空字符串。
* **返回:**
  无返回值
* **抛出:**
  **ValueError** – 如果segments为空，则抛出此异常。

#### as_retriever()

将对象转化为retriever

* **参数:**
  **无**
* **返回:**
  转化后的retriever对象
* **返回类型:**
  [BaiduVDBRetriever](#appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.BaiduVDBRetriever)

#### *property* client *: Any*

获取客户端对象。

* **参数:**
  **无参数**
* **返回:**
  返回客户端对象，具体类型依赖于vdb_client属性的值。
* **返回类型:**
  Any

#### *classmethod* from_params(instance_id: str, api_key: str, account: str = 'root', database_name: str = 'AppBuilderDatabase', table_name: str = 'AppBuilderTable', drop_exists: bool = False, \*\*kwargs)

从参数中实例化类。

* **参数:**
  * **cls** (*type*) – 类对象，即当前函数所属的类。
  * **instance_id** (*str*) – 实例ID。
  * **api_key** (*str*) – API密钥。
  * **account** (*str* *,* *optional*) – 账户名，默认为’root’。 Defaults to DEFAULT_ACCOUNT.
  * **database_name** (*str* *,* *optional*) – 数据库名，默认为’AppBuilderDatabase’。 Defaults to DEFAULT_DATABASE_NAME.
  * **table_name** (*str* *,* *optional*) – 表名，默认为’AppBuilderTable’。 Defaults to DEFAULT_TABLE_NAME.
  * **drop_exists** (*bool* *,* *optional*) – 是否删除已存在的表，默认为False。 Defaults to False.
  * **\*\*kwargs** – 其他参数，可选的维度参数dimension默认为384。
* **返回:**
  类实例，包含实例ID、账户名、API密钥、数据库名、表参数等属性。
* **返回类型:**
  cls

#### vdb_uri_prefix *= b'/api/v1/bce/vdb/instance/'*

### *class* appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.TableParams(dimension: int, table_name: str = 'AppBuilderTable', replication: int = 3, partition: int = 1, index_type: str = 'HNSW', metric_type: str = 'L2', drop_exists: bool = False, vector_params: Dict | None = None)

基类：`object`

Baidu VectorDB table params.
See the following documentation for details:
[https://cloud.baidu.com/doc/VDB/s/mlrsob0p6](https://cloud.baidu.com/doc/VDB/s/mlrsob0p6)

* **参数:**
  * **int** (*partition*) – The dimension of vector.
  * **int** – The number of replicas in the table.
  * **int** – The number of partitions in the table.
  * **index_type** (*Optional* *[**str* *]*) – HNSW, FLAT… Default value is “HNSW”
  * **metric_type** (*Optional* *[**str* *]*) – L2, COSINE, IP. Default value is “L2”
  * **drop_exists** (*Optional* *[**bool* *]*) – Delete the existing Table. Default value is False.
  * **vector_params** (*Optional* *[**Dict* *]*) – if HNSW set parameters: M and efConstruction, for example {‘M’: 16, efConstruction: 200}
    default is HNSW
