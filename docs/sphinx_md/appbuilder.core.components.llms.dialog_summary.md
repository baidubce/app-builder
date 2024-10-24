# appbuilder.core.components.llms.dialog_summary package

## Submodules

## appbuilder.core.components.llms.dialog_summary.component module

### *class* appbuilder.core.components.llms.dialog_summary.component.DialogSummary(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

会话小结大模型组件， 基于生成式大模型对一段用户与坐席的对话生成总结，结果按{“诉求”: “”, “回应”: “”, “解决情况”: “”}格式输出。

Examples:

```python
import app
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

dialog_summary = appbuilder.DialogSummary("ERNIE Speed-AppBuilder")
text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
answer = dialog_summary(appbuilder.Message(text))
print(answer)
```

#### meta

`DialogSummaryArgs` 的别名

#### name *: str* *= 'dialog_summary'*

#### run(message, stream=False, temperature=1e-10, top_p=0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*
