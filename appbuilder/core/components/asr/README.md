# 短语音识别-极速版 (Automatic Speech Recognition) 

## 简介
短语音识别（ASR）可以将音频流实时识别为文字，并返回每句话的开始和结束时间，适用于手机语音输入、语音搜索、人机对话等语音交互场景。

### 功能介绍
通过极速API接口，将语音识别为文字，毫秒级响应，快速返回识别结果。

### 特色优势
采用领先国际的流式端到端建模方法SMLTA，近场普通话语音识别准确率可达98%；采用最新识别解码技术，识别速度提升5倍以上，极速返回识别结果；专有GPU服务集群、提供企业级的稳定服务，弹性灵活的高并发承载及高可靠性保障。
### 应用场景
语音输入、语音搜索、人机对话等。

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

### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

无

### 调用参数
|参数名称 |参数类型 |是否必须 |描述 | 示例值    |
|--------|--------|--------|----|--------|
|message |String  |是 |输入的消息，用于模型的主要输入内容。这是一个必需的参数| Message(content={"raw_audio": b"..."}) |
|audio_format|String|是 |定义语言文件的格式，包括"pcm"、"wav"、"amr"、"m4a"，默认值为"pcm"| pcm    |
|rate|Integer|是 |定义录音采样率，固定值16000| 16000  |
|timeout|Integer|是 |HTTP超时时间| 10     |
|retry|Integer|是 |HTTP重试次数| 3      |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |String  |返回结果|["北京科技馆。"]|
### 响应示例
```json
{"result": ["北京科技馆。"]}
```
### 错误码
| 错误码 |描述|
|---|---|
| 0 |success|
| 2000  |data empty|

## 高级用法

目前该模块仅提供基础的语音识别功能。


## 更新记录和贡献
* 短语音识别能力 (2023-12)