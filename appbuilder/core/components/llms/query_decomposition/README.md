# 复杂Query分解（QueryDecomposition）

## 简介
复杂Query分解组件（QueryDecomposition）可以将已经确定为复杂问题的原始问题拆解为一个个简单问题。广泛应用在知识问答场景。

## 基本用法

下面是一个基本的使用示例：

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = "..."

query_decomposition = appbuilder.QueryDecomposition(model="eb-turbo-appbuilder")

msg = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
msg = appbuilder.Message(msg)
answer = query_decomposition(msg)

print("Answer: \n{}".format(answer.content))
```

## 参数说明

* 初始化参数说明

  - `model` (str|None): 模型名称，用于指定要使用的千帆模型。

* 调用参数说明

  - `message (obj:Message)`: 输入消息，用于模型的主要输入内容。这是一个必需的参数。

  - `stream (bool, 可选)`: 指定是否以流式形式返回响应。默认为 False。

  - `temperature (float, 可选)`: 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

返回值：

- `obj:Message`: 模型运行后产生的输出消息。

## 高级用法

你可以根据特定的场景调整参数来获得更精确的结果，例如：

```python
# 流式返回, 调整模型temperature参数
answer = query_decomposition(msg, stream=True, temperature=0.5)
```

## 示例和案例研究

### 示例

- **场景:** 用户提出问题
- **输入:** "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
- **输出:** 
1. 吸塑包装盒在工业化生产中有什么重要性？
2. 吸塑包装盒在物流运输中有什么重要性？