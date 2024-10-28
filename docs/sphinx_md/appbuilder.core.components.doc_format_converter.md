# appbuilder.core.components.doc_format_converter package

## Submodules

## appbuilder.core.components.doc_format_converter.component module

文档格式转换

### *class* appbuilder.core.components.doc_format_converter.component.DocFormatConverter(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

可识别图片/PDF文档版面布局，提取文字内容，并转换为保留原文档版式的Word、Excel文档，方便二次编辑和复制，
可支持含表格、印章、水印、手写等内容的文档。满足文档格式转换、企业档案电子化等信息管理需求。

### 示例

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥
os.environ["APPBUILDER_TOKEN"] = '...'

table_ocr = appbuilder.DocFormatConverter()
out = self.component.run(appbuilder.Message(content={"file_path": ""}))
print(out.content)
```

#### manifests *= [{'description': '提供文档格式转换功能，包含图片转word、图片转excel、PDF转word、PDF转excel', 'name': 'doc_format_converter', 'parameters': {'anyOf': [{'required': ['file_name']}, {'required': ['file_url']}], 'properties': {'file_name': {'description': '待转换文件的文件名称', 'type': 'string'}, 'file_url': {'description': '待转换文件的URL地址', 'type': 'string'}, 'page_num': {'anyOf': [{'type': 'string'}, {'type': 'integer'}], 'description': '待转换PDF文档的页码, 从1开始, 如果不传则默认转换全部页码'}}, 'type': 'object'}}]*

#### name *= 'doc_converter'*

#### queryDocFormatConverterTask(request: DocFormatConverterQueryRequest, timeout: float | None = None, retry: int = 0, request_id: str | None = None) → DocFormatConverterQueryResponse

查询任务
:param request: 请求参数
:type request: DoFormatcConverterQueryRequest
:return: 返回结果
:rtype: DocFormatConverterSubmitResponse

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0, request_id: str = None) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

将PDF、JPG、PNG、BMP等格式文件转换为Word、Excel格式，并返回转换后的文件URL。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 包含待转换文件路径和页码信息的消息对象。
  * **timeout** (*float* *,* *optional*) – 请求超时时间，单位为秒。默认为None，表示不设置超时时间。
  * **retry** (*int* *,* *optional*) – 请求重试次数。默认为0，表示不重试。
* **返回:**
  包含转换后文件URL的消息对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **AppBuilderServerException** – 文档格式转换服务发生错误时抛出。

#### submitDocFormatConverterTask(request: DocFormatConverterSubmitRequest, timeout: float | None = None, retry: int = 0, request_id: str | None = None) → DocFormatConverterSubmitResponse

提交任务
:param request: 请求参数
:type request: DocFormatConverterSubmitRequest
:return: 返回结果
:rtype: DocFormatConverterSubmitResponse

#### tool_eval(streaming: bool, origin_query: str, \*\*kwargs)

评估工具函数。

* **参数:**
  * **streaming** (*bool*) – 是否流式输出。如果为True，则逐个生成文件URL；如果为False，则直接返回结果内容。
  * **origin_query** (*str*) – 原始查询字符串。
  * **\*\*kwargs** – 其他关键字参数，包括但不限于：
    traceid (str): 请求的跟踪ID，用于日志追踪。
    file_url (str): 文件的URL地址。如果为空，则从file_urls和file_name中获取。
    file_urls (dict): 包含多个文件路径与URL的映射关系的字典。
    file_name (str): 文件名。如果file_url为空，则从file_urls和file_name中获取file_url。
    page_num (Union[int, str]): 需要处理的页面编号，如果为字符串，必须为纯数字。
* **返回:**
  如果streaming为True，则逐个生成包含文件URL的字典；如果streaming为False，则直接返回结果内容。
* **抛出:**
  * **InvalidRequestArgumentError** – 如果请求格式错误，如page_num不是整数、file_url为空且无法从file_urls和file_name中获取file_url等。
  * **AppBuilderServerException** – 如果服务执行过程中出现异常。

#### version *= 'v1'*
