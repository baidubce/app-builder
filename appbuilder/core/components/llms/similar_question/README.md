# 相似问生成组件（SimilarQuestion）

## 简介
相似问生成组件（SimilarQuestion）可以用于基于输入的问题，挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。

## 基本用法

### 快速开始

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

similar_question = appbuilder.SimilarQuestion(model="eb-turbo-appbuilder")

msg = "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
msg = appbuilder.Message(msg)
answer = similar_question(msg)

print("Answer: \n{}".format(answer.content))
```

## 参数说明

### 初始化参数

- `model` (str|None): 模型名称，用于指定要使用的千帆模型。

### 调用参数

- `message` (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
- `stream` (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
- `temperature` (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

### 返回值

- 返回一个对象 `Message`，包含模型运行后的输出消息。

## 高级用法

### 特殊场景示例

你可以根据特定的场景调整参数来获得更精确的结果，例如：

```python
# 流式返回, 调整模型temperature参数
answer = similar_question(msg, stream=True, temperature=0.5)
```

## 示例和案例研究

### 示例

- **场景:** 用户提出问题
- **输入:** "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
- **输出:** 1. 请问哪里的冰淇淋最美味？ 2. 在哪些地方可以品尝到最好的冰淇淋？ .....

