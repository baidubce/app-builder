# 知识库组件（Dataset）(即将下线)

## 简介

知识库组件（Dataset）是对线上知识库操作的组件，可以通过SDK实现创建知识库、添加知识文档、查询知识库文档、删除知识文档等操作，可在平台console中查看结果。

### 功能介绍

对console端知识库进行操作，可以通过SDK实现创建知识库、添加知识文档、查询知识库文档、删除知识文档等操作，可在平台console中查看结果。

### 特色优势

和console端知识库操作一致，可实现快速创建、查询、删除等操作。

### 应用场景

通过SDK代码实现console端知识库操作。

## 基本用法

### Python

#### 组件初始化参数

| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| dataset_id | string | 线上数据集ID | "正确的数据集ID" |

#### 创建知识库调用参数

| 参数名称         | 参数类型   | 是否必须 | 描述     | 示例值          |
|--------------|--------|------|--------|--------------|
| dataset_name | String | 是    | 知识库的名字 | "my_dataset" |

#### 创建知识库响应参数

| 参数名称   | 参数类型    | 描述        | 示例值                                                                               |
|--------|---------|-----------|-----------------------------------------------------------------------------------|
| result | Dataset | dataset实例 | Dataset(dataset_id=2dae2091-99dc-47dd-8600-ff7c4b3ed93d, dataset_name=my_dataset) |

响应示例：

```
Dataset(dataset_id=2dae2091-99dc-47dd-8600-ff7c4b3ed93d, dataset_name=my_dataset)
```

#### 添加文档调用参数

| 参数名称                   | 参数类型         | 是否必须 | 描述                                                                                                                                                                    | 示例值                                                                  |
|------------------------|--------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| file_paths             | List[String] | 是    | 文档路径列表                                                                                                                                                                | ["./path1", "./path2"]                                               |
| is_custom_process_rule | bool         | 否    | 是否使用自定义文档处理策略                                                                                                                                                         | True                                                                 |
| custom_process_rule    | Dict         | 否    | 自定义文档处理策略，在is_custom_process_rule为True时需要设置，separators文本切分符，支持这几种[ , , "？", , "!", "?", "……"]，target_length是文本切片片段长度，取值范围[300, 800]，overlap_rate是文本片段重叠率，取值范围[0, 0.3] | {"separators":["。", "，"], "target_length": 300, "overlap_rate": 0.3} |
| is_enhanced            | bool         | 否    | 是否开启知识增强，在检索问答时通过知识点来索引到对应的切片，大模型根据切片内容生成答案，开启知识增强会调用大模型抽取更加丰富的知识点，增加切片的召回率                                                                                           | False                                                                |

#### 添加文档响应参数

| 参数名称   | 参数类型                 | 描述       | 示例值                                                                                                                           |
|--------|----------------------|----------|-------------------------------------------------------------------------------------------------------------------------------|
| result | AddDocumentsResponse | 添加文档响应信息 | AddDocumentsResponse(dataset_id='4437e170-876a-4634-9469-2ff6b76584e7' document_ids=['a279f3f2-e779-45c8-85ba-19f63c1c1316']) |

响应示例：

```
AddDocumentsResponse(dataset_id='4437e170-876a-4634-9469-2ff6b76584e7' document_ids=['a279f3f2-e779-45c8-85ba-19f63c1c1316'])
```

#### 获取文档列表调用参数

| 参数名称    | 参数类型   | 是否必须 | 描述       | 示例值  |
|---------|--------|------|----------|------|
| page    | int    | 是    | 页码，从1开始  | 1    |
| limit   | int    | 是    | 每页包含文档数量 | 10   |
| keyword | string | 否    | 关键词匹配    | "ai" |

#### 获取文档列表响应参数

| 参数名称   | 参数类型                 | 描述     | 示例值                                                                                                                                                                                                                                                                                              |
|--------|----------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| result | DocumentListResponse | 文档列表对象 | DocumentListResponse(data=[FileInfo(id='a279f3f2-e779-45c8-85ba-19f63c1c1316', name='test.pdf', created_at=1706515108, indexing_status='parsing', error=None, enabled=True, disabled_at=None, disabled_by=None, display_status='处理中', word_count=0)], has_more=False, limit=10, total=1, page=1) |

响应示例：

