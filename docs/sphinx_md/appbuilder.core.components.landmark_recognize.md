# appbuilder.core.components.landmark_recognize package

## Submodules

## appbuilder.core.components.landmark_recognize.component module

landmark recognize component.

### *class* appbuilder.core.components.landmark_recognize.component.LandmarkRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

识别地标组件，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的地标识别结果

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
landmark_recognize = appbuilder.LandmarkRecognition()
with open("xxxx.jpg", "rb") as f:
    inp = appbuilder.Message(content={"raw_image": f.read()})
    out = landmark_recognize.run(inp)
    # 打印识别结果
    print(out.content) # eg: {"landmark": "狮身人面相"}
```

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行地标识别任务

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息对象，包含待识别的图片或图片URL。
    例如：Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,* *optional*) – HTTP请求的超时时间。默认为None。
  * **retry** (*int* *,* *optional*) – HTTP请求的重试次数。默认为0。
* **返回:**
  地标识别结果的消息对象。
  : 例如：Message(content={“landmark”: b”狮身人面像”})
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
