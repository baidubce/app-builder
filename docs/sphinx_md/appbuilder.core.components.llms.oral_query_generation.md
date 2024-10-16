# appbuilder.core.components.llms.oral_query_generation package

## Submodules

## appbuilder.core.components.llms.oral_query_generation.component module

### *class* appbuilder.core.components.llms.oral_query_generation.component.OralQueryGeneration(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

口语化Query生成，可用于问答场景下对文档增强索引。
 *注：该组件推荐使用ERNIE Speed-AppBuilder模型。*

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
        '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
        '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
        '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
        '，实时视频分享您的生活。')
oral_query_generation = appbuilder.OralQueryGeneration(model='ERNIE Speed-AppBuilder')
answer = oral_query_generation(appbuilder.Message(text), query_type='全部', output_format='str')
print(answer.content)
```

#### completion(version, base_url, request, timeout: float | None = None, retry: int = 0)

Send a byte array of an audio file to obtain the result of speech recognition.

#### manifests *= [{'description': '输入文本、待生成的query类型和输出格式，生成query，并按照要求的格式进行输出。', 'name': 'query_generation', 'parameters': {'properties': {'output_format': {'description': '输出格式，可选json或str，str格式与老版本输出格式相同。', 'text': 'string'}, 'query_type': {'description': '待生成的query类型，可选问题、短语以及全部（问题 + 短语）。', 'text': 'string'}, 'text': {'description': '输入文本，组件会根据该输入文本生成query。', 'text': 'string'}}, 'required': ['text'], 'type': 'object'}}]*

#### meta

[`OralQueryGenerationArgs`](#appbuilder.core.components.llms.oral_query_generation.component.OralQueryGenerationArgs) 的别名

#### name *: str* *= 'query_generation'*

#### regenerate_output(model_output, output_format)

兼容老版本的输出格式

#### run(message, query_type='全部', output_format='str', stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息，包含query、context和answer等信息。这是一个必需的参数。
  * **query_type** (*str* *,*  *可选*) – 待生成的query类型，包括问题、短语和全部（问题+短语）。默认为全部。
  * **output_format** (*str* *,*  *可选*) – 输出格式，包括json和str，当stream为True时，只能以json形式输出。默认为str。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](appbuilder.core.md#appbuilder.core.message.Message))

#### tool_eval(name: str, stream: bool = False, \*\*kwargs)

调用函数进行工具评估。

* **参数:**
  * **name** (*str*) – 评估工具的名称。
  * **stream** (*bool* *,* *optional*) – 是否以流的形式返回结果。默认为False。
  * **\*\*kwargs** – 关键字参数，可以包含以下参数：
    text (str): 需要评估的文本。
    query_type (str, optional): 查询类型，默认为’全部’。
    output_format (str, optional): 输出格式，默认为’str’。
    model_configs (dict, optional): 模型配置，默认为空字典。
* **返回:**
  如果stream为False，则返回评估结果列表；
  如果stream为True，则逐个返回评估结果。
* **抛出:**
  **ValueError** – 如果未提供text参数，则抛出ValueError异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.oral_query_generation.component.OralQueryGenerationArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, text: str, query_type: [QueryTypeChoices](#appbuilder.core.components.llms.oral_query_generation.component.QueryTypeChoices), output_format: [QueryTypeChoices](#appbuilder.core.components.llms.oral_query_generation.component.QueryTypeChoices))

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

口语化Query生成配置

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'name': FieldInfo(annotation=str, required=False, default=''), 'output_format': FieldInfo(annotation=QueryTypeChoices, required=True, description='输出格式，可选值为json、str。', json_schema_extra={'variable_name': 'output_format'}), 'query_type': FieldInfo(annotation=QueryTypeChoices, required=True, description='待生成的query类型，可选值为问题、短语和全部（问题+短语）。', json_schema_extra={'variable_name': 'query_type'}), 'text': FieldInfo(annotation=str, required=True, description='输入文本，用于生成Query', json_schema_extra={'valiable_name': 'text'}), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### output_format *: [QueryTypeChoices](#appbuilder.core.components.llms.oral_query_generation.component.QueryTypeChoices)*

#### query_type *: [QueryTypeChoices](#appbuilder.core.components.llms.oral_query_generation.component.QueryTypeChoices)*

#### text *: str*

### *class* appbuilder.core.components.llms.oral_query_generation.component.OutputFormatChoices(value)

基类：`Enum`

An enumeration.

#### json_format *= 'json'*

#### str_format *= 'str'*

#### to_chinese()

将OutputFormatChoices枚举类中的值转换为中文描述。

* **参数:**
  **无参数**
* **返回:**
  返回一个字典，键是OutputFormatChoices枚举类的成员，值为对应的中文描述字符串。

### *class* appbuilder.core.components.llms.oral_query_generation.component.QueryTypeChoices(value)

基类：`Enum`

An enumeration.

#### phrases *= '短语'*

#### questions *= '问题'*

#### questions_and_phrases *= '全部'*

#### to_chinese()

将QueryTypeChoices枚举类中的值转换为中文描述。

* **参数:**
  **无参数**
* **返回:**
  返回一个字典，键是QueryTypeChoices枚举类的成员，值为对应的中文描述字符串。
