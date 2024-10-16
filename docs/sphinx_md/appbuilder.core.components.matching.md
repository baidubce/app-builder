# appbuilder.core.components.matching package

## Submodules

## appbuilder.core.components.matching.component module

### *class* appbuilder.core.components.matching.component.Matching(embedding_component: EmbeddingBaseComponent)

基类：`MatchingBaseComponent`

基于Embedding类型的文本表示模型，输入query和文本列表，对其进行排序或者相似度计算

### 示例

```python
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
```

#### meta

`MatchingArgs` 的别名

#### name *: str* *= 'Matching'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str, contexts: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]] | List[str], return_score: bool = False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]]

根据给定的查询和上下文，返回匹配的上下文列表。

* **参数:**
  * **query** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**str* *]* *,* *str* *]*) – 查询字符串或Message对象，包含查询字符串。
  * **contexts** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**List* *[**str* *]* *]* *,* *List* *[**str* *]* *]*) – 上下文字符串列表或Message对象，包含上下文字符串列表。
  * **return_score** (*bool* *,* *optional*) – 是否返回匹配得分。默认为False。
* **返回:**
  匹配的上下文列表。如果return_score为True，则返回包含得分和上下文的元组列表；否则仅返回上下文列表。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]]

#### semantics(query_embedding: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]] | List[float], context_embeddings: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[List[float]]] | List[List[float]]) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]]

计算query和context的相似度

* **参数:**
  * **query_embedding** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**List* *[**float* *]* *]* *,* *List* *[**float* *]* *]*) – query的embedding，长度为n的数组
  * **context_embeddings** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**List* *[**List* *[**float* *]* *]* *]* *,* *List* *[**List* *[**float* *]* *]* *]*) – context的embedding，长度为m x n的矩阵，其中m表示候选context的数量
* **返回:**
  query和所有候选context的相似度列表
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]]

#### version *: str* *= 'v1'*
