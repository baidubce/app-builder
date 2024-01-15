# 会话小结（DialogSummary）

## 简介
会话小结（DialogSummary）基于生成式大模型对一段用户与坐席的对话生成总结，结果按{"诉求": "", "回应": "", "解决情况": ""}格式输出。适用于运营商、金融、汽车等多种场景的对话总结。

## 基本用法

为了快速开始使用会话小结组件，您可以参考以下步骤：

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

model = "eb-turbo-appbuilder"
dialog_summary = appbuilder.DialogSummary(model)
text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
answer = dialog_summary(appbuilder.Message(text))
print(answer)
```

## 参数说明

### 初始化参数
- `model` (str|None): 模型名称，用于指定要使用的千帆模型。

### 调用参数
- `message (Message)`: 输入消息，用于模型的主要输入内容。这是一个必需的参数。
- `stream (bool)`: 是否以流式形式返回响应。默认为 False。
- `temperature (float)`: 模型的生成概率调整参数。范围为 0.0 到 1.0，默认为 1e-10。

### 返回值
- 返回一个 `Message` 对象，包含模型运行后的输出消息。

## 高级用法

暂无

## 示例和案例研究

目前暂无具体的实际应用案例。

## API文档

暂无

## 更新记录和贡献

- 初始版本发布。
- 如您希望为会话小结组件贡献代码或反馈，请参考 [贡献指南](#)。
