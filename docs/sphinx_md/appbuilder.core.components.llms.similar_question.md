# appbuilder.core.components.llms.similar_question package

## Submodules

## appbuilder.core.components.llms.similar_question.component module

similar question

### *class* appbuilder.core.components.llms.similar_question.component.SimilarQuestion(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = "..."

qa_mining = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
msg = appbuilder.Message(msg)
answer = qa_mining(msg)

print("Answer: \n{}".format(answer.content))
```

#### manifests *= [{'description': '基于输入的问题，挖掘出与该问题相关的类似问题。', 'name': 'similar_question', 'parameters': {'properties': {'query': {'description': '输入的问题，用于大模型根据该问题输出相关的类似问题。', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

[`SimilarQuestionMeta`](#appbuilder.core.components.llms.similar_question.component.SimilarQuestionMeta) 的别名

#### name *: str* *= 'similar_question'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0, request_id=None)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### tool_eval(name: str, streaming: bool = False, \*\*kwargs)

执行函数调用的评估工具。

* **参数:**
  * **name** (*str*) – 函数名。
  * **streaming** (*bool* *,* *optional*) – 是否以流式方式输出结果。默认为False。
  * **\*\*kwargs** – 

    其他关键字参数，包括：
    traceid (str, optional): 请求的追踪ID。
    query (str): 输入的查询字符串。
    model_configs (dict, optional): 模型配置字典，包括：
    > temperature (float, optional): 温度参数，用于控制输出结果的多样性。默认为1e-10。
    > top_p (float, optional): 截断概率，用于控制生成文本的质量。默认为0.0。
* **返回:**
  如果streaming为False，则返回评估结果的字符串表示。
  如果streaming为True，则生成评估结果的字符串表示的迭代器。
* **抛出:**
  **ValueError** – 如果未提供query参数，则抛出此异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.similar_question.component.SimilarQuestionMeta(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

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
