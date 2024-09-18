# 文本精排（Reranker）

## 简介
文本精排能力，将Query召回到的N个候选文本段落进行精排；保证与Query相关程度越高的文本段落排序越靠前，提升检索效果。

### 功能介绍
文本精排（Reranker）用于检索排序，输入为Query和Top K个段落，输出为每个段落的排序得分；Query相关程度越高的文本段落排序越靠前，用于提升检索效果。

### 特色优势
- 高效准确：基于开源模型[
bce-reranker](https://huggingface.co/maidalun1020/bce-reranker-base_v1)的能力，提供高效且准确的内容检索功能。[百度云推理服务Api](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/xlu216rqn)

### 应用场景
检索排序场景


## 基本用法

以下是有关如何开始使用BESRetriever的代码示例：

```python
import os
import appbuilder
from appbuilder import Message

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

reranker = appbuilder.Reranker()
ranked_1 = reranker("你好", ["他也好", "hello?"])
print(ranked_1)

# 使用上游的Message作为输入的代码示例
ranked_2 = reranker(appbuilder.Message("你好"), appbuilder.Message(["他也好", "hello?"]))
print(ranked_2)
```

## 参数说明
### 初始化参数说明：

| 参数名称 | 参数类型 |是否必须 | 描述 | 示例值 |
|---------|--------|--------|------------------|---------------|
| model | str |是 | 指定底座模型的类型。当前仅支持 bce-reranker-base 作为可选值。若不指定，默认值为 bce-reranker-base。 | bce-reranker-base |


### 调用参数：

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
|---------|--------|--------|------------------|---------------|
| query | str |是 | 精排Query，长度小于1600。 | "你好" |
| texts | List[str] | 是 | 精排输入段落，会对列表里的所有内容排序，最大长度为50. | ["你好", "世界"] |


### 响应示例
#### 输入
```python
query="你好", text=["他也好", "hello?"]
```

#### 响应
```json
[
    {
        "document": "hello?",
        "relevance_score": 0.5651187300682068,
        "index": 1
    },
    {
        "document": "他也好",
        "relevance_score": 0.47729530930519104,
        "index": 0
    }
]
```


### 错误码

无

## 更新记录和贡献

* reranker-base (2024-08)
