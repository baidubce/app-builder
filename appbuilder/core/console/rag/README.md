# console端RAG操作工具(RAG)

## 简介
RAG是基于线上RAG应用的问答组件，可以使用该组件利用线上RAG应用进行问答。

### 功能介绍
利用线上RAG应用进行问答

### 特色优势
与线上应用联动，利用线上RAG应用进行问答

### 应用场景
使用SDK利用线上RAG应用进行问答

## 基本用法
以下是使用SDK进行问答的示例代码
```python
import appbuilder
import os
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

app_id = '...' # 线上RAG应用ID，可在console端查看
rag_app = appbuilder.console.RAG(app_id)
query = "中国2023年的人均GDP是多少"
result = rag_app.integrated(appbuilder.Message(query))
# 输出运行结果
print(result.content)
# 获取reference
print(result.extra)
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
- `app_id`: 线上RAG应用的ID


### 调用参数 （以表格形式展示）
| 参数名称   | 参数类型   | 是否必须 | 描述                  | 示例值  |
|--------|--------|------|---------------------|------|
| query  | String | 是    | 提问的内容               | "北京的面积多大" |
| stream | bool   | 否    | 是否流式返回              | False|
| conversation_id | string | 否    | 不传默认新建会话 | ""|

### 响应参数
| 参数名称    | 参数类型       | 描述     | 示例值                                                   |
|---------|------------|--------|-------------------------------------------------------|
| content | String     | 返回结果   | "1.64万平方公里"                                           |
| extra   | List[Dict] | 返回结果来源 | ["id":"1", "content":"...", "from":"search_baidu"...] |


## 高级用法
暂无


## 更新记录和贡献
* 平台console端RAG应用能力 (2024-01)
