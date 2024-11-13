# appbuilder.core.components.excel2figure package

## Submodules

## appbuilder.core.components.excel2figure.component module

excel2figure component

### *class* appbuilder.core.components.excel2figure.component.Excel2Figure(model: str, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

excel2figure 组件类

* **参数:**
  * **model** -- str
  * **secret_key** -- Optional[str]
  * **gateway** -- str
  * **lazy_certification** -- bool

#### excluded_models *: List[str]* *= ['Yi-34B-Chat', 'ChatLaw']*

#### manifests *= [{'description': 'Excel转图表工具，当用户需要根据Excel图表的数据进行数据分析并绘制图表（柱状图、折线图、雷达图等），使用该工具。', 'name': 'excel_to_figure', 'parameters': {'properties': {'query': {'description': '需要根据Excel图表的数据进行数据分析并绘制图表的请求描述。', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

`Excel2FigureArgs` 的别名

#### model_info *: ModelInfo* *= None*

#### model_type *: str* *= 'chat'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message)) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行 excel2figure。

* **参数:**
  **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) -- 消息对象，其 content 属性是一个字典，包含以下键值对：
  - query (str): 用户的问题。
  - excel_file_url (str): 用户的 Excel 文件地址。
* **返回:**
  处理后的消息对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **ValueError** -- 当 message.content 解析失败时抛出此异常。

#### set_secret_key_and_gateway(\*\*kwargs)

设置密钥和网关地址。

* **参数:**
  * **secret_key** (*Optional* *[**str* *]* *,* *optional*) -- 密钥，默认为None。如果未指定，则使用实例当前的密钥。
  * **gateway** (*str* *,* *optional*) -- 网关地址，默认为空字符串。如果未指定，则使用实例当前的网关地址。
* **返回:**
  None

#### tool_eval(streaming: bool, origin_query: str, file_urls: dict, \*\*kwargs)

对指定的Excel文件进行图表生成和评估。

* **参数:**
  * **streaming** (*bool*) -- 是否以流式传输方式返回结果。如果为True，则通过生成器返回结果；如果为False，则直接返回结果。
  * **origin_query** (*str*) -- 原始查询字符串，用于在缺少其他查询参数时使用。
  * **file_urls** (*dict*) -- 包含Excel文件信息的字典，其中键为文件名，值为文件URL。
  * **\*\*kwargs** -- 其他关键字参数，可以包括查询字符串等。
* **返回:**
  如果streaming为True，则通过生成器返回结果。每个结果是一个字典，包含以下键：
  - event (str): 事件类型，始终为'excel_to_figure'。
  - type (str): 数据类型，始终为'files'。
  - text (list of str): 包含生成的图表信息的列表。

  如果streaming为False，则直接返回一个包含上述信息的字典。
* **抛出:**
  * **ValueError** -- 如果file_urls的长度不等于1，则抛出异常。
  * **RuntimeError** -- 如果Excel文件到图表的转换失败或出现异常，则抛出异常。
