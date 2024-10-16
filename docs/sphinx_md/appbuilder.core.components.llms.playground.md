# appbuilder.core.components.llms.playground package

## Submodules

## appbuilder.core.components.llms.playground.component module

### *class* appbuilder.core.components.llms.playground.component.Playground(prompt_template=None, model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

空模板， 支持用户自定义prompt模板，并进行执行

Examples:

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "..."

play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model="ERNIE Speed-AppBuilder")
play(appbuilder.Message({"name": "小明", "bot_name": "小红", "bot_type": "聊天机器人", "bot_function": "聊天", "bot_question": "你好吗？"}), stream=False)
```

#### meta

[`PlaygroundArgs`](#appbuilder.core.components.llms.playground.component.PlaygroundArgs) 的别名

#### name *: str* *= 'playground'*

#### prompt_template *= ''*

#### run(message, stream=False, temperature=1e-10, top_p=0.0, max_output_tokens=1024, disable_search=True, response_format='text', stop=[], \*\*kwargs)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
  * **max_output_tokens** (*int* *,*  *可选*) – 指定生成的文本的最大长度，默认最大输出token数为1024, 最小为2，
    最大输出token与选择的模型有关。
  * **disable_search** (*bool* *,*  *可选*) – 是否强制关闭实时搜索功能，默认为 True，表示关闭。
  * **response_format** (*str* *,*  *可选*) – 指定返回的消息格式，默认为 ‘text’，以文本模式返回。
    可选 ‘json_object’，以 json 格式返回，但可能存在不满足效果的情况。
  * **stop** (*list* *[**str* *]* *,*  *可选*) – 生成停止标识，当模型生成结果以 stop 中某个元素结尾时，停止文本生成。
    每个元素长度不超过 20 字符，最多 4 个元素。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### variable_names *= {}*

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.playground.component.PlaygroundArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

空模板参数配置

#### message

输入消息，用于模型的主要输入内容

* **Type:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### message *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'message': FieldInfo(annotation=Message, required=True, json_schema_extra={'variable_name': 'query', 'description': '输入消息，用于模型的主要输入内容'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.
