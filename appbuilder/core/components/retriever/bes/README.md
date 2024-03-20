# 向量检索-BES（BaiduElasticSearchRetriever）

## 简介
向量检索-BES组件（BaiduElasticSearchRetriever）基于一款Baidu ElasticSearch的内容检索组件，支持根据文本的向量的相似度进行内容检索。

### 功能介绍
向量检索-BES组件（BaiduElasticSearchRetriever）用于在将文本内容输入到Baidu ElasticSearch，根据文本的向量相似度进行高效的内容检索。

### 特色优势
- 高效准确：基于Baidu ElasticSearch的强大能力，提供高效且准确的内容检索功能。

### 应用场景
各种内容检索场景

## 准备工作
在使用BaiduElasticSearchRetriever进行内容检索之前，需要到Baidu ElasticSearch官网创建相应的集群，详情见[教程](https://cloud.baidu.com/doc/BES/s/gke3ocf89)。

注：创建集群时请选择7.10.2版本的ES，否则可能无法使用本组件。

## 基本用法

以下是有关如何开始使用BESRetriever的代码示例：

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

embedding = appbuilder.Embedding()
segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
# 初始化构建索引
vector_index = appbuilder.BESVectorStoreIndex.from_segments(segments=segments, cluster_id=es_cluster_id, user_name=es_username, 
                                                            password=es_password, embedding=embedding)
# 获取当前索引中的全部内容
all_content = vector_index.get_all_segments()
print(all_content)
# 转化为retriever
retriever = vector_index.as_retriever()
# 按照query进行检索
query = appbuilder.Message("文心一言")
res = retriever(query=query, top_k=1)
print(res)
# 删除当前索引中的全部内容
vector_index.delete_all_segments()
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
- cluster_id （str，必填）：ElacticSearch集群的id，创建集群时获取
- user_name  （str，必填）：连接ES集群所需的用户名，创建集群时获取
- password   （str，必填）：连接ES集群所需的密码，创建集群时获取
- embedding  （obj，非必填）：用于将文本转为向量的模型，默认为Embedding

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
* 向量检索能力 (2023-12)