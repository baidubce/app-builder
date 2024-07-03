# 知识库组件（KnowledgeBase）

## 简介

知识库组件（KnowledgeBase）是对线上知识库操作的组件，可以通过SDK实现创建知识库、添加知识文档、查询知识库文档、删除知识文档等操作，可在平台console中查看结果。

### 功能介绍

对console端知识库进行操作，可以通过SDK实现创建知识库、添加知识文档、查询知识库文档、删除知识文档等操作，可在平台console中查看结果。

### 特色优势

和console端知识库操作一致，可实现快速创建、查询、删除等操作。

### 应用场景

通过SDK代码实现console端知识库操作。

## Python基本用法

### 1、新建知识库`KnowledgeBase().create_knowledge(knowledge_name: str) -> KnowledgeBase()`

#### 方法参数
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| knowledge_name | string | 希望创建的知识库名称 | "我的知识库" |

#### 方法返回值
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| KnowledgeBase | class KnowledgeBase | 实例化的知识库类 | - |

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge = appbuilder.KnowledgeBase().create_knowledge("my_knowledge")
print("新建的知识库ID: ", my_knowledge.knowledge_id)
print("新建的知识库名称: ", my_knowledge.knowledge_name)

# 新建的知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 新建的知识库名称:  my_knowledge
```

### 2、实例化已创建的知识库 `KnowledgeBase(knowledge_id: str)`

#### 方法参数

| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| knowledge_id | string | 线上知识库ID | "正确的数据集ID" |

#### 方法返回值
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| KnowledgeBase | class KnowledgeBase | 实例化的知识库类 | - |

#### 方法示例
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

# 知识库ID:  your_knowledge_base_id
```

### 3、上传通用文档 `KnowledgeBase().upload_file(file_path: str)->KnowledgeBaseUploadFileResponse`

#### 方法参数
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| file_path | string | 本地的文件路径 | "/home/my_doc" |

#### 方法返回值
`KnowledgeBaseUploadFileResponse` 类定义如下
```python
class KnowledgeBaseUploadFileResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    id: str = Field(..., description="文件ID")
    name: str = Field(..., description="文件名称")
```


#### 方法示例
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

upload_res = my_knowledge.upload_file("./test.txt")
print(upload_res)

# 知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# request_id='255eec22-ec87-4564-bdeb-3e5623eaxxxx' id='ef12119b-d5be-492a-997c-77f8e84axxxx' name='test.txt'
```
### 4、向知识库添加文档 `KnowledgeBase().add_document()->KnowledgeBaseAddDocumentResponse`

#### 方法参数
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| content_type | enum[str] | 知识库文档类型，有raw_text和qa两种可选，分别对应文本文档 和 结构化的excel问答对 | "raw_text" |
| file_ids | list[str] | 文件ID列表，文件ID通过`upload_file`接口获得 | ['ef12119b-d5be-492a-997c-77f8e84axxxx'] |
| is_enhanced | bool | 文档是否开启基于大模型的知识增强 | False |
| custom_process_rule | CustomProcessRule | 文档的自定义切分逻辑 | `appbuilder.CustomProcessRule(separators=["?"], target_length=400,overlap_rate=0.2)` |


`CustomProcessRule` 类定义如下：
```python
class CustomProcessRule(BaseModel):
    separators: list[str] = Field(..., description="分段符号列表", example=[",", "?"])
    target_length: int = Field(..., description="分段最大长度", ge=300, le=1200)
    overlap_rate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25", ge=0, le=0.3, example=0.2)

```

#### 方法返回值
方法返回`KnowledgeBaseAddDocumentResponse`，该类定义如下：
```python
class KnowledgeBaseAddDocumentResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    knowledge_base_id: str = Field(..., description="知识库ID")
    document_ids: list[str] = Field(..., description="成功新建的文档id集合")

