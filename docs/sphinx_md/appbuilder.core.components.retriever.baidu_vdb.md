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
