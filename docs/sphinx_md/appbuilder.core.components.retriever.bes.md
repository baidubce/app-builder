# appbuilder.core.components.retriever.bes package

## Submodules

## appbuilder.core.components.retriever.bes.bes_retriever module

基于baidu ES的retriever

### *class* appbuilder.core.components.retriever.bes.bes_retriever.BESRetriever(embedding, index_name, bes_client, index_type='hnsw')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

向量检索组件，用于检索和query相匹配的内容

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
vector_index = appbuilder.BESVectorStoreIndex.from_segments(segments, self.cluster_id, self.username,
                                                            self.password)
query = appbuilder.Message("文心一言")
time.sleep(5)
retriever = vector_index.as_retriever()
res = retriever(query)
```

#### base_es_url *: str* *= '/v1/bce/bes/cluster/'*

#### name *: str* *= 'BaiduElasticSearchRetriever'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message), top_k: int = 1)

根据query进行查询

* **参数:**
  * **query** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**str* *]*) – 需要查询的内容，以Message对象的形式传递。
  * **top_k** (*int* *,* *optional*) – 查询结果中匹配度最高的top_k个结果。默认为1。
* **返回:**
  查询到的结果，包含文本、元数据以及匹配得分，以Message对象的形式返回。
* **返回类型:**
  obj ([Message](appbuilder.core.md#appbuilder.core.message.Message)[Dict])

#### tool_desc *: Dict[str, Any]* *= {'description': 'a retriever based on Baidu ElasticSearch'}*

### *class* appbuilder.core.components.retriever.bes.bes_retriever.BESVectorStoreIndex(cluster_id, user_name, password, embedding=None, index_name=None, index_type='hnsw', prefix='/rpc/2.0/cloud_hub')

基类：`object`

BES向量存储检索工具

#### add_segments(segments: [Message](appbuilder.core.md#appbuilder.core.message.Message), metadata='')

向BES中插入数据

* **参数:**
  * **segments** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**str* *]*) – 需要插入的内容，包含多个文本段
  * **metadata** (*str* *,* *optional*) – 元数据，默认为空字符串。
* **返回:**
  无返回值

#### as_retriever()

将当前对象转化为retriever。

* **参数:**
  **无**
* **返回:**
  转化后的retriever对象
* **返回类型:**
  [BESRetriever](#appbuilder.core.components.retriever.bes.bes_retriever.BESRetriever)

#### base_es_url *: str* *= '/v1/bce/bes/cluster/'*

#### *static* create_index_mappings(index_type, vector_dims)

创建索引的mapping

* **参数:**
  * **index_type** (*str*) – 索引类型，如”hnsw”
  * **vector_dims** (*int*) – 向量的维度
* **返回:**
  索引的mapping配置
* **返回类型:**
  dict

#### delete_all_segments()

删除索引中的全部内容。

* **参数:**
  **无**
* **返回:**
  无

#### *property* es

获取Elasticsearch客户端实例。

* **参数:**
  **无**
* **返回:**
  Elasticsearch客户端实例。

#### *classmethod* from_segments(segments, cluster_id, user_name, password, embedding=None, \*\*kwargs)

根据段落创建一个bes向量索引。

* **参数:**
  * **segments** (*list*) – 切分的文本段落列表。
  * **cluster_id** (*str*) – bes集群ID。
  * **user_name** (*str*) – bes用户名。
  * **password** (*str*) – bes用户密码。
  * **embedding** ([*Embedding*](appbuilder.core.components.embeddings.md#appbuilder.core.components.embeddings.component.Embedding) *,* *optional*) – 文本段落embedding工具，默认为None，使用默认的Embedding类。
  * **\*\*kwargs** – 其他初始化参数。
* **返回:**
  bes索引实例。
* **返回类型:**
  BesVectorIndex

#### *static* generate_id(length=16)

生成随机的ID。

* **参数:**
  **length** (*int* *,* *optional*) – 生成ID的长度，默认为16。
* **返回:**
  生成的随机ID。
* **返回类型:**
  str

#### get_all_segments()

获取索引中的全部内容

#### *property* helpers

获取帮助器实例。

* **参数:**
  **无**
* **返回:**
  帮助器实例。
* **返回类型:**
  \_helpers (对象)
