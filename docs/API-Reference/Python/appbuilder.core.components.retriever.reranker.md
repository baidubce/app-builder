# appbuilder.core.components.retriever.reranker package

## Submodules

## appbuilder.core.components.retriever.reranker.rerank module

Reranker 文本精排

### *class* appbuilder.core.components.retriever.reranker.rerank.Reranker(model='bce-reranker-base')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

Examples:

```python
import os
import appbuilder
from appbuilder import Message

os.environ["APPBUILDER_TOKEN"] = '...'

reranker = appbuilder.Reranker()
ranked_1 = reranker("你好", ["他也好", "hello?"])
print(ranked_1)
```

#### accepted_models *= ['bce-reranker-base']*

#### base_urls *= {'bce-reranker-base': '/api/v1/component/component/bce_reranker_base'}*

#### meta

`RerankerArgs` 的别名

#### name *: str* *= 'reranker'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str, texts: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]] | List[str]) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[dict]]

运行查询，对给定的文本集合进行批量处理，并返回处理后的结果列表。

* **参数:**
  * **query** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**str* *]* *,* *str* *]*) -- 查询条件，可以是字符串或Message对象。
  * **texts** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**List* *[**str* *]* *]* *,* *List* *[**str* *]* *]*) -- 待处理的文本集合，可以是字符串列表或包含字符串列表的Message对象。
* **返回:**
  处理后的结果列表，每个元素是一个字典，包含处理后的文本信息。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[dict]]

#### version *: str* *= 'v1'*
