# appbuilder.core.components.asr package

## Submodules

## appbuilder.core.components.asr.component module

ASR component.

### *class* appbuilder.core.components.asr.component.ASR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

ASR组件，即对于输入的语音文件，输出语音识别结果

Examples:

```python
import appbuilder
asr = appbuilder.ASR()
os.environ["APPBUILDER_TOKEN"] = '...'

with open("xxxx.pcm", "rb") as f:
    audio_data = f.read()
content_data = {"audio_format": "pcm", "raw_audio": audio_data, "rate": 16000}
msg = appbuilder.Message(content_data)
out = asr.run(msg)
print(out.content) # eg: {"result": ["北京科技馆。"]}
```

#### manifests *= [{'description': '对于输入的语音文件进行识别，输出语音识别结果。', 'name': 'asr', 'parameters': {'anyOf': [{'required': ['file_url']}, {'required': ['file_name']}], 'properties': {'file_name': {'description': '待识别语音文件名,用于生成获取语音的url', 'type': 'string'}, 'file_type': {'description': '语音文件类型,支持pcm/wav/amr/m4a', 'enum': ['pcm', 'wav', 'amr', 'm4a'], 'type': 'string'}, 'file_url': {'description': '输入语音文件的url,根据url获取到语音文件', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'asr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), audio_format: str = 'pcm', rate: int = 16000, timeout: float = None, retry: int = 0, \*\*kwargs) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行语音识别操作，并返回识别结果。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息对象，包含待识别的音频数据。该参数为必需项，格式如：Message(content={“raw_audio”: b”…”})。
  * **audio_format** (*str* *,* *optional*) – 音频文件格式，支持pcm/wav/amr/m4a，不区分大小写，推荐使用pcm格式。默认为”pcm”。
  * **rate** (*int* *,* *optional*) – 音频采样率，固定为16000。默认为16000。
  * **timeout** (*float* *,* *optional*) – HTTP请求超时时间。默认为None。
  * **retry** (*int* *,* *optional*) – HTTP请求重试次数。默认为0。
* **返回:**
  语音识别结果，格式如：Message(content={“result”: [“识别结果”]})。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

评估给定文件名或文件URL的语音识别结果。

* **参数:**
  * **name** (*str*) – 函数调用名称。
  * **streaming** (*bool*) – 是否以流的方式返回结果。
  * **\*\*kwargs** – 关键字参数，用于指定文件名、文件URL等参数。
* **返回:**
  如果streaming为True，则通过生成器逐个返回包含识别结果的消息对象；
  如果streaming为False，则返回包含识别结果的JSON字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 如果未设置文件名或文件URL不存在，则抛出此异常。

#### version *= 'v1'*
