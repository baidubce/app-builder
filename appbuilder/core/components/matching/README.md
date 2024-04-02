# 语义匹配（Matching）

## 简介

语义匹配组件（Matching）可以计算query与文本列表之间的相似度关系，并根据其进行排序。

### 功能介绍

根据query与文本列表之间的相似度关系，并根据其进行排序。

### 特色优势

基于百度文心大模型技术的文本表示模型，学习数据的内在特征，使得排序效果相较于bm25等排序算法，可以更好地处理相似问和同义、近义句子之间的偏序关系。

### 应用场景

1. 语义排序

## 基本用法

### 下面是基于query和文本之间的相似度进行匹配排序的代码示例

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

# 初始化所需要的组件
embedding = appbuilder.Embedding()
matching = appbuilder.Matching(embedding)

# 定义query和文本列表
query = appbuilder.Message("你好")
contexts = appbuilder.Message(["世界", "你好"])

contexts_matched = matching(query, contexts)
print(contexts_matched.content)
```

```
['你好', '世界']
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

| 参数名称   | 参数类型    | 是否必须 | 描述                                                          | 示例值          |
| ---------- | ----------- | -------- | ------------------------------------------------------------- | --------------- |
| embedding  | Embedding   | 可选     | 一个类型为Embedding的Component，用于初始化 Matching 的向量计算功能。底座模型当前仅支持 embedding-v1 作为可选值。若不指定，默认值为 embedding-v1 。 |  appbuilder.Embedding()   |

### 调用参数

| 参数名称  | 参数类型    | 是否必须 | 描述                                                         | 示例值                             |
| --------- | ----------- | -------- | ------------------------------------------------------------ | ---------------------------------- |
| query     | 字符串      | 必须     | 一个类型为 string 的句子，用于输入。该句子的长度不能超过384个字符，通常为用户输入的问题。 | "如何提高工作效率？"                |
| contexts  | 字符串列表   | 必须     | 一个类型为 List[string] 的句子数组。数组中的每个元素都是一个句子，且每个句子的长度不能超过384个字符。这些句子通常为与问题相关的文本候选集。 | ["时间管理技巧", "提高专注力的方法"]  |
| return_score | 布尔 | 可选 | 默认为False, 仅返回排序后的字符串列表；当设置为True时，返回匹配分数和字符串的二元组列表 |

### 响应示例

默认为排完序后的字符串列表

```
["时间管理技巧", "提高专注力的方法"]
```

当设置`return_score = True`时，二元组的第一个值为相似度分数，第二个值为字符串

```
[(0.9999999852985002, '你好'), (0.18920520439845268, '世界')]
```

### 错误码

无

## 更新记录和贡献

* 语义匹配 (2023-12)
