# appbuilder.core.components.mix_card_ocr package

## Submodules

## appbuilder.core.components.mix_card_ocr.component module

身份证混贴识别组件

### *class* appbuilder.core.components.mix_card_ocr.component.MixCardOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

身份证混贴识别组件

Examples:

```python
import os
import requests
import appbuilder

os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
# 从BOS存储读取样例文件
image_url="https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T06%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe1865e4393da5a3515e90d72d81ef18296bd29598"
raw_image = requests.get(image_url).content
# 输入参数为一张图片
inp = appbuilder.Message(content={"raw_image": raw_image})
# 进行识别
mix_card_ocr = MixCardOCR()
out = mix_card_ocr.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '当身份证正反面在同一张图片上，需要识别图片中身份证正反面所有字段时，使用该工具', 'name': 'mixcard_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别文件的文件名', 'items': {'type': 'string'}, 'type': 'array'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'mixcard_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行身份证识别操作

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 包含待识别图片或图片下载URL的Message对象.
    示例: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”}).
  * **timeout** (*float* *,*  *可选*) – HTTP请求的超时时间，默认为None.
  * **retry** (*int* *,*  *可选*) – HTTP请求的重试次数，默认为0.
* **返回:**
  包含身份证识别结果的Message对象.
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

对指定文件进行OCR识别。

* **参数:**
  * **name** (*str*) – API名称。
  * **streaming** (*bool*) – 是否流式输出。如果为True，则逐个返回识别结果；如果为False，则一次性返回所有识别结果。
  * **\*\*kwargs** – 其他参数。
* **返回:**
  如果streaming为False，则返回包含所有识别结果的JSON字符串。
  如果streaming为True，则逐个返回包含识别结果的字典，每个字典包含以下字段：
  > type (str): 消息类型，固定为”text”。
  > text (str): 识别结果的JSON字符串。
  > visible_scope (str): 消息可见范围，可以是”llm”或”user”。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误，即文件URL不存在时抛出。

#### version *= 'v1'*
