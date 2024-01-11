# 短语音识别-极速版 (Automatic Speech Recognition) 

## 简介
短语音识别（ASR）可以将音频流实时识别为文字，并返回每句话的开始和结束时间，适用于手机语音输入、语音搜索、人机对话等语音交互场景。

## 基本用法

下面是短语音识别的代码示例：

```python
import os
import requests
import appbuilder
# 设置环境变量和初始化
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

asr = appbuilder.ASR()

audio_file_url = "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                   "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                   "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
audio_data = requests.get(audio_file_url).content
content_data = {"audio_format": "pcm", "raw_audio": audio_data, "rate": 16000}
msg = appbuilder.Message(content_data)
out = asr.run(msg)
print(out.content)
```
## 参数说明
### 初始化参数

无

### 调用参数
- `run`函数中包含以下参数：
   - `message`: 输入的消息，用于模型的主要输入内容。这是一个必需的参数，例如：Message(content={"raw_audio": b"..."})
   - `audio_format`: 定义语言文件的格式，包括"pcm"、"wav"、"amr"、"m4a"，默认值为"pcm"。
   - `rate`: 定义录音采样率，固定值16000
   - `timeout`: HTTP超时时间
   - `retry`: HTTP重试次数

返回值示例：eg: {"result": ["北京科技馆。"]}

## 高级用法

目前该模块仅提供基础的语音识别功能。


## 更新记录和贡献
* 短语音识别能力 (2023-12)