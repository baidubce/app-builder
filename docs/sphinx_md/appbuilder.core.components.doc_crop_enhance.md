# appbuilder.core.components.doc_crop_enhance package

## Submodules

## appbuilder.core.components.doc_crop_enhance.component module

doc_crop_enhance component.

### *class* appbuilder.core.components.doc_crop_enhance.component.DocCropEnhance(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

对图片中的文件、卡证、票据等内容进行四角点检测定位，提取主体内容并对其进行矫正，同时可选图片增强效果进一步提升图片清晰度，
达到主体检测矫正并增强的目的，提升图片整体质量

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

doc_crop_enhance = appbuilder.DocCropEnhance()
with open("./doc_enhance_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), enhance_type: int = 0, timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

文档矫正增强

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入图片或图片url下载地址用于执行操作。举例: Message(content={“raw_image”: b”…”,
  * **"enhance_type"** – 3})或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **enhance_type** (*int* *,*  *可选*) – 选择是否开启图像增强功能，如开启可选择增强效果，可选值如下：
    - 0：默认值，不开启增强功能
    - 1：去阴影
    - 2：增强并锐化
    - 3：黑白滤镜。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间
  * **retry** (*int* *,*  *可选*) – HTTP重试次数
* **返回:**
  识别结果。举例: Message(name=msg, content={‘image_processed’: ‘…’,
  ‘points’: [{‘x’: 220, ‘y’: 705}, {‘x’: 240, ‘y’: 0}, {‘x’: 885, ‘y’: 2}, {‘x’: 980, ‘y’: 759}]},
  mtype=dict)
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