```
DocumentListResponse(data=[FileInfo(id='a279f3f2-e779-45c8-85ba-19f63c1c1316', name='test.pdf', created_at=1706515108, indexing_status='parsing', error=None, enabled=True, disabled_at=None, disabled_by=None, display_status='处理中', word_count=0)], has_more=False, limit=10, total=1, page=1)
```

#### 删除文档调用参数

| 参数名称         | 参数类型         | 是否必须 | 描述     | 示例值            |
|--------------|--------------|------|--------|----------------|
| document_ids | List[String] | 是    | 文档id列表 | ["1234567890"] |

#### 删除文档响应参数

无

#### 示例代码

下面是示例代码，相应的操作结果可在平台console中查看，与console端同步

```python
import appbuilder
import os
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."

# 初始化已有线上知识库，dataset_id 可在平台console中查看获取，详情可在下方初始化参数部分查看
dataset_id = "..."
dataset = appbuilder.console.Dataset(dataset_id)
# 或创建全新知识库
dataset = appbuilder.console.Dataset.create_dataset("my_dataset")

file_url = "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/test.pdf?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-01-25T12%3A56%3A15Z/-1/host/b54178fea9be115eafa2a8589aeadfcfaeba20d726f434f871741d4a6cb0c70d"
file_data = requests.get(file_url).content
file_path = "./test.pdf"  # 待解析的文件路径
with open(file_path, "wb") as f:
    f.write(file_data)

# 上传文档到知识库
file_paths = ["./test.pdf"]
document_infos = dataset.add_documents(file_paths)
print(document_infos)

# 获取第一页的文档列表, 每页10条
document_list = dataset.get_documents(1, 10)
print(document_list)

# 删除一个文档
document_ids = [document_infos.document_ids[0]]
dataset.delete_documents(document_ids)
```

### Java

#### 组件初始化参数

| 参数名称   | 参数类型      | 是否必须 | 描述      | 示例值 |
|--------|-----------|------|---------|-----|
| datasetId | String | 否|线上数据集ID，可通过createDataset()创建数据集 | "正确的数据集ID" |

#### 示例代码
```java
class DatasetDemo {
    public static void main(String[] args) throws IOException, AppBuilderServerException {
        // 填写自己的APPBUILDER_TOKEN
        System.setProperty("APPBUILDER_TOKEN", "填写秘钥");

        Dataset ds = new Dataset();
        // 创建数据集
        String datasetId = ds.createDataset("java创建数据集");
        System.out.println("datasetId:  " + datasetId);

        // 上传文档，填写正确的文件路径
        String filePath = "src/test/java/中秋节.docx";
        String[] documentIds = ds.addDocuments(new ArrayList<>(Collections.singletonList(filePath)), false, null, false);
        System.out.println("documentIds:  " + Arrays.toString(documentIds));

        // 获取文档列表
        DocumentListResponse resp = ds.getDocumentList(1, 20, "");
        System.out.println("document total num:  " + resp.getResult().getTotal());
        for (DocumentListData data : resp.getResult().getData()) {
            System.out.println("documentList:  " + data.getName());
        }
        // 删除文档
        ds.deleteDocuments(documentIds);
    }
}
```

### Go

#### 组件初始化参数

| 参数名称   | 参数类型      | 描述      | 示例值 |
|--------|-----------|---------|-----|
| config | SDKConfig | SDK配置信息 |     |

#### 示例代码

```Go
package main

import (
	"fmt"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"

)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://appbuilder.baidu.com
	os.Setenv("GATEWAY_URL", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化dataset实例
	dataset, _ := appbuilder.NewDataset(config)
	// 创建dataset
	datasetID, err := dataset.Create("name")
	if err != nil {
		fmt.Println("create dataset failed: ", err)
		return
	}
	// 上传文档
	documentID, err := dataset.UploadLocalFile(datasetID, "/Users/zhangxiaoyu15/Desktop/cv.pdf")
	if err != nil {
		fmt.Println("upload file failed: ", err)
		return
	}
	// 获取数据集下第一页不超过10篇文档
	_, err = dataset.ListDocument(datasetID, 1, 10, "")
	if err != nil {
		fmt.Println("list document failed: ", err)
		return
	}
	// 删除文档
	if err := dataset.DeleteDocument(datasetID, documentID); err != nil {
		fmt.Println("delete document failed: ", err)
		return
	}
}
```