# 口语化Query生成（OralQueryGeneration）

## 简介
口语化Query生成组件（OralQueryGeneration）可以基于输入文本生成与文档内容相关的Query。可用于增强文档索引等场景。

## 基本用法
### 快速开始
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
        '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
        '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
        '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
        '，实时视频分享您的生活。')
oral_query_generation = appbuilder.OralQueryGeneration(model='eb-turbo-appbuilder')
answer = oral_query_generation(appbuilder.Message(text))
print(answer.content)
```

## 参数说明
### 初始化参数
- `model` (str|None): 模型名称，用于指定要使用的千帆模型。

### 调用参数
- `message` (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
- `stream` (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
- `temperature` (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
### 返回
- `Message`: 模型运行后的输出消息。

## 更新日志
### 2023.12.07
#### [Added]
- 增加口语化Query生成能力。
- 增加口语化Query生成单元测试。