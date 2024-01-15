# 复杂Query判定（IsComplexQuery）

## 简介
复杂Query判定组件（IsComplexQuery）可以根据输入的提问进行初步的分类，区分简单问题和复杂问题，以便后续运用不同的处理流程处理。可应用于知识问答场景。

## 基本用法

下面是一个基本的使用示例：

```python
import os
import appbuilder


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

is_complex_query = appbuilder.IsComplexQuery(model="eb-turbo-appbuilder")

msg = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
msg = appbuilder.Message(msg)
answer = is_complex_query(msg)

print("Answer: \n{}".format(answer.content))
```

## 参数说明

* 初始化参数说明

  - `model` (str|None): model (str|None): 模型名称，用于指定要使用的千帆模型。
  
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
answer = is_complex_query(msg, stream=True, temperature=0.5)
```

## 示例和案例研究

### 示例

- **场景:** 用户提出问题
- **输入:** "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
- **输出:** 分析：这个问题涉及到吸塑包装盒在工业化生产和物流运输中的重要性。回答这个问题需要从多个角度来考虑，比如生产方面、运输方面、环保方面等。这需要对吸塑包装盒有深入的了解，并且需要考虑到生产、运输等各个环节。因此，这是一个复杂问题。
类型：复杂问题