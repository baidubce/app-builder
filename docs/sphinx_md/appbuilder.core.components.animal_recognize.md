# appbuilder.core.components.animal_recognize package

## Submodules

## appbuilder.core.components.animal_recognize.component module

animal recognize component.

### *class* appbuilder.core.components.animal_recognize.component.AnimalRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出动物识别结果。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

animal_recognition = appbuilder.AnimalRecognition()
with open("./animal_recognition_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### manifests *= [{'description': '用于识别图片中动物类别，可识别近八千种动物', 'name': 'animal_rec', 'parameters': {'anyOf': [{'required': ['img_name']}, {'required': ['img_url']}], 'properties': {'img_name': {'description': '待识别图片的文件名', 'type': 'string'}, 'img_url': {'description': '待识别图片的url', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'animal_rec'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行动物识别

* **参数:**
  * **(****obj** (*message*) – Message): 用于执行识别操作的输入图片或图片url下载地址。
    例如：Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间
  * **retry** (*int* *,*  *可选*) – HTTP重试次数
* **返回:**
  Message): 识别结果。
  : 例如：Message(name=msg, content={‘result’: [{‘name’: ‘国宝大熊猫’, ‘score’: ‘0.945917’}, {‘name’: ‘秦岭四宝’, ‘score’: ‘0.0417291’},
    {‘name’: ‘团团圆圆’, ‘score’: ‘0.00584368’}, {‘name’: ‘圆仔’, ‘score’: ‘0.000846628’}, {‘name’: ‘棕色大熊猫’, ‘score’: ‘0.000538988’},
    {‘name’: ‘金丝猴’, ‘score’: ‘0.000279618’}]}, mtype=dict)
* **返回类型:**
  message (obj

#### tool_eval(name: str, streaming: bool, origin_query: str, \*\*kwargs) → Generator[str, None, None] | str

用于工具的执行，通过调用底层接口进行动物识别。

* **参数:**
  * **name** (*str*) – 工具名。
  * **streaming** (*bool*) – 是否流式返回。
  * **origin_query** (*str*) – 用户原始query。
  * **\*\*kwargs** – 工具调用的额外关键字参数。
* **返回:**
  动物识别结果，包括识别出的动物类别和相应的置信度信息。
* **返回类型:**
  Union[Generator[str, None, None], str]

#### version *= 'v1'*

## Module contents
