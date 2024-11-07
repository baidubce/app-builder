# appbuilder.core.components.text_to_image package

## Submodules

## appbuilder.core.components.text_to_image.component module

Text2Image component.

### *class* appbuilder.core.components.text_to_image.component.Text2Image(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文生图组件，即对于输入的文本，输出生成的图片url。

Examples:

```python
import appbuilder
text_to_image = appbuilder.Text2Image()
os.environ["APPBUILDER_TOKEN"] = '...'
content_data = {"prompt": "上海的经典风景", "width": 1024, "height": 1024, "image_num": 1}
msg = appbuilder.Message(content_data)
out = text_to_image.run(inp)
# 打印生成结果
print(out.content) # eg: {"img_urls": ["xxx"]}
```

#### *static* check_service_error(request_id: str, data: dict)

检查服务错误信息

* **参数:**
  * **request_id** (*str*) – 请求ID
  * **data** (*dict*) – 响应数据
* **抛出:**
  **AppBuilderServerException** – 如果响应数据中包含错误信息，则抛出异常
* **返回:**
  None

#### extract_img_urls(response: Text2ImageQueryResponse)

从作画生成的返回结果中提取图片url。

* **参数:**
  **(****obj** (*response*) – Text2ImageQueryResponse): 作画生成的返回结果。
* **返回:**
  从返回体中提取的图片url列表。
* **返回类型:**
  List[str]

#### manifests *= [{'description': '文生图，该组件只用于图片创作。当用户需要进行场景、人物、海报等内容的绘制时，使用该画图组件。如果用户需要生成图表（柱状图、折线图、雷达图等），则必须使用代码解释器。', 'name': 'text_to_image', 'parameters': {'properties': {'query': {'description': '文生图用的query。特别注意，这个字段只能由中文字符组成，不能含有任何英语描述。', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### queryText2ImageData(request: Text2ImageQueryRequest, timeout: float | None = None, retry: int = 0, request_id: str | None = None) → Text2ImageQueryResponse

将文本查询请求转换为图像数据。

* **参数:**
  * **request** (*Text2ImageQueryRequest*) – 输入请求，必填参数。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间，默认为None。
  * **retry** (*int* *,* *optional*) – 请求的重试次数，默认为0。
  * **request_id** (*str* *,* *optional*) – 请求的唯一标识符，默认为None。
* **返回:**
  接口返回的输出消息。
* **返回类型:**
  Text2ImageQueryResponse

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), width: int = 1024, height: int = 1024, image_num: int = 1, image: str | None = None, url: str | None = None, pdf_file: str | None = None, pdf_file_num: str | None = None, change_degree: int | None = None, text_content: str | None = None, task_time_out: int | None = None, text_check: int | None = 1, request_id: str | None = None)

执行文本到图像的生成任务。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 包含任务相关信息的消息对象。
  * **width** (*int* *,* *optional*) – 生成的图像的宽度，默认为1024。
  * **height** (*int* *,* *optional*) – 生成的图像的高度，默认为1024。
  * **image_num** (*int* *,* *optional*) – 生成图像的数量，默认为1。
  * **image** (*Optional* *[**str* *]* *,* *optional*) – 参考图像的路径或URL，默认为None。
  * **url** (*Optional* *[**str* *]* *,* *optional*) – 参考图像的URL，默认为None。
  * **pdf_file** (*Optional* *[**str* *]* *,* *optional*) – 参考PDF文件的路径，默认为None。
  * **pdf_file_num** (*Optional* *[**str* *]* *,* *optional*) – 参考PDF文件中的页码范围，默认为None。
  * **change_degree** (*Optional* *[**int* *]* *,* *optional*) – 图像变换的程度，默认为None。
  * **text_content** (*Optional* *[**str* *]* *,* *optional*) – 需要转换的文本内容，默认为None。
  * **task_time_out** (*Optional* *[**int* *]* *,* *optional*) – 任务超时时间，默认为None。
  * **text_check** (*Optional* *[**int* *]* *,* *optional*) – 是否进行文本内容检查，默认为1。
  * **request_id** (*Optional* *[**str* *]* *,* *optional*) – 请求的唯一标识，默认为None。
* **返回:**
  包含生成图像URL的消息对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **HTTPError** – 请求失败时抛出异常。

#### submitText2ImageTask(request: Text2ImageSubmitRequest, timeout: float | None = None, retry: int = 0, request_id: str | None = None) → Text2ImageSubmitResponse

使用给定的输入并返回文生图的任务信息。

* **参数:**
  * **(****obj** (*request*) – Text2ImageSubmitRequest): 输入请求，这是一个必需的参数。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间。默认为None。
  * **retry** (*int* *,* *optional*) – 请求的重试次数。默认为0。
  * **request_id** (*str* *,* *optional*) – 请求的唯一标识符。默认为None。
* **返回:**
  Text2ImageSubmitResponse: 接口返回的输出消息。
* **返回类型:**
  obj
