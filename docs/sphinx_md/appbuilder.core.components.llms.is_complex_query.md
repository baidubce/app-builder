# appbuilder.core.components.llms.is_complex_query package

## Submodules

## appbuilder.core.components.llms.is_complex_query.component module

is complex query

### *class* appbuilder.core.components.llms.is_complex_query.component.IsComplexQuery(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

基于输入的问题, 对问题进行初步的分类，方便下游使用不同类型的流程来处理当前的简单问题/复杂问题。广泛用于知识问答场景。

Examples:

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

is_complex_query = appbuilder.IsComplexQuery(model="ERNIE Speed-AppBuilder")

msg = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
msg = appbuilder.Message(msg)
answer = is_complex_query(msg)

print("Answer: \n{}".format(answer.content))
```

#### meta

[`IsComplexQueryMeta`](#appbuilder.core.components.llms.is_complex_query.component.IsComplexQueryMeta) 的别名

#### name *: str* *= 'is_complex_query'*

#### run(message, stream=False, temperature=1e-10, top_p=0)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.is_complex_query.component.IsComplexQueryMeta(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

#### message

输入消息，用于模型的输入，一般为问题。

* **Type:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### message *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'message': FieldInfo(annotation=Message, required=True, description='输入消息，用于模型的输入，一般为问题。', json_schema_extra={'variable_name': 'query'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.
