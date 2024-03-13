# 会话小结（DialogSummary）

## 简介
会话小结（DialogSummary）基于生成式大模型对一段用户与坐席的对话生成总结，结果按{"诉求": "", "回应": "", "解决情况": ""}格式输出。适用于运营商、金融、汽车等多种场景的对话总结。

### 功能介绍
基于生成式大模型对一段用户与坐席的对话生成总结。

### 特色优势
基于生成式大模型对一段用户与坐席的对话生成总结，结果按{"诉求": "", "回应": "", "解决情况": ""}格式输出。

### 应用场景
适用于运营商、金融、汽车等多种场景的对话总结。

## 基本用法

为了快速开始使用会话小结组件，您可以参考以下步骤：

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"

dialog_summary = appbuilder.DialogSummary("ERNIE Speed-AppBuilder")
text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
answer = dialog_summary(appbuilder.Message(text))
print(answer)
```

## 参数说明

### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
- `model` (str|None): 模型名称，用于指定要使用的千帆模型。

### 调用参数
### 调用参数
|参数名称 |参数类型 | 是否必须 | 描述                                                                          | 示例值           |
|--------|--------|---|-----------------------------------------------------------------------------|---------------|
|message |Message  | 是 | 输入消息，包含用户提出的问题。                                                             | Message("你好") |
|stream|bool| 否 | 是否以流式形式返回响应                                                                 | False         |
|temperature|float| 否 | 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。 | 0.0001        |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |Message  |返回结果|对象，包含模型运行后的输出消息。|
### 响应示例
```json
{"result": ["您话费余的话还有87.49元钱"]}
```
### 错误码
无

## 高级用法

暂无

## 示例和案例研究

目前暂无具体的实际应用案例。

## API文档

暂无

## 更新记录和贡献
* 会话小结更新Readme (2023-12)
