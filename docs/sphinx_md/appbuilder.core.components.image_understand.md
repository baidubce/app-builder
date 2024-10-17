# appbuilder.core.components.image_understand package

## Submodules

## appbuilder.core.components.image_understand.component module

图像内容理解

### *class* appbuilder.core.components.image_understand.component.ImageUnderstand(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

图像内容理解组件，即对于输入的一张图片（可正常解码，且长宽比适宜）与问题，输出对图片的描述

Examples:

```python
import os
import appbuilder
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
# 从BOS存储读取样例文件
image_url = "https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bfe25c372b7e56e6"
# 输入参数为一张图片
inp = Message(content={"url": image_url, "question": "图片里内容是什么?"})
# 进行图像内容理解
image_understand = ImageUnderstand()
out = image_understand.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '可对输入图片进行理解，可输出图片描述、OCR 及图像识别结果', 'name': 'image_understanding', 'parameters': {'anyOf': [{'required': ['img_name']}, {'required': ['img_url']}], 'properties': {'img_name': {'description': '待识别图片的文件名', 'type': 'string'}, 'img_url': {'description': '待识别图片的url', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'image_understanding'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行图像内容理解

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={“raw_image”: b”…”, “question”: “图片主要内容是什么？”})
    或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”, “question”: “图片主要内容是什么？”}).
  * **timeout** (*float* *,* *optional*) – HTTP超时时间. 默认为 None.
  * **retry** (*int* *,* *optional*) – HTTP重试次数. 默认为 0.
* **返回:**
  模型识别结果.
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, origin_query: str, \*\*kwargs) → Generator[str, None, None] | str

用于工具的执行，调用底层接口进行图像内容理解

* **参数:**
  * **name** (*str*) – 工具名
  * **streaming** (*bool*) – 是否流式返回
  * **origin_query** (*str*) – 用户原始query
  * **\*\*kwargs** – 工具调用的额外关键字参数
* **返回:**
  图片内容理解结果
* **返回类型:**
  Union[Generator[str, None, None], str]

#### version *= 'v1'*
