# 短文本在线合成（TTS）

## 简介
短文本在线合成组件（TTS）提供高度拟人、流畅自然的语音合成服务，将文本朗读出来，基础音库性价比更高，精品音库听感更逼真。

### 功能介绍
提供高度拟人、流畅自然的语音合成服务。

### 特色优势
将文本朗读出来，基础音库性价比更高，精品音库听感更逼真。可实时生成语音输出，几乎没有延迟，更加自然流畅。

### 应用场景
文本朗读


## 基本用法

下面是语音合成的代码示例：
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
tts = appbuilder.TTS()
cwd = os.getcwd()

# 使用baidu-tts模型, 默认返回MP3格式
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp)
mp3_sample_path = os.path.join(cwd,"sample.mp3")
with open(mp3_sample_path, "wb") as f:
    f.write(out.content["audio_binary"])
print("成功将文本转语音，mp3格式文件已写入：{}".format(mp3_sample_path))

# 使用paddlespeech-tts模型，目前只支持返回WAV格式
wav_sample_path = os.path.join(cwd,"sample.wav")
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp, model="paddlespeech-tts", audio_type="wav")
with open(wav_sample_path, "wb") as f:
    f.write(out.content["audio_binary"])
print("成功将文本转语音，wav格式文件已写入：{}".format(wav_sample_path))
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 

os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数

无

### 调用参数
| 参数名称       | 参数类型    | 是否必须 | 描述                                                                                                                                                                                             | 示例值                                 |
|------------|---------|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| message    | String  | 是    | 待转成语音的文本                                                                                                                                                                                       | Message(content={"text": "需合成的文本"}) |
| model      | String  | 否    | 默认是`baidu-tts`模型，可选值：`paddlespeech-tts`、`baidu-tts`                                                                                                                                            | paddlespeech-tts                    |
| speed      | Integer | 否    | 语音语速，默认是5中等语速，取值范围在0~15之间，仅当模型为`baidu-tts`参数有效，如果模型为`paddlespeech-tts`，参数自动失效                                                                                                                  | 5                                   |
| pitch      | Integer | 否    | 语音音调，默认是5中等音调，取值范围在0~15之间，仅当模型为`baidu-tts`参数有效，如果模型为`paddlespeech-tts`，参数自动失效                                                                                                                  | 5                                   |
| volume     | Integer | 否    | 语音音量，默认是5中等音量，取值范围在0~15之间，,仅当模型为`baidu-tts`参数有效，如果模型为`paddlespeech-tts`，参数自动失效                                                                                                                 | 5                                   |
| person     | Integer | 否    | 语音人物特征，默认是0(度小美),普通音库可选值包括: 0(度小美)、1(度小宇)、3(度逍遥-基础)、4(度丫丫)；精品音库包括：5003(度逍遥-精品)、  5118(度小鹿) 、106(度博文)、 110(度小童)、 111(度小萌)、 103(度米朵)、 5(度小娇),仅当模型为`baidu-tts`参数有效，如果模型为`paddlespeech-tts`，参数自动失效 | 0                                   |
| audio_type | String  | 否    | 音频文件格式，如果使用`baidu-tts`模型可选`mp3`, `wav`; 如果使用`paddlespeech-tts`模型非流式返回，参数只能设为`wav`;如果使用`paddlespeech-tts`模型流式返回，参数只能设为`pcm`                                                                     | wav                                 |
| stream     | Bool    | 否    | 默认是False, 目前`paddlespeech-tts`模型支持流式返回，`baidu-tts`模型不支持流式返回                                                                                                                                    | False                               |
| retry      | Integer | 否    | HTTP重试次数                                                                                                                                                                                       | 3                                   |
| timeout    | Integer | 否    | HTTP超时时间                                                                                                                                                                                       | 5                                   |

### 非流式语音响应参数
| 参数名称          | 参数类型   | 描述     | 示例值     |
|---------------|--------|--------|---------|
| content       | Dict   | 消息内容   | 无       |
| +audio_binary | Bytes  | 音频二进制流 | b'语音流'  |
| +audio_type   | String | 音频类型   | wav/mp3 |


### 流式语音响应参数
| 参数名称    | 参数类型             | 描述       | 示例值 |
|---------|------------------|----------|-----|
| content | Python Generator | 可迭代的二进制流 | 无   |


### 响应示例
```json
{
"content": {
             "audio_binary": "",
              "audio_type": "mp3"
           }
}
```


### 错误码
| 错误码 | 描述 |
|-----|----|

## 高级用法

### TTS实时播放语音流
```python
import os
import appbuilder
import pyaudio

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
tts = appbuilder.TTS()
# 使用paddlespeech-tts模型，目前只支持返回WAV格式
inp = appbuilder.Message(content={"text": """随着科技的迅速发展，教育领域也经历了巨大的变革。科技不仅改变了教学和学习的方式，还扩展了教育的可能性和边界。
        从在线课程到交互式学习工具，科技为学生和教师提供了前所未有的资源和机遇。科技使得个性化学习成为可能。通过智能学习系统和适应性学习技术，
        教育内容可以根据学生的学习速度和能力进行定制。"""})
# 仅支持model为paddlespeech-tts，audio_type为pcm, stream为True
out = tts.run(inp, model="paddlespeech-tts", audio_type="pcm", stream=True)
play = pyaudio.PyAudio()
stream = play.open(format=play.get_format_from_width(2),
                    channels=1,
                    rate=24000,
                    output=True,
                    frames_per_buffer=2048)
# 实时播放语音流
for pcm in out.content:
    stream.write(pcm)
stream.stop_stream()
stream.close()
```
### pcm文件转wav

```python
import os
import appbuilder
import wave

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
tts = appbuilder.TTS()
inp = appbuilder.Message(content={"text": """随着科技的迅速发展，教育领域也经历了巨大的变革。科技不仅改变了教学和学习的方式，还扩展了教育的可能性和边界。
        从在线课程到交互式学习工具，科技为学生和教师提供了前所未有的资源和机遇。科技使得个性化学习成为可能。通过智能学习系统和适应性学习技术，
        教育内容可以根据学生的学习速度和能力进行定制。"""})
# 仅支持model为paddlespeech-tts，audio_type为pcm, stream为True
out = tts.run(inp, model="paddlespeech-tts", audio_type="pcm", stream=True)
count = 1
cwd = os.getcwd()
for pcm in out.content:
    wave_sample_path = os.path.join(cwd, "{}.wav".format(count))
    wavfile = wave.open(wave_sample_path, 'wb')
    wavfile.setnchannels(1)
    wavfile.setsampwidth(2)
    wavfile.setframerate(24000)
    wavfile.writeframes(pcm)
    wavfile.close()
    print("成功将第{}个pcm语音块转换成wav格式，并将对应文件写入：{}".format(count, wave_sample_path))
    count += 1
```


## 更新记录和贡献
* 短文本在线合成 (2024-01)
* 增加流式能力 (2024-02)

