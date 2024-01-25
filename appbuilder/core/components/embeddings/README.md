# 向量计算（Embedding）

## 简介

向量计算组件（Embedding）支持将文本转化为用数值表示的向量形式，用于文本检索、信息推荐、知识挖掘等场景。嵌入（Embedding）是一种在机器学习和自然语言处理中常用的技术，主要用于将大量高维数据（如单词、图像等）转换为更低维的向量表示。这些向量表示捕获了原始数据的关键特征和关系。

### 功能介绍

1. 维度降低：将高维数据（如词汇表中的单词）映射到低维空间，使得数据处理更高效。
2. 特征学习：学习数据的内在特征，使得具有相似含义的元素在嵌入空间中彼此接近。
3. 关系映射：在嵌入空间中，数据点的距离和方向可以表示元素之间的关系。

### 特色优势

Embedding-V1，是基于百度文心大模型技术的文本表示模型，在Embedding模块中，我们使用Embedding-V1作为默认模型。

### 应用场景

1. 文本检索
2. 信息推荐
3. 知识挖掘

## 基本用法

当前支持的embedding底座模型暂时只包括：
- embedding-v1

### 下面是使用单条字符串测试的代码示例

请注意，您必须确保字符串的token长度小于384

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()

out = embedding("hello world!")
# 得到一个长度为384的float数组
print(out.content)
```

### 下面是使用多条字符串测试的代码示例

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()

outs = embedding.batch(["hello", "world"])
# 得到一个长度为 2 x 384的float 二维数组
print(out.content)
```

### 下面是使用上游的Message作为输入的代码示例

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()

query = Message("你好，世界！")
out = embedding(query)
# 得到一个长度为384的float数组
print(out.content)
```

### 下面是批量运行的代码示例

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()

query = Message([
    "你好",
    "世界"
])
outs = embedding.batch(query)
# 得到一个长度为 2 x 384的float 二维数组
print(outs.content)
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

| 参数名称 | 参数类型 | 是否必须 | 描述                                                         | 示例值           |
| -------- | -------- | -------- | ------------------------------------------------------------ | ---------------- |
| model    | 字符串   | 可选     | 指定底座模型的类型。当前仅支持 embedding-v1 作为可选值。若不指定，默认值为 embedding-v1。 | embedding-v1   |

### 调用参数

#### 单条

| 参数名称 | 参数类型 | 是否必须 | 描述                                                         | 示例值           |
| -------- | -------- | -------- | ------------------------------------------------------------ | ---------------- |
| text     | 字符串   | 必须     | 一个类型为 string 的句子，用于输入。该句子的长度不能超过384个字符，通常为用户的输入。 | "您好，我需要帮助。" |

#### 批量

| 参数名称 | 参数类型        | 是否必须 | 描述                                                             | 示例值                               |
| -------- | --------------- | -------- | ---------------------------------------------------------------- | ------------------------------------ |
| texts    | 字符串列表      | 必须     | 一个类型为 List[string] 的句子数组。数组中的每个元素都是一个句子，且每个句子的长度不能超过384个字符。通常这些句子为和用户输入相关的文本候选集。 | ["您好，我需要帮助。", "请问有什么可以帮您？"] |

### 响应示例

#### 单条

```
[0.1, 0.2, 0.3, ....]
```

#### 批量

```
[
    [0.1, 0.2, ...],
    ...,
    [0.1, 0.2, ...],
]
```

### 错误码

无

### 使用示例

#### 单条字符串

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()

embedding("hello world!")
```

#### 多条字符串

```python
import appbuilder
from appbuilder import Message
# 请先确保您设置了密钥
embedding = appbuilder.Embedding()

embedding.batch(["hello", "world"])
```

## 更新记录和贡献

* embedding-v1 (2023-12)
