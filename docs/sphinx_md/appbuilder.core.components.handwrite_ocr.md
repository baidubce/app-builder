# appbuilder.core.components.handwrite_ocr package

## Submodules

## appbuilder.core.components.handwrite_ocr.component module

手写文字识别组件

### *class* appbuilder.core.components.handwrite_ocr.component.HandwriteOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

手写文字识别组件

Examples:

```python
import os
import appbuilder
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
# 从BOS存储读取样例文件
image_url="https://bj.bcebos.com/v1/appbuilder/test_handwrite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b"
# 输入参数为一张图片
inp = appbuilder.Message(content={"url": image_url})
# 进行植物识别
handwrite_ocr = HandwriteOCR()
out = handwrite_ocr.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '需要对图片中手写体文字进行识别时，使用该工具，不支持PDF文件，如果用户没有提供图片文件，应引导用户提供图片，而不是尝试使用该工具', 'name': 'handwriting_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别文件的文件名', 'items': {'type': 'string'}, 'type': 'array'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'handwriting_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

输入图片并识别其中的文字

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行识别操作.例如: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”}).
  * **timeout** (*float* *,* *optional*) – HTTP超时时间. 默认为None.
  * **retry** (*int* *,* *optional*) – HTTP重试次数. 默认为0.
* **返回:**
  手写体模型识别结果.
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

对指定文件或URL进行手写识别。

* **参数:**
  * **name** (*str*) – 任务名称。
  * **streaming** (*bool*) – 是否以流式形式返回结果。
  * **kwargs** – 其他参数，包括：
    traceid (str, optional): 请求的traceid，用于标识请求的唯一性。默认为None。
    file_names (List[str], optional): 待识别的文件名列表。默认为None，此时会从kwargs中获取’files’参数。
    file_urls (Dict[str, str], optional): 文件名与URL的映射字典。默认为空字典。
* **返回:**
  如果streaming为True，则以生成器形式返回识别结果，否则直接返回结果字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误，例如指定的文件名对应的URL不存在。

#### version *= 'v1'*
