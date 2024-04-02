# 风格写作（StyleWriting）

## 简介
风格写作组件（StyleWriting）是一款基于生成式大模型进行文本创作的工具，支持多种风格，包括B站、小红书等，适用于编写文案、广告等多种场景。

### 功能介绍
风格写作组件（StyleWriting）根据用户的输入内容和风格要求，利用大语言模型的生成能力，自动生成符合特定风格的文案。


### 特色优势
风格写作组件（StyleWriting），基于百度自研的大语言模型文新一言，提供内置的风格生成能力，无需更多的prompt描述，即可生成对应风格的文案。


### 应用场景
风格写作组件（StyleWriting）可用于特定平台的文案生成分发营销场景。


## 基本用法

为了快速开始使用风格写作组件，您可以参考以下步骤：

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

model = "ERNIE Speed-AppBuilder"
style_writing = appbuilder.StyleWriting(model)

query = "帮我写一篇关于人体工学椅的文案"
style = "小红书"
length = 100

msg = appbuilder.Message(query)
answer = style_writing(message=msg, style_query=style, length=length)
print(answer)
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数
|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
|message |Message  |是 |输入的消息，用于模型的主要输入内容，这是一个必需的参数。 |Message(content="帮我生成一个介绍保温杯的话术") |
|style_query |str |否 |定义生成文案的格式，包括"通用"、"B站"、"小红书"，默认为"通用" |"通用" |
|length |int |否 |定义生成文案的长度，可选 '短' (100), '中' (300), '长' (600), 默认100 |100 |
|stream |bool | 否 |指定是否以流式形式返回响应。默认为 False。 |False |
|temperature |float | 否 |模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。 |0.7 |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|result  |Message  |返回结果|Message(content="大家好，我给你们介绍一款家里和办公室都要备上的保温杯。...")|

### 响应示例
```
Message(name=msg, content=大家好，我给你们介绍一款家里和办公室都要备上的保温杯。我平常上班的时候都会装上一杯热开水，但用普通保温杯装上一会就凉了，所以我赶紧在网上淘了一个好货。它是双层设计，内层是不锈钢材质，外层是玻璃材质，非常贴心，冷热都能装。装上热水，保温效果非常出色，到晚上还是热的。这个保温杯的外观也非常漂亮，采用优质不锈钢材质，耐磨、易清洗。同时，它还非常轻便，可以轻松放入口袋、背包中。有了这个保温杯后，我再也不用担心喝水问题了。无论是在家里、办公室还是户外活动，它都能随时随地为你提供热水。而且，它还非常安全、健康，采用了优质的保温材料和先进的生产工艺。无论男女老少都可以使用这款保温杯哦。快来购买吧。", mtype=dict, extra={})
```

## 高级用法

使用风格写作组件进行更复杂的文本创作，例如调整不同的风格和长度参数来适应特定的写作场景。

## 更新记录和贡献

- 初始版本发布(2023-10)
