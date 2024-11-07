# appbuilder.core.components.table_ocr package

## Submodules

## appbuilder.core.components.table_ocr.component module

table ocr component.

### *class* appbuilder.core.components.table_ocr.component.TableOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

支持识别图片中的表格内容，返回各表格的表头表尾内容、单元格文字内容及其行列位置信息，全面覆盖各类表格样式，包括常规有线表格、
无线表格、含合并单元格表格。同时，支持多表格内容识别。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

table_ocr = appbuilder.TableOCR()
with open("./table_ocr_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### get_table_markdown(tables_result)

将表格识别结果转换为Markdown格式。

* **参数:**
  **tables_result** (*list*) – 表格识别结果列表，每个元素是一个包含表格数据的字典，其中包含表格体（body）等字段。
* **返回:**
  包含Markdown格式表格的字符串列表。
* **返回类型:**
  list

#### manifests *= [{'description': '需要识别图片中的表格内容，使用该工具, 但不支持html后缀文件的识别', 'name': 'table_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别图片的文件名', 'items': {'type': 'string'}, 'type': 'array'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'table_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

表格文字识别

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行识别操作。
    举例: Message(content={“raw_image”: b”…”})
    或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP重试次数。
* **返回:**
  识别结果。
  : 举例: Message(name=msg, content={‘tables_result’: [{
    ‘table_location’: [{‘x’: 15, ‘y’: 15}, {‘x’: 371, ‘y’: 15}, {‘x’: 371, ‘y’: 98}, {‘x’: 15,
    ‘y’: 98}], ‘header’: [], ‘body’: [{‘cell_location’: [{‘x’: 15, ‘y’: 15}, {‘x’: 120, ‘y’: 15},
    {‘x’: 120, ‘y’: 58}, {‘x’: 15, ‘y’: 58}], ‘row_start’: 0, ‘row_end’: 1, ‘col_start’: 0,
    ‘col_end’: 1, ‘words’: ‘参数’}, {‘cell_location’: [{‘x’: 120, ‘y’: 15}, {‘x’: 371, ‘y’: 15},
    {‘x’: 371, ‘y’: 58}, {‘x’: 120, ‘y’: 58}], ‘row_start’: 0, ‘row_end’: 1, ‘col_start’: 1,
    ‘col_end’: 2, ‘words’: ‘值’}, {‘cell_location’: [{‘x’: 15, ‘y’: 58}, {‘x’: 120, ‘y’: 58},
    {‘x’: 120, ‘y’: 98}, {‘x’: 15, ‘y’: 98}], ‘row_start’: 1, ‘row_end’: 2, ‘col_start’: 0,
    ‘col_end’: 1, ‘words’: ‘Content-Type’}, {‘cell_location’: [{‘x’: 120, ‘y’: 58}, {‘x’: 371,
    ‘y’: 58}, {‘x’: 371, ‘y’: 98}, {‘x’: 120, ‘y’: 98}], ‘row_start’: 1, ‘row_end’: 2, ‘col_start’:
    1, ‘col_end’: 2, ‘words’: ‘application/x-www-form-urlencoded’}], ‘footer’: []}]}, mtype=dict)
* **返回类型:**
  message ([Message](appbuilder.core.md#appbuilder.core.message.Message))

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

对传入文件进行处理，并返回处理结果。

* **参数:**
  * **name** (*str*) – 工具的名称。
  * **streaming** (*bool*) – 是否为流式处理。若为True，则以生成器形式返回结果；若为False，则直接返回结果。
  * **\*\*kwargs** – 关键字参数，包含以下参数：
    traceid (str): 请求的唯一标识符。
    file_names (List[str]): 文件名列表，表示需要处理的文件名。
    files (List[str]): 同file_names，用于兼容老版本接口。
    file_urls (Dict[str, str]): 文件名和对应URL的映射字典。
* **返回:**
  若streaming为True，则以生成器形式返回处理结果，每个元素为包含type和text的字典，type固定为”text”，text为处理结果的JSON字符串。
  若streaming为False，则直接返回处理结果的JSON字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 若传入文件名在file_urls中未找到对应的URL，则抛出此异常。

#### version *= 'v1'*
