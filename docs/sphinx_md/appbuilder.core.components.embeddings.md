# appbuilder.core.components.embeddings package

## Submodules

## appbuilder.core.components.embeddings.component module

ernie bot embedding

### *class* appbuilder.core.components.embeddings.component.Embedding(model='Embedding-V1')

基类：`EmbeddingBaseComponent`

Embedding-V1是基于百度文心大模型技术的文本表示模型，将文本转化为用数值表示的向量形式，用于文本检索、信息推荐、知识挖掘等场景。

#### model

str = “Embedding-V1”

### 示例

```python
import appbuilder
from appbuilder import Message

os.environ["APPBUILDER_TOKEN"] = '...'

embedding = appbuilder.Embedding()

embedding_single = embedding(Message("hello world!"))

embedding_batch = embedding.batch(Message(["hello", "world"]))
```

#### accepted_models *= ['Embedding-V1']*

#### base_urls *= {'Embedding-V1': '/v1/bce/wenxinworkshop/ai_custom/v1/embeddings/embedding-v1'}*

#### batch(texts: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]] | List[str]) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[List[float]]]

批量处理文本数据。

* **参数:**
  **texts** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**List* *[**str* *]* *]* *,* *List* *[**str* *]* *]*) – 待处理的文本数据，可以是 Message 类型，包含多个文本列表，也可以是普通列表类型，包含多个文本。
* **返回:**
  处理后的结果，为 Message 类型，包含一个二维浮点数列表，每个子列表对应输入文本列表中一个文本的处理结果。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[List[float]]]

#### meta

[`EmbeddingArgs`](#appbuilder.core.components.embeddings.component.EmbeddingArgs) 的别名

#### name *: str* *= 'embedding'*

#### run(text: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]]

处理给定的文本或消息对象，并返回包含处理结果的消息对象。

* **参数:**
  **text** (*Union* *[*[*Message*](appbuilder.core.md#appbuilder.core.message.Message) *[**str* *]* *,* *str* *]*) – 待处理的文本或消息对象。
* **返回:**
  处理后的结果，封装在消息对象中。结果是一个浮点数列表。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]]

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.embeddings.component.EmbeddingArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, text: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str)

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

ernie bot embedding配置

#### text

输入文本

* **Type:**
  Union[[Message](appbuilder.core.md#appbuilder.core.message.Message)[str], str]

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'name': FieldInfo(annotation=str, required=False, default=''), 'text': FieldInfo(annotation=Union[Message[str], str], required=True), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### text *: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str*
