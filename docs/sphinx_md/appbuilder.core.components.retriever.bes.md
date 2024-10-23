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
