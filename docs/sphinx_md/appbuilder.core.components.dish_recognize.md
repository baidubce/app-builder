# appbuilder.core.components.dish_recognize package

## Submodules

## appbuilder.core.components.dish_recognize.component module

菜品识别组件.

### *class* appbuilder.core.components.dish_recognize.component.DishRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

菜品识别组件，适用于识别只含有单个菜品的图片，返回识别的菜品名称和卡路里信息

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

dish_recognition = appbuilder.DishRecognition()

with open("xxxx.jpg", "rb") as f:
    resp = dish_recognition(appbuilder.Message({"raw_image": f.read()}))
    # 输出示例 {'result': [{'name': '剁椒鱼头', 'calorie': '127'}]}
    print(resp.content)
```

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

根据输入图片进行菜品识别。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入待识别图片，支持传图片二进制流和图片URL。
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为 None。
  * **retry** (*int* *,* *optional*) – 重试次数，默认为 0。
* **返回:**
  包含菜品识别结果的输出消息。例如，Message(content={‘result’: [{‘name’: ‘剁椒鱼头’, ‘calorie’: ‘127’}]})
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
