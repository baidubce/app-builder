# 空应用（Playground）

## 简介
Playground空应用（Playground）是一款灵活的组件，允许用户自定义prompt模板并执行。


### 功能介绍
Playground空应用（Playground）是一款灵活的组件，允许用户自定义prompt模板并执行。它适用于各种场景，特别是在需要自定义输入模板和使用预训练模型进行交互的情况下。

### 特色优势
灵活可自定义，用户可自由定义提示词，来跟大模型进行交互。

### 应用场景
在需要灵活定义提示词的场景，并且其他提供的开箱即用的组件无法满足的情况下使用。

## 基本用法

要开始使用 Playground，你需要设置prompt模板和模型名称。以下是一个基本示例：

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

play = appbuilder.Playground(
    prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。",
    model="ERNIE Speed-AppBuilder"
)
play(appbuilder.Message({"name": "小明", "bot_name": "小红", "bot_type": "聊天机器人", "bot_function": "聊天", "bot_question": "你好吗？"}), stream=False)
```

## 参数说明
### 初始化参数

| 参数名称           | 类型         | 说明                               |
|----------------|------------|----------------------------------|
| prompt_template | str        | 输入模板，用于指定prompt格式。                 |
| model           | str \| None | 模型名称，用于指定要使用的千帆模型。 |

### 调用参数

| 参数名称      | 类型            | 说明                         | 默认值  |
|-----------|---------------|----------------------------|------|
| message   | obj:`Message` | 输入消息，必需参数。              | 无    |
| stream    | bool          | 是否以流式形式返回响应。           | False |
| temperature | float        | 模型配置的温度参数。              | 1e-10 |

### 响应参数

| 类型             | 说明                 |
|----------------|--------------------|
| obj:`Message` | 模型运行后的输出消息。 |

### 响应示例
```json
{"result": "北京科技馆。"}
```

### 错误码
|错误码|描述|
|------|---|


## 高级用法
此部分可根据实际应用场景提供更复杂的示例和用法说明。

## 示例和案例研究
目前暂无具体案例，将在未来更新。

## API文档
无

## 更新记录和贡献
- 2024年01月24日 更新Readme格式，调整请求参数样式，新增特色优势
