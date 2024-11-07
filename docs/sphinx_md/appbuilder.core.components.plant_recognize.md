# appbuilder.core.components.plant_recognize package

## Submodules

## appbuilder.core.components.plant_recognize.component module

植物识别组件

### *class* appbuilder.core.components.plant_recognize.component.PlantRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

植物识别组件，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的植物识别结果

Examples:

```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
image_url = "https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2188d971ca547c53d01742af4a2cbe"

# 从BOS存储读取样例文件
raw_image = requests.get(image_url).content
inp = appbuilder.Message(content={"raw_image": raw_image})
# inp = Message(content={"url": image_url})

# 运行植物识别
plant_recognize = appbuilder.PlantRecognition()
out = plant_recognize.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '用于识别图片中植物类别', 'name': 'plant_rec', 'parameters': {'anyOf': [{'required': ['img_name']}, {'required': ['img_url']}], 'properties': {'img_name': {'description': '待识别图片的文件名', 'type': 'string'}, 'img_url': {'description': '待识别图片的url', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'plant_rec'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

输入图片并识别其中的植物

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={“raw_image”: b”…”})
  * **Message****(****content={"url"** ( *或*) – “[https://image/download/uel](https://image/download/uel)”}).
  * **timeout** (*float* *,* *optional*) – HTTP超时时间，默认为None
  * **retry** (*int* *,* *optional*) – HTTP重试次数，默认为0
* **返回:**
  模型识别结果
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, origin_query: str, \*\*kwargs) → Generator[str, None, None] | str

用于工具的执行，通过调用底层接口进行植物识别

* **参数:**
  * **name** (*str*) – 工具名
  * **streaming** (*bool*) – 是否流式返回
  * **origin_query** (*str*) – 用户原始query
  * **\*\*kwargs** – 工具调用的额外关键字参数
* **返回:**
  植物识别结果，包括识别出的植物类别和相应的置信度信息
* **返回类型:**
  Union[Generator[str, None, None], str]

#### version *= 'v1'*
