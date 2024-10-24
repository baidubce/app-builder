# appbuilder.core.components.llms.tag_extraction package

## Submodules

## appbuilder.core.components.llms.tag_extraction.component module

### *class* appbuilder.core.components.llms.tag_extraction.component.TagExtraction(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

标签抽取组件，基于生成式大模型进行关键标签的抽取。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

tag_extraction = appbuilder.TagExtraction(model="ERNIE Speed-AppBuilder")
answer = tag_extraction(appbuilder.Message("从这段文本中抽取关键标签"))
```

#### meta

`TagExtractionArgs` 的别名

#### name *: str* *= 'tag_extraction'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message, 必选): 输入消息，用于模型的主要输入内容。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*
