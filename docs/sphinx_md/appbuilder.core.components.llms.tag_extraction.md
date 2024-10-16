# appbuilder.core.components.llms.tag_extraction package

## Submodules

## appbuilder.core.components.llms.tag_extraction.component module

### *class* appbuilder.core.components.llms.tag_extraction.component.TagExtraction(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

标签抽取组件，基于生成式大模型进行关键标签的抽取。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

tag_extraction = appbuilder.TagExtraction(model="ERNIE Speed-AppBuilder")
answer = tag_extraction(appbuilder.Message("从这段文本中抽取关键标签"))
```

#### meta

[`TagExtractionArgs`](#appbuilder.core.components.llms.tag_extraction.component.TagExtractionArgs) 的别名

#### name *: str* *= 'tag_extraction'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message, 必选): 输入消息，用于模型的主要输入内容。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.tag_extraction.component.TagExtractionArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

标签抽取配置

#### message

输入消息，用于模型的主要输入内容

* **Type:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### message *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'message': FieldInfo(annotation=Message, required=True, description="输入消息，用于模型的主要输入内容，例如'本实用新型公开了一种可利用热能的太阳能光伏光热一体化组件，\\n                             包括太阳能电池，还包括有吸热板，太阳能电池粘附在吸热板顶面，吸热板内嵌入有热电材料制成的内芯，吸热板底面设置有蛇形管。\\n                             本实用新型结构紧凑，安装方便，能充分利用太阳能电池散发的热能，具有较高的热能利用率。'", json_schema_extra={'variable_name': 'query'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.
