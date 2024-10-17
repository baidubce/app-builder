# appbuilder.core.components.llms.style_writing package

## Submodules

## appbuilder.core.components.llms.style_writing.component module

### *class* appbuilder.core.components.llms.style_writing.component.LengthChoices(value)

基类：`Enum`

An enumeration.

#### LONG *= 600*

#### MEDIUM *= 300*

#### SHORT *= 100*

#### to_chinese()

将LengthChoices枚举对象转换为中文描述。

* **参数:**
  **无参数**
* **返回:**
  转换后的中文描述，包括”短”、”中”和”长”。
* **返回类型:**
  str

### *class* appbuilder.core.components.llms.style_writing.component.StyleQueryChoices(value)

基类：`Enum`

StyleQueryChoices是一个枚举类型，包含三个选项：

#### BILIBILI

* **Type:**
  “B站”

#### XIAOHONGSHU

* **Type:**
  “小红书”

#### GENERAL

* **Type:**
  “通用”

#### BILIBILI *= 'B站'*

#### GENERAL *= '通用'*

#### XIAOHONGSHU *= '小红书'*

#### to_chinese()

将StyleQueryChoices枚举类中的值转换为中文描述。

* **参数:**
  **无参数**
* **返回:**
  返回一个字典，键是StyleQueryChoices枚举类的成员，值为对应的中文描述字符串。

### *class* appbuilder.core.components.llms.style_writing.component.StyleWriting(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

风格写作大模型组件， 基于生成式大模型进行风格写作，支持B站、小红书等多种风格，可用于文案、广告等多种场景。

Examples:

```python
import os
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

style_writing = appbuilder.StyleWriting(model="ERNIE Speed-AppBuilder")
answer = style_writing(appbuilder.Message("帮我写一篇关于人体工学椅的文案"), style_query="小红书", length=100)
```

#### manifests *= [{'description': '根据用户输入的文案要求和文案风格，生成符合特定风格的产品介绍或宣传文案。目前支持生成小红书风格、B站风格或通用风格的文案。', 'name': 'style_writing', 'parameters': {'properties': {'length': {'description': '用于定义输出内容的长度。有效的选项包括 100（短）、300（中）、600（长），默认值为 100。', 'enum': [100, 300, 600], 'type': 'integer'}, 'query': {'description': '用于描述生成文案的主题和要求。', 'type': 'string'}, 'style': {'description': '用于定义文案生成的风格，包括通用、B站、小红书，默认为通用。', 'enum': ['通用', 'B站', '小红书'], 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

[`StyleWritingArgs`](#appbuilder.core.components.llms.style_writing.component.StyleWritingArgs) 的别名

#### name *: str* *= 'style_writing'*

#### run(message, style_query='通用', length=100, stream=False, temperature=1e-10, top_p=0, request_id=None)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **style_query** (*str*) – 风格查询选项，用于指定写作风格。有效的选项包括 ‘B站’, ‘小红书’, ‘通用’。默认值为 ‘通用’。
  * **length** (*int*) – 输出内容的长度。有效的选项包括 100（短），300（中），600（长）。默认值为 100。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
  * **request_id** (*str* *,* *optional*) – 请求ID，用于跟踪和识别请求。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### tool_eval(name: str, streaming: bool = False, \*\*kwargs)

对指定的工具进行函数调用评估。

* **参数:**
  * **name** (*str*) – 工具名称。
  * **streaming** (*bool* *,* *optional*) – 是否以流的方式返回结果。默认为False。
  * **\*\*kwargs** – 其他参数。
* **返回:**
  如果 streaming 为 False，则返回评估结果字符串；如果 streaming 为 True，则返回一个生成器，每次迭代返回评估结果字符串的一部分。
* **返回类型:**
  str 或 generator
* **抛出:**
  **ValueError** – 如果未提供必要的参数 ‘query’。

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.style_writing.component.StyleWritingArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message), style_query: [StyleQueryChoices](#appbuilder.core.components.llms.style_writing.component.StyleQueryChoices), length: [LengthChoices](#appbuilder.core.components.llms.style_writing.component.LengthChoices))

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

风格写作配置

#### message

Message = Field(…)

* **Type:**
  [appbuilder.core.message.Message](appbuilder.core.md#appbuilder.core.message.Message)

#### style_query

StyleQueryChoices = Field(…)

* **Type:**
  [appbuilder.core.components.llms.style_writing.component.StyleQueryChoices](#appbuilder.core.components.llms.style_writing.component.StyleQueryChoices)

#### length

LengthChoices = Field(…)

* **Type:**
  [appbuilder.core.components.llms.style_writing.component.LengthChoices](#appbuilder.core.components.llms.style_writing.component.LengthChoices)

#### length *: [LengthChoices](#appbuilder.core.components.llms.style_writing.component.LengthChoices)*

#### message *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'length': FieldInfo(annotation=LengthChoices, required=True, description="输出长度，可选值为 '短' (100), '中' (300), '长' (600)。", json_schema_extra={'variable_name': 'length'}), 'message': FieldInfo(annotation=Message, required=True, description="输入消息，用于模型的主要输入内容，例如'帮我生成一个介绍保温杯的话术'", json_schema_extra={'variable_name': 'query'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'style_query': FieldInfo(annotation=StyleQueryChoices, required=True, description="风格查询选项，可选值为 'B站', '小红书', '通用'。", json_schema_extra={'variable_name': 'style_query'}), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### style_query *: [StyleQueryChoices](#appbuilder.core.components.llms.style_writing.component.StyleQueryChoices)*
