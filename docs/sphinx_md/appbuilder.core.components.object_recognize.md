# appbuilder.core.components.object_recognize package

## Submodules

## appbuilder.core.components.object_recognize.component module

object recognize component.

### *class* appbuilder.core.components.object_recognize.component.ObjectRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

提供通用物体及场景识别能力，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的多
个物体及场景标签。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

object_recognition = appbuilder.ObjectRecognition()
with open("./object_recognition_test.jepg", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### manifests *= [{'description': '提供通用物体及场景识别能力，即对于输入的一张图片，输出图片中的多个物体及场景标签。', 'name': 'object_recognition', 'parameters': {'anyOf': [{'required': ['img_url']}, {'required': ['img_name']}], 'properties': {'img_name': {'description': '待识别图片的文件名,用于生成图片url', 'type': 'string'}, 'img_url': {'description': '待识别图片的url,根据该url能够获取图片', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'object_recognition'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

通用物体识别

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行识别操作。
    例如: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,* *optional*) – HTTP超时时间，默认为None。
  * **retry** (*int* *,* *optional*) – HTTP重试次数，默认为0。
* **返回:**
  模型识别结果。
  : 例如: Message(content={“result”:[{“keyword”:”苹果”,
    : ”score”:0.94553,”root”:”植物-蔷薇科”},{“keyword”:”姬娜果”,”score”:0.730442,”root”:”植物-其它”},
      {“keyword”:”红富士”,”score”:0.505194,”root”:”植物-其它”}]})
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

评估并识别传入图像中的物体或场景。

* **参数:**
  * **name** (*str*) – 调用此方法的对象名称。
  * **streaming** (*bool*) – 是否以流式方式返回结果。如果是True，则以生成器形式返回结果；如果是False，则直接返回字符串形式的识别结果。
  * **\*\*kwargs** – 任意关键字参数，支持以下参数：
    traceid (str, optional): 请求的追踪ID，用于追踪请求处理流程。默认为None。
    img_url (str, optional): 待识别图像的URL地址。默认为None，如果未指定，则尝试从file_urls和img_name参数中获取图像路径。
    file_urls (dict, optional): 包含文件名和对应URL的字典。默认为空字典。
    img_name (str, optional): 待识别图像的文件名。如果img_url未指定，则根据img_name从file_urls中获取图像的URL。默认为None。
    score_threshold (float, optional): 置信度阈值，低于此阈值的识别结果将被忽略。默认为0.5。
* **返回:**
  如果streaming为True，则返回一个生成器，生成器中的元素为包含识别结果的字典，字典包含以下键：
  : type (str): 结果类型，固定为”text”。
    text (str): 识别结果的JSON字符串表示。
    visible_scope (str): 结果的可见范围，’llm’表示仅对LLM可见，’user’表示对用户可见。

  如果streaming为False，则直接返回识别结果的JSON字符串表示。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误（如未设置文件名或文件URL不存在），则抛出此异常。

#### version *= 'v1'*
