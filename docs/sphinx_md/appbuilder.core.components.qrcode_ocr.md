# appbuilder.core.components.qrcode_ocr package

## Submodules

## appbuilder.core.components.qrcode_ocr.component module

qrcode ocr component.

### *class* appbuilder.core.components.qrcode_ocr.component.QRcodeOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

qrcode_ocr = appbuilder.QRcodeOCR()
with open("./qrcode_ocr_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read(),"location": "true"}))
print(out.content)
```

#### manifests *= [{'description': '需要对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息，使用该工具', 'name': 'qrcode_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别文件的文件名', 'items': {'type': 'string'}, 'type': 'array'}, 'location': {'description': '是否输出二维码/条形码位置信息', 'type': 'string'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'qrcode_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), location: str = 'true', timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行二维码识别操作。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入的图片或图片URL下载地址，用于执行识别操作。例如：
    Message(content={“raw_image”: b”…”, “location”: “”}) 或
    Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **location** (*str* *,*  *可选*) – 是否需要返回二维码位置信息，默认为 “true”。
  * **timeout** (*float* *,*  *可选*) – HTTP请求的超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP请求的重试次数。
* **返回:**
  识别结果，包含识别到的二维码信息。例如：
  : Message(name=msg, content={‘codes_result’: [{‘type’: ‘QR_CODE’, ‘text’: [’[http://weixin.qq.com/r/cS7M1PHE5qyZrbW393tj](http://weixin.qq.com/r/cS7M1PHE5qyZrbW393tj)’],
    : ’location’: {‘top’: 63, ‘left’: 950, ‘width’: 220, ‘height’: 211}}, …]}, mtype=dict)
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **InvalidRequestArgumentError** – 如果 location 参数非法，将抛出该异常。

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

评估工具函数

* **参数:**
  * **name** (*str*) – 工具名称
  * **streaming** (*bool*) – 是否流式输出
  * **\*\*kwargs** – 其他关键字参数
* **关键字参数:**
  * **traceid** (*str*) – 请求的traceid
  * **file_names** (*List* *[**str* *]*) – 文件名列表
  * **locations** (*str*) – 是否需要获取位置信息，可选值为’true’或’false’，默认为’false’
  * **file_urls** (*Dict* *[**str* *,* *str* *]*) – 文件名到文件URL的映射
* **返回:**
  如果streaming为True，则返回一个生成器，生成两个字典，分别代表LLM和用户可见的内容；
  : 如果streaming为False，则返回一个JSON字符串，包含评估结果
* **返回类型:**
  Union[str, Generator[Dict[str, Any], None, None]]
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误，或者位置信息不合法，则抛出该异常

#### version *= 'v1'*
