# console端知识库操作助手

## 目标
用户可通过SDK对console端知识库进行操作，实现创建知识库、添加知识文档、查询知识库文档、删除知识文档等操作，可在平台console中查看结果。

```python
#  设置环境变量
import os

#  设置环境变量
#  请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."
```

## 管理知识库

### 初始化已有知识库
获取线上已有知识库的ID，可在[console](https://console.bce.baidu.com/ai_apaas/dataset)端查看，示例

<img width="1536" alt="image" src="./image/dataset示例.png">

```python
import appbuilder
# 初始化已有线上知识库, dataset_id 可在平台console中查看
dataset_id = "..."
dataset = appbuilder.console.Dataset(dataset_id)
```

### 创建全新知识库

```python
# 创建全新知识库
dataset = appbuilder.console.Dataset.create_dataset("my_dataset")
```

### 上传文档到知识库

```python
# 设置文档路径，例如“./test.pdf”
file_path1 = "..."
file_path2 = "..."
file_paths = [file_path1, file_path2]
# 将文档上传到知识库
document_infos = dataset.add_documents(file_paths)
print(document_infos)
```

### 获取知识库关联文档
```python
# 获取第一页的文档列表, 每页10条
document_list = dataset.get_documents(1, 10)
print(document_list)
```

### 删除知识库中的文档
```python
# 删除第一个文档
document_ids = [document_list.data[0].id]
dataset.delete_documents(document_ids)
```

### 知识库使用示例

- [知识库使用示例](https://github.com/baidubce/app-builder/blob/master/cookbooks/end2end_application/rag/qa_system_1_dataset.ipynb)