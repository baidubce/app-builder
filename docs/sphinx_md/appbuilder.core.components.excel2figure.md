# appbuilder.core.components.excel2figure package

## Submodules

## appbuilder.core.components.excel2figure.component module

excel2figure component

### *class* appbuilder.core.components.excel2figure.component.Excel2Figure(model: str, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

excel2figure 组件类

* **参数:**
  * **model** – str
  * **secret_key** – Optional[str]
  * **gateway** – str
  * **lazy_certification** – bool

#### excluded_models *: List[str]* *= ['Yi-34B-Chat', 'ChatLaw']*

#### manifests *= [{'description': 'Excel转图表工具，当用户需要根据Excel图表的数据进行数据分析并绘制图表（柱状图、折线图、雷达图等），使用该工具。', 'name': 'excel_to_figure', 'parameters': {'properties': {'query': {'description': '需要根据Excel图表的数据进行数据分析并绘制图表的请求描述。', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

[`Excel2FigureArgs`](#appbuilder.core.components.excel2figure.component.Excel2FigureArgs) 的别名

#### model_info *: ModelInfo* *= None*

#### model_type *: str* *= 'chat'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message)) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行 excel2figure。

* **参数:**
  **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 消息对象，其 content 属性是一个字典，包含以下键值对：
  - query (str): 用户的问题。
  - excel_file_url (str): 用户的 Excel 文件地址。
* **返回:**
  处理后的消息对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **ValueError** – 当 message.content 解析失败时抛出此异常。

#### set_secret_key_and_gateway(\*\*kwargs)

#### tool_eval(streaming: bool, origin_query: str, file_urls: dict, \*\*kwargs)

对指定的Excel文件进行图表生成和评估。

* **参数:**
  * **streaming** (*bool*) – 是否以流式传输方式返回结果。如果为True，则通过生成器返回结果；如果为False，则直接返回结果。
  * **origin_query** (*str*) – 原始查询字符串，用于在缺少其他查询参数时使用。
  * **file_urls** (*dict*) – 包含Excel文件信息的字典，其中键为文件名，值为文件URL。
  * **\*\*kwargs** – 其他关键字参数，可以包括查询字符串等。
* **返回:**
  如果streaming为True，则通过生成器返回结果。每个结果是一个字典，包含以下键：
  - event (str): 事件类型，始终为’excel_to_figure’。
  - type (str): 数据类型，始终为’files’。
  - text (list of str): 包含生成的图表信息的列表。

  如果streaming为False，则直接返回一个包含上述信息的字典。
* **抛出:**
  * **ValueError** – 如果file_urls的长度不等于1，则抛出异常。
  * **RuntimeError** – 如果Excel文件到图表的转换失败或出现异常，则抛出异常。

### *class* appbuilder.core.components.excel2figure.component.Excel2FigureArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, query: Annotated[str, MaxLen(max_length=400)], excel_file_url: Url)

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

excel2figure 的参数

#### query

str

* **Type:**
  str

#### excel_file_url

AnyUrl

* **Type:**
  pydantic_core._pydantic_core.Url

#### excel_file_url *: Url*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'excel_file_url': FieldInfo(annotation=Url, required=True, description='用户的 excel 文件地址，需要是一个可被公网下载的 URL 地址'), 'name': FieldInfo(annotation=str, required=False, default=''), 'query': FieldInfo(annotation=str, required=True, description='用户的 query 输入', metadata=[MaxLen(max_length=400)]), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### query *: str*
