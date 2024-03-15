# 向量检索（Baidu VDB Retriever）

## 简介
向量检索组件（Baidu VDB Retriever）基于一款百度向量数据库的内容检索组件，支持根据文本的向量的相似度进行内容检索。

### 功能介绍
向量检索组件（Baidu VDB Retriever）用于在将文本内容输入到百度向量数据库，根据文本的向量相似度进行高效的内容检索。

### 特色优势
高效准确：基于百度向量数据库的强大能力，提供高效且准确的内容检索功能。

### 应用场景
各种内容检索场景

## 准备工作
在使用Baidu VDB Retriever进行内容检索之前，需要到百度向量数据库官网创建相应的实例，[教程](https://cloud.baidu.com/doc/VDB/s/hlrsoazuf)。

## 基本用法

以下是有关如何开始使用BaiduVDBRetriever的代码示例：

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

embedding = appbuilder.Embedding()
segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
# 初始化构建索引
vector_index = appbuilder.BaiduVDBVectorStoreIndex.from_params(
    instance_id=your_instance_id,
    api_key=your_api_key,
    drop_exists=True,
)
vector_index.add_segments(segments)

query = appbuilder.Message("文心一言")
retriever = vector_index.as_retriever()
res = retriever(query)
print(res)
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数说明：

- segments （Message[List[str]]，必填）：需要入库的文本段落
- instance_id（str，必填）：百度向量数据库的实例id，创建实例时获取
- api_key    （str，必填）：连接向量数据库所需的密码，创建实例时获取
- account    （str，非必填）：连接向量数据库所需的用户名，默认root
- embedding  （obj，非必填）：用于将文本转为向量的模型，默认为Embedding
- drop_exists (bool, 非必填) ：是否清空数据库历史记录，默认为False

### 调用参数：
| 参数名称    | 参数类型   |是否必须 | 描述               | 示例值           |
|---------|--------|--------|------------------|---------------|
| message | String |是 | 需要检索的内容          | "中国2023人均GDP" |
| top_k   | int    |否 | 返回相似度最高的top_k个内容 | 1             |

### 响应参数
| 参数名称 | 参数类型   | 描述  | 示例值                |
|------|--------|-----|--------------------|
| text | string | 检索结果 | "中国2023年人均GDP8.94万元" |
| score | float  | 相似度 | 0.95               |
| meta | dict   | 元信息 | ""                   |
### 响应示例
```json
{"text": "中国2023年人均GDP8.94万元", "score": 0.95, "meta": ""}
```

## 高级用法：

本组件根据向量的相似度进行检索，支持使用不同的embedding方法和索引方式来优化检索的效果。

## 更新记录和贡献
* 向量检索能力 (2024-03)