```

#### 方法示例
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

upload_res = my_knowledge.upload_file("./test.txt")
print("文件上传结果: ",upload_res)

add_res = my_knowledge.add_document(content_type='raw_text', file_ids=[upload_res.id])
print("添加文档结果: ",add_res)

# 知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 文件上传结果: request_id='255eec22-ec87-4564-bdeb-3e5623eaxxxx' id='ef12119b-d5be-492a-997c-77f8e84axxxx' name='test.txt'
# 添加文档结果: request_id='412e1630-b570-47c9-a042-caf3cd9dxxxx' knowledge_base_id='da51a988-cbe7-4b24-aa5b-768985e8xxxx' document_ids=['5e0eb279-7688-4100-95d1-241f3d19xxxx']
```

### 5、从知识库删除文档 `KnowledgeBase().delete_document()->KnowledgeBaseDeleteDocumentResponse`

#### 方法参数
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| document_id | string | 待删除的文档ID | '5e0eb279-7688-4100-95d1-241f3d19xxxx' |

#### 方法返回值

方法返回 `KnowledgeBaseDeleteDocumentResponse`, 该类的定义是

```python
class KnowledgeBaseDeleteDocumentResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
```

#### 方法示例
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

upload_res = my_knowledge.upload_file("./test.txt")
print("文件上传结果: ",upload_res)

add_res = my_knowledge.add_document(content_type='raw_text', file_ids=[upload_res.id])
print("添加文档结果: ",add_res)

delete_res = my_knowledge.delete_document(document_id=add_res.document_ids[0])
print("删除文档结果: ",delete_res)

# 知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 文件上传结果: request_id='255eec22-ec87-4564-bdeb-3e5623eaxxxx' id='ef12119b-d5be-492a-997c-77f8e84axxxx' name='test.txt'
# 添加文档结果: request_id='412e1630-b570-47c9-a042-caf3cd9dxxxx' knowledge_base_id='da51a988-cbe7-4b24-aa5b-768985e8xxxx' document_ids=['5e0eb279-7688-4100-95d1-241f3d19xxxx']
# 删除文档结果: request_id='ba0e8bc0-b799-45b5-bdac-0d4c50e2xxxx'
```

### 6、获取知识库的文档列表`KnowledgeBase().get_documents_list()->KnowledgeBaseGetDocumentsListResponse` 

#### 方法参数
| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| limit | int | 单次请求列表获得的文档数量,最大100  | 10 |
| after | str | 用于分页的游标。after 是一个文档的id，它定义了在列表中的位置。例如，如果你发出一个列表请求并收到 10个对象，以 app_id_123 结束，那么你后续的调用可以包含 after=app_id_123 以获取列表的下一页数据。默认为空  | '5e0eb279-7688-4100-95d1-241f3d19xxxx' |
| before | str | 用于分页的游标。与after相反，填写它将获取前一页数据,如果和after都传，两个参数都会起到分页效果，默认为空  | '5e0eb279-7688-4100-95d1-241f3d19xxxx' |

#### 方法返回值

方法返回类`KnowledgeBaseGetDocumentsListResponse`，定义为
```python
class KnowledgeBaseGetDocumentsListResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    data: list[Document] = Field([], description="文档信息列表")
```

衍生类`Document`以及`DocumentMeta`定义为：
```python
class Document(BaseModel):
    id: str = Field(..., description="文档ID")
    name: str = Field(..., description="文档名称")
    created_at: str = Field(..., description="文档创建时间")
    word_count: int = Field(..., description="文档字数")
    enabled: bool = Field(True, description="文档是否可用")
    meta: Optional[DocumentMeta] = Field(..., description="文档元信息，包括source、file_id")

class DocumentMeta(BaseModel):
    source: str = Field("", description="文档来源")
    file_id: str = Field("", description="文档对应的文件ID")
