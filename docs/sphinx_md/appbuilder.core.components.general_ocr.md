# appbuilder.core.components.general_ocr package

## Submodules

## appbuilder.core.components.general_ocr.component module

general ocr component.

### *class* appbuilder.core.components.general_ocr.component.GeneralOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

提供通用文字识别能力，在通用文字识别的基础上，提供更高精度的识别服务，支持更多语种识别（丹麦语、荷兰语、马来语、
瑞典语、印尼语、波兰语、罗马尼亚语、土耳其语、希腊语、匈牙利语、泰语、越语、阿拉伯语、印地语及部分中国少数民族语言），
并将字库从1w+扩展到2w+，能识别所有常用字和大部分生僻字。

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

general_ocr = appbuilder.GeneralOCR()
with open("./general_ocr_test.png", "rb") as f:
    out = general_ocr.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### manifests *= [{'description': '提供更高精度的通用文字识别能力，能够识别图片中的文字，不支持html后缀文件的输入', 'name': 'general_ocr', 'parameters': {'anyOf': [{'required': ['img_url']}, {'required': ['img_name']}], 'properties': {'img_name': {'description': '待识别图片的文件名,用于生成图片url', 'type': 'string'}, 'img_url': {'description': '待识别图片的url,根据该url能够获取图片', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'general_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行图片中的文字识别。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行识别操作。举例: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP重试次数。
* **返回:**
  模型识别结果。举例: Message(content={“words_result”:[{“words”:”100”}, {“words”:”G8”}]})。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

根据给定的参数执行OCR识别功能。

* **参数:**
  * **name** (*str*) – 函数名称，此处未使用，但为保持一致性保留。
  * **streaming** (*bool*) – 是否以流式方式返回结果。如果为True，则逐个返回结果，否则返回全部结果。
  * **kwargs** – 关键字参数，支持以下参数：
    traceid (str): 请求的唯一标识符，用于追踪请求和响应。
    img_url (str): 待识别图片的URL。
    file_urls (dict): 包含文件名和对应URL的字典。如果提供了img_url，则忽略此参数。
    img_name (str): 待识别图片的文件名，与file_urls配合使用。
* **返回:**
  如果streaming为False，则返回包含识别结果的JSON字符串。
  如果streaming为True，则逐个返回包含识别结果的字典。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误（例如未设置文件名或指定文件名对应的URL不存在），则抛出此异常。

#### version *= 'v1'*
