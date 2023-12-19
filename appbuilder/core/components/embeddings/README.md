# 向量计算（Embedding）

## 简介

语义向量计算组件（Embedding）支持将文本转化为用数值表示的向量形式，用于文本检索、信息推荐、知识挖掘等场景

Embedding-V1，是基于百度文心大模型技术的文本表示模型，在Embedding模块中，我们使用Embedding-V1作为默认模型

## 基本用法

### 初始化

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()
```

### 使用单条字符串测试

请注意，您必须确保字符串的token长度小于384

```python
out = embedding("hello world!")
# 得到一个长度为384的float数组
print(out.content)
```

### 使用多条字符串测试

```python
outs = embedding.batch(["hello", "world"])
# 得到一个长度为 2 x 384的float 二维数组
print(out.conetnt)
```

### 使用上游的Message作为输入

```python
query = Message("你好，世界！")
out = embedding(query)
# 得到一个长度为384的float数组
print(out.content)
```

### 批量运行

```python
query = Message([
    "你好",
    "世界"
])
outs = embedding.batch(query)
# 得到一个长度为 2 x 384的float 二维数组
print(outs.content)
```

## 参数说明

### 初始化参数说明

无

### 调用参数说明

#### 单条字符串

```python
embedding("hello world!")
```

- text：【必须】一个类型为`string`的句子，长度不能超过384，通常为用户的输入

#### 多条字符串

```python
embedding.batch(["hello", "world"])
```

- texts：【必须】一个类型为`List[string]`的句子数组，每个元素长度不能超过384，通常为和用户输入相关的文本候选集
