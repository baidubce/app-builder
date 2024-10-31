# 复杂Query判定（IsComplexQuery）

## 简介
复杂Query判定组件（IsComplexQuery）可以根据输入的提问进行初步的分类，区分简单问题和复杂问题，以便后续运用不同的处理流程处理。可应用于知识问答场景。

### 功能介绍
在知识问答领域中存在很多复杂问题需要处理，这些复杂问题通常需要进行问题分解并采用分治的方法处理。复杂Query判定组件尝试定义复杂问题和简单问题的概念，对用户的问题进行初步的分类，方便下游使用不同类型的流程来处理当前的简单问题/复杂问题。

### 特色优势
复杂Query判定组件通过对问题进行有效分类，系统可以更快速地将简单问题导向快速回答流程，而将复杂问题导向更深入的分析流程。这种判定能力可以提高整个问答系统的效率和准确性。

### 应用场景
广泛应用于知识问答场景

## 基本用法
下面是复杂Query判定的代码示例：
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

is_complex_query = appbuilder.IsComplexQuery(model="Qianfan-Appbuilder-Speed-8k")

msg = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
msg = appbuilder.Message(msg)
answer = is_complex_query(msg)

print("Answer: \n{}".format(answer.content))
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
|model |str  |是 |模型名称，用于指定要使用的千帆模型|Qianfan-Appbuilder-Speed-8k|

### 调用参数
|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
|message |obj:`Message`|是 |输入消息，用于模型的主要输入内容。这是一个必需的参数| |
|stream|bool|否 |指定是否以流式形式返回响应。默认为 False|False|
|temperature|float|否 |模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10|1e-10|

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
|Message |obj:`Message` |输出消息，包含模型运行后的输出| |

### 响应示例
```text
分析：这个问题涉及到吸塑包装盒在工业化生产和物流运输中的重要性。回答这个问题需要从多个角度来考虑，比如生产方面、运输方面、环保方面等。这需要对吸塑包装盒有深入的了解，并且需要考虑到生产、运输等各个环节。因此，这是一个复杂问题。
类型：复杂问题
```

### 错误码
无

## 高级用法
你可以通过自定义调整参数来获得想要的结果，例如：
```python
# 流式返回, 调整模型temperature参数
answer = is_complex_query(msg, stream=True, temperature=0.5)
```

## 更新记录和贡献
* 复杂Query判定 (2024-01)
