# appbuilder.core.components.tts package

## Submodules

## appbuilder.core.components.tts.component module

text to speech component.

### *class* appbuilder.core.components.tts.component.TTS(\*args, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文本转语音组件，即输入一段文本将其转为一段语音

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
tts = appbuilder.TTS()

# 默认使用baidu-tts模型, 默认返回MP3格式
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp)
with open("sample.mp3", "wb") as f:
    f.write(out.content["audio_binary"])

# 使用paddlespeech-tts模型，目前只支持返回WAV格式
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp, model="paddlespeech-tts", audio_type="wav")
with open("sample.wav", "wb") as f:
    f.write(out.content["audio_binary"])
```

#### Baidu_TTS *= 'baidu-tts'*

#### PaddleSpeech_TTS *= 'paddlespeech-tts'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), model: Literal['baidu-tts', 'paddlespeech-tts'] = 'baidu-tts', speed: int = 5, pitch: int = 5, volume: int = 5, person: int = 0, audio_type: Literal['mp3', 'wav', 'pcm'] = 'mp3', timeout: float = None, retry: int = 0, stream: bool = False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行文本转语音。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 待转为语音的文本。
    举例: Message(content={“text”: “欢迎使用百度语音”})如果选择baidu-tts模型，text最大文本长度为1024 GBK编码长度,大约为512个中英文字符;如果选择paddlespeech-tts模型, text最大文本长度是510个字符。
  * **model** (*str* *,*  *可选*) – 默认是\`baidu-tts\`模型，可设置为\`paddlespeech-tts\`。
  * **speed** (*int* *,*  *可选*) – 语音语速，默认是5中等语速，取值范围在0~15之间，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **pitch** (*int* *,*  *可选*) – 语音音调，默认是5中等音调，取值范围在0~15之间，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **volume** (*int* *,*  *音量*) – 语音音量，默认是5中等音量，取值范围在0~15之间，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **person** (*int* *,*  *可选*) – 语音人物特征，默认是0,
    可选值包括度小宇=1 度小美=0 度逍遥（基础）=3 度丫丫=4 度逍遥（精品）=5003
    度小鹿=5118 度博文=106 度小童=110 度小萌=111 度米朵=103 度小娇=5，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **audio_type** (*str* *,*  *可选*) – 音频文件格式，默认是\`mp3\`，
    如果选择\`paddlespeech-tts\`模型，参数只能设为\`wav\`。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP重试次数。
  * **stream** (*bool* *,*  *可选*) – 是否以流的形式返回音频数据，默认为False。
* **返回:**
  文本转语音结果。举例: Message(content={“audio_binary”: b”xxx”, “audio_type”: “mp3”})
* **返回类型:**
  message ([Message](appbuilder.core.md#appbuilder.core.message.Message))