```


#### 方法示例
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

list_res = my_knowledge.get_documents_list()
print("文档列表: ", list_res)

# 知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 文档列表: request_id='f66c2193-6035-4022-811b-c4cd7743xxxx' data=[{'id': '8f388b10-5e6a-423f-8acc-dd5fdc2fxxxx', 'name': 'test.txt', 'created_at': 1719988868, 'word_count': 16886, 'enabled': True, 'meta': {'source': 'upload_file', 'file_id': '0ebb03fb-ea48-4c49-b494-cf0cec11xxxx'}}, {'id': '5e0eb279-7688-4100-95d1-241f3d19xxxx', 'name': 'test.txt', 'created_at': 1719987921, 'word_count': 16886, 'enabled': True, 'meta': {'source': 'upload_file', 'file_id': '059e2ae2-1e3c-43ea-8b42-5d988f93xxxx'}}]
```

### Java基本用法

#### 方法及各方法入参/出参

参考 `python KnowledgeBase`接口文档


#### 示例代码
```java
public class KnowledgebaseTest {
    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN","");
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
    }
    
    @Test
    public void testAddDocument() throws IOException, AppBuilderServerException {
        // 实例化Knowledgebase
        String knowledgeBaseId  = "";
        Knowledgebase knowledgebase = new Knowledgebase();

        // 获取知识库文档列表
        DocumentListRequest listRequest = new DocumentListRequest(); 
        listRequest.setKonwledgeBaseId(knowledgeBaseId);
        listRequest.setLimit(10);
        Document[] documents = knowledgebase.getDocumentList(listRequest);

        // 向知识库上传通用文档
        String fileId = knowledgebase.uploadFile("src/test/java/com/baidubce/appbuilder/files/test.pdf");
        System.out.println(fileId);
        
        // 向知识库添加文档
        DocumentAddRequest request = new DocumentAddRequest();
        request.setKnowledgeBaseId(knowledgeBaseId);
        request.setContentType("raw_text");
        request.setFileIds(new String[] { fileId });
        DocumentAddRequest.CustomProcessRule customProcessRule = new DocumentAddRequest.CustomProcessRule();
        customProcessRule.setSeparators(new String[] { "。" });
        customProcessRule.setTargetLength(300);
        customProcessRule.setOverlapRate(0.25);
        request.setCustomProcessRule(customProcessRule);
        String[] documentsRes = knowledgebase.addDocument(request);
        assertNotNull(documentsRes);

        // 从知识库删除文档
        DocumentDeleteRequest deleteRequest = new DocumentDeleteRequest();
        deleteRequest.setKonwledgeBaseId(knowledgeBaseId);
        deleteRequest.setDocumentId(documentsRes[0]);
        knowledgebase.deleteDocument(deleteRequest);
    }
}
```

### Go基本用法

#### 方法及各方法入参/出参

参考 `python KnowledgeBase`接口文档


#### 示例代码

```Go
package appbuilder

import (
	"fmt"
	"os"
	"testing"
)

func TestKnowledgeBase(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_LOGFILE", "")

    // 实例化KnowledgeBase
	knowledgeBaseID := ""
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}

    // 获取知识库中的文档列表
	documentsRes, err := client.GetDocumentList(GetDocumentListRequest{
		KnowledgeBaseID: knowledgeBaseID,
	})
	if err != nil {
		t.Fatalf("create document failed: %v", err)
	}
	fmt.Println(documentsRes)

    // 向知识库中上传通用文件
	fileID, err := client.UploadFile("./files/test.pdf")
	if err != nil {
		t.Fatalf("upload file failed: %v", err)
	}
	fmt.Println(fileID)

    // 向知识库中添加文档
	createDocumentRes, err := client.CreateDocument(CreateDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		ContentType:     ContentTypeRawText,
		FileIDS:         []string{fileID},
		CustomProcessRule: &CustomProcessRule{
			Separators:   []string{"。"},
			TargetLength: 300,
			OverlapRate:  0.25,
		},
	})
	if err != nil {
		t.Fatalf("create document failed: %v", err)
	}
	fmt.Println(createDocumentRes)

    // 从知识库中删除文档
	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      createDocumentRes.DocumentsIDS[0]})
	if err != nil {
		t.Fatalf("delete document failed: %v", err)
	}
}
```