# 语义匹配（Matching）

## 简介

语义匹配组件（Matching）可以计算query与文本列表之间的相似度关系，并根据其进行排序。

## 基本用法

初始化

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

# 初始化所需要的组件
embedding = appbuilder.Embedding()
matching = appbuilder.Matching(embedding)

# 定义query和文本列表
query = appbuilder.Message("你好")
contexts = appbuilder.Message(["世界", "你好"])
```

### 基于query和文本之间的相似度进行匹配排序

```python
contexts_matched = matching(query, contexts)
print(contexts_matched.content)
```

```
['你好', '世界']
```

## 参数说明

#### 初始化参数说明

- embedding：【必须】一个类型为Embedding的Component，用于初始化`Matching`的向量计算功能

#### 调用参数说明

- query：【必须】一个类型为string的句子，长度不能超过384，通常为用户输入的问题
- contexts：【必须】一个类型为List[string]的句子数组，每个元素长度不能超过384，通常为和问题相关的文本候选集

## 高级用法

### 对query和文本计算相似度

使用如下的示例代码，可以直接计算query和文本间的余弦相似度，用于判别不同的embedding模型之间的性能差异

```python
query_embedding = embedding(query)
context_embedding = embedding.batch(contexts)

semantics = matching.semantics(query_embedding, context_embedding)

print(semantics.content)
```

```
[0.1892052043984527, 0.9999999852985002]
```
