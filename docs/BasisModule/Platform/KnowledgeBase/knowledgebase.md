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

### 1、新建知识库`KnowledgeBase().create_knowledge_base(name: str, description: str, type: str, esUrl: str, esUserName: str, esPassword: str) -> KnowledgeBaseDetailResponse`

#### 方法参数
| 参数名称    | 参数类型 | 是否必传 | 描述                                  | 示例值             |
| ----------- | -------- | -------- | ------------------------------------- | ------------------ |
| name        | string   | 是       | 希望创建的知识库名称                  | "我的知识库"       |
| description | string   | 否       | 知识库描述                            | "我的知识库"       |
| type        | string   | 是       | 知识库索引存储配置 (public、bes、vdb) | "public"           |
| esUrl       | string   | 否       | bes 访问地址，type填bes时填写         | "http://test/test" |
| esUserName  | string   | 否       | bes 用户名，type填bes时填写           | "username"         |
| esPassword  | string   | 否       | bes密码，type填bes时填写              | "password"         |

#### 方法返回值

`KnowledgeBaseDetailResponse` 类定义如下：

```python
class KnowledgeBaseDetailResponse(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")
```

衍生类`KnowledgeBaseConfig`定义如下：

```python
class KnowledgeBaseConfig(BaseModel):
    index: Optional[KnowledgeBaseConfigIndex] = Field(..., description="索引配置")
```

衍生类`KnowledgeBaseConfigIndex`定义如下：

```python
class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    esUrl: Optional[str] = Field(..., description="ES地址")
    username: Optional[str] = Field(None, description="ES用户名")
    password: Optional[str] = Field(None, description="ES密码")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge = appbuilder.KnowledgeBase()
resp = knowledge.create_knowledge_base(
        name="my_knowledge",
        description="my_knowledge",
        type="public",
    )
print("新建的知识库ID: ", resp.id)
print("新建的知识库名称: ", resp.name)

# 新建的知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 新建的知识库名称:  my_knowledge
```

### 2、实例化已创建的知识库 `KnowledgeBase(knowledge_id: str)`

#### 方法参数

| 参数名称     | 参数类型 | 是否必传 | 描述         | 示例值           |
| ------------ | -------- | -------- | ------------ | ---------------- |
| knowledge_id | string   | 是       | 线上知识库ID | "正确的知识库ID" |

#### 方法返回值
| 参数名称      | 参数类型            | 必然存在 | 描述             | 示例值 |
| ------------- | ------------------- | -------- | ---------------- | ------ |
| KnowledgeBase | class KnowledgeBase | 是       | 实例化的知识库类 | -      |

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

### 3、获取知识库详情`get_knowledge_base_detail(knowledge_base_id: Optional[str] = None) -> KnowledgeBaseDetailResponse`

#### 方法参数

| 参数名称     | 参数类型 | 是否必传 | 描述         | 示例值           |
| ------------ | -------- | -------- | ------------ | ---------------- |
| knowledge_id | string   | 是       | 线上知识库ID | "正确的知识库ID" |

#### 方法返回值

`KnowledgeBaseDetailResponse` 类定义如下：

```python
class KnowledgeBaseDetailResponse(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")
```

衍生类`KnowledgeBaseConfig`定义如下：

```python
class KnowledgeBaseConfig(BaseModel):
    index: Optional[KnowledgeBaseConfigIndex] = Field(..., description="索引配置")
```

衍生类`KnowledgeBaseConfigIndex`定义如下：

```python
class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    esUrl: Optional[str] = Field(..., description="ES地址")
    username: Optional[str] = Field(None, description="ES用户名")
    password: Optional[str] = Field(None, description="ES密码")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge = appbuilder.KnowledgeBase()
resp = knowledge.get_knowledge_base_detail("da51a988-cbe7-4b24-aa5b-768985e8xxxx")
print("新建的知识库ID: ", resp.id)
print("新建的知识库名称: ", resp.name)

# 新建的知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 新建的知识库名称:  my_knowledge
```

### 4、 获取知识库列表`get_knowledge_base_list(knowledge_base_id: Optional[str] = None, maxKeys: int = 10, keyword: Optional[str] = None) -> KnowledgeBaseGetListResponse`

#### 方法参数

| 参数名称          | 参数类型 | 是否必传 | 描述                        | 示例值           |
| ----------------- | -------- | -------- | --------------------------- | ---------------- |
| knowledge_base_id | string   | 是       | 起始位置，知识库id          | "正确的知识库ID" |
| maxKeys           | int      | 否       | 数据大小，默认10，最大值100 | 10               |
| keyword           | string   | 否       | 搜索关键字                  | "测试"           |

#### 方法返回值

`KnowledgeBaseGetListResponse` 类定义如下：

```python
class KnowledgeBaseGetListResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    data: list[KnowledgeBaseDetailResponse] = Field([], description="知识库详情列表")
    marker: str = Field(..., description="起始位置")
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(10, description="返回文档数量大小，默认10，最大值100")
    isTruncated: bool = Field(..., description="是否有更多结果")
```

衍生类`KnowledgeBaseDetailResponse` 定义如下：

```python
class KnowledgeBaseDetailResponse(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")
```

衍生类`KnowledgeBaseConfig`定义如下：

```python
class KnowledgeBaseConfig(BaseModel):
    index: Optional[KnowledgeBaseConfigIndex] = Field(..., description="索引配置")
```

衍生类`KnowledgeBaseConfigIndex`定义如下：

```python
class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    esUrl: Optional[str] = Field(..., description="ES地址")
    username: Optional[str] = Field(None, description="ES用户名")
    password: Optional[str] = Field(None, description="ES密码")
```

#### 方法示例：

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge = appbuilder.KnowledgeBase()
resp = knowledge.get_knowledge_base_list("da51a988-cbe7-4b24-aa5b-768985e8xxxx",10)
print("获取到的知识库列表: ", resp)
```

### 5、修改知识库`modify_knowledge_base(knowledge_base_id: Optional[str] = None, name: Optional[str] = None, description: Optional[str] = None)`

#### 方法参数

| 参数名称          | 参数类型 | 是否必传 | 描述               | 示例值           |
| ----------------- | -------- | -------- | ------------------ | ---------------- |
| knowledge_base_id | string   | 是       | 起始位置，知识库id | "正确的知识库ID" |
| name              | string   | 否       | 修改后的知识库名称 | "new_name"       |
| description       | string   | 否       | 修改后的知识库描述 | "测试"           |

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge = appbuilder.KnowledgeBase()
knowledge.modify_knowledge_base("da51a988-cbe7-4b24-aa5b-768985e8xxxx", name="new_name", description="测试")
```

### 6、 删除知识库`delete_knowledge_base(knowledge_base_id: Optional[str] = None)`

#### 方法参数

| 参数名称          | 参数类型 | 是否必传 | 描述       | 示例值           |
| ----------------- | -------- | -------- | ---------- | ---------------- |
| knowledge_base_id | string   | 是       | 知识库的id | "正确的知识库ID" |

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge = appbuilder.KnowledgeBase()
knowledge.delete_knowledge_base("da51a988-cbe7-4b24-aa5b-768985e8xxxx")
```

### 7、 导入知识库`create_documents(id: Optional[str] = None, contentFormat: str = "", source: DocumentSource = None, processOption: DocumentProcessOption = None)`

#### 方法参数

| 参数名称      | 参数类型              | 是否必传                               | 描述                                                         | 示例值           |
| ------------- | --------------------- | -------------------------------------- | ------------------------------------------------------------ | ---------------- |
| id            | string                | 是                                     | 知识库id                                                     | "正确的知识库ID" |
| contentFormat | string                | 是                                     | 文档格式：rawText (允许配置后续分割策略), qa(不支持配置后续分割策略) | "rawText"        |
| source        | DocumentSource        | 是                                     | 数据来源                                                     |                  |
| processOption | DocumentProcessOption | 当contentFormat参数配置为rawText时必传 | 文档处理策略                                                 |                  |

`DocumentSource`类定义如下：

```python
class DocumentSource(BaseModel):
    type: str = Field(..., description="数据来源类型", enum=["bos", "web"])
    urls: list[str] = Field(None, description="文档URL")
    urlDepth: int = Field(None, description="url下钻深度，1时不下钻")
```

`DocumentProcessOption`类及衍生类定义如下：

```python
class DocumentProcessOption(BaseModel):
    template: str = Field(
        ...,
        description="模板类型，ppt：模版配置—ppt幻灯片, resume：模版配置—简历文档, paper：模版配置—论文文档, custom：自定义配置—自定义切片, default：自定义配置—默认切分",
        enum=["ppt", "paper", "qaPair", "resume", " custom", "default"],
    )
    parser: Optional[DocumentChoices] = Field(None, description="解析方法(文字提取默认启动，参数不体现，layoutAnalysis版面分析，ocr按需增加)")
    knowledgeAugmentation: Optional[DocumentChoices] = Field(
        None, description="知识增强，faq、spokenQuery、spo、shortSummary按需增加。问题生成:faq、spokenQuery，段落摘要:shortSummary，三元组知识抽取:spo"
    )
    chunker: Optional[DocumentChunker] = Field(None, description="分段器类型")

class DocumentChoices(BaseModel):
    choices: list[str] = Field(..., description="选择项")

class DocumentChunker(BaseModel):
    choices: list[str] = Field(..., description="使用哪些chunker方法 (separator | pattern | onePage)，separator：自定义切片—标识符，pattern：自定义切片—标识符中选择正则表达式，onePage：整文件切片")
    prependInfo: list[str] = Field(
        ...,
        description="chunker关联元数据，可选值为title (增加标题), filename(增加文件名)",
    )
    separator: Optional[DocumentSeparator] = Field(..., description="分隔符配置")
    pattern: Optional[DocumentPattern] = Field(None, description="正则表达式")

class DocumentSeparator(BaseModel):
    separators: list[str] = Field(..., description="分隔符列表，可以使用分页符")
    targetLength: int = Field(..., description="分段最大长度")
    overlapRate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25")

class DocumentPattern(BaseModel):
    markPosition: str = Field(
        ..., description="命中内容放置策略, head：前序切片, tail：后序切片, drop：匹配后丢弃", enum=["head", "tail", "drop"]
    )
    regex: str = Field(..., description="正则表达式")
    targetLength: int = Field(..., description="分段最大长度")
    overlapRate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge_base_id = "your_knowledge_base_id"
knowledge = appbuilder.KnowledgeBase()
knowledge.create_documents(
	id=knowledge_base_id,
	contentFormat="rawText",
	source=appbuilder.DocumentSource(
		type="web",
		urls=["https://baijiahao.baidu.com/s?id=1802527379394162441"],
    urlDepth=1,
  ),
	processOption=appbuilder.DocumentProcessOption(
		template="custom",
		parser=appbuilder.DocumentChoices(
			choices=["layoutAnalysis", "ocr"]
		),
		chunker=appbuilder.DocumentChunker(
			choices=["separator"],
			separator=appbuilder.DocumentSeparator(
				separators=["。"],
				targetLength=300,
				overlapRate=0.25,
      ),
			prependInfo=["title", "filename"],
		),
		knowledgeAugmentation=appbuilder.DocumentChoices(choices=["faq"]),
	),
)
```

### 8、 上传文档到知识库`upload_documents(file_path: str, content_format: str = "rawText", id: Optional[str] = None, processOption: DocumentProcessOption = None)`

#### 方法参数

| 参数名称       | 参数类型              | 是否必传 | 描述                                                         | 示例值           |
| -------------- | --------------------- | -------- | ------------------------------------------------------------ | ---------------- |
| file_path      | string                | 是       | 文件路径                                                     | "正确的文件路径" |
| content_format | string                | 否       | 文档格式：rawText (允许配置后续分割策略), qa(不支持配置后续分割策略) | "rawText"        |
| id             | string                | 是       | 知识库ID                                                     | "正确的知识库ID" |
| processOption  | DocumentProcessOption | 是       | 文档处理策略                                                 |                  |

`DocumentProcessOption`类及衍生类定义如下：

```python
class DocumentProcessOption(BaseModel):
    template: str = Field(
        ...,
        description="模板类型，ppt: 模版配置—ppt幻灯片, resume：模版配置—简历文档, paper：模版配置—论文文档, custom：自定义配置—自定义切片, default：自定义配置—默认切分",
        enum=["ppt", "paper", "qaPair", "resume", " custom", "default"],
    )
    parser: Optional[DocumentChoices] = Field(None, description="解析器类型")
    knowledgeAugmentation: Optional[DocumentChoices] = Field(
        None, description="知识增强，faq、spokenQuery、spo、shortSummary按需增加。问题生成:faq、spokenQuery，段落摘要:shortSummary，三元组知识抽取:spo"
    )
    chunker: Optional[DocumentChunker] = Field(None, description="分段器类型")

class DocumentChoices(BaseModel):
    choices: list[str] = Field(..., description="选择项")

class DocumentChunker(BaseModel):
    choices: list[str] = Field(..., description="使用哪些chunker方法 (separator | pattern | onePage), separator：自定义切片—标识符，pattern：自定义切片—标识符中选择正则表达式，onePage：整文件切片")
    prependInfo: list[str] = Field(
        ...,
        description="chunker关联元数据，可选值为title (增加标题), filename(增加文件名)",
    )
    separator: Optional[DocumentSeparator] = Field(..., description="分段符号")
    pattern: Optional[DocumentPattern] = Field(None, description="正则表达式")

class DocumentSeparator(BaseModel):
    separators: list[str] = Field(..., description="分段符号")
    targetLength: int = Field(..., description="分段最大长度")
    overlapRate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25")

class DocumentPattern(BaseModel):
    markPosition: str = Field(
        ..., description="命中内容放置策略, head：前序切片, tail：后序切片, drop：匹配后丢弃", enum=["head", "tail", "drop"]
    )
    regex: str = Field(..., description="正则表达式")
    targetLength: int = Field(..., description="分段最大长度")
    overlapRate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25")

```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge_base_id = "your_knowledge_base_id"
knowledge = appbuilder.KnowledgeBase()
knowledge.upload_documents(
	id=knowledge_base_id,
	content_format="rawText",
	file_path="./appbuilder/tests/data/qa_appbuilder_client_demo.pdf",
	processOption=appbuilder.DocumentProcessOption(
		template="custom",
		parser=appbuilder.DocumentChoices(
			choices=["layoutAnalysis", "ocr"]
		),
		chunker=appbuilder.DocumentChunker(
			choices=["separator"],
			separator=appbuilder.DocumentSeparator(
				separators=["。"],
				targetLength=300,
				overlapRate=0.25,
      ),
			prependInfo=["title", "filename"],
		),
		knowledgeAugmentation=appbuilder.DocumentChoices(choices=["faq"]),
	),
)
```

### 9、上传通用文档 `KnowledgeBase().upload_file(file_path: str)->KnowledgeBaseUploadFileResponse`

#### 方法参数
| 参数名称  | 参数类型 | 是否必传 | 描述           | 示例值         |
| --------- | -------- | -------- | -------------- | -------------- |
| file_path | string   | 是       | 本地的文件路径 | "/home/my_doc" |

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
### 10、向知识库添加文档 `KnowledgeBase().add_document()->KnowledgeBaseAddDocumentResponse`

#### 方法参数
| 参数名称            | 参数类型          | 是否必传 | 描述                                                         | 示例值                                                       |
| ------------------- | ----------------- | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| content_type        | enum[str]         | 是       | 知识库文档类型，有raw_text和qa两种可选，分别对应文本文档 和 结构化的excel问答对 | "raw_text"                                                   |
| file_ids            | list[str]         | 是       | 文件ID列表，文件ID通过`upload_file`接口获得                  | ['ef12119b-d5be-492a-997c-77f8e84axxxx']                     |
| is_enhanced         | bool              | 否       | 文档是否开启基于大模型的知识增强                             | False                                                        |
| custom_process_rule | CustomProcessRule | 否       | 文档的自定义切分逻辑                                         | `appbuilder.CustomProcessRule(separators=["?"], target_length=400,overlap_rate=0.2)` |


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

### 11、从知识库删除文档 `KnowledgeBase().delete_document()->KnowledgeBaseDeleteDocumentResponse`

#### 方法参数
| 参数名称    | 参数类型 | 是否必传 | 描述           | 示例值                                 |
| ----------- | -------- | -------- | -------------- | -------------------------------------- |
| document_id | string   | 是       | 待删除的文档ID | '5e0eb279-7688-4100-95d1-241f3d19xxxx' |

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

### 12、获取知识库的文档列表`KnowledgeBase().get_documents_list()->KnowledgeBaseGetDocumentsListResponse` 

#### 方法参数
| 参数名称 | 参数类型 | 是否必传 | 描述                                                         | 示例值                                 |
| -------- | -------- | -------- | ------------------------------------------------------------ | -------------------------------------- |
| limit    | int      | 否       | 单次请求列表获得的文档数量,最大100                           | 10                                     |
| after    | str      | 否       | 用于分页的游标。after 是一个文档的id，它定义了在列表中的位置。例如，如果你发出一个列表请求并收到 10个对象，以 app_id_123 结束，那么你后续的调用可以包含 after=app_id_123 以获取列表的下一页数据。默认为空 | '5e0eb279-7688-4100-95d1-241f3d19xxxx' |
| before   | str      | 否       | 用于分页的游标。与after相反，填写它将获取前一页数据,如果和after都传，两个参数都会起到分页效果，默认为空 | '5e0eb279-7688-4100-95d1-241f3d19xxxx' |

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

list_res = my_knowledge.get_documents_list(my_knowledge_base_id)
print("文档列表: ", list_res)

# 知识库ID:  da51a988-cbe7-4b24-aa5b-768985e8xxxx
# 文档列表: request_id='f66c2193-6035-4022-811b-c4cd7743xxxx' data=[{'id': '8f388b10-5e6a-423f-8acc-dd5fdc2fxxxx', 'name': 'test.txt', 'created_at': 1719988868, 'word_count': 16886, 'enabled': True, 'meta': {'source': 'upload_file', 'file_id': '0ebb03fb-ea48-4c49-b494-cf0cec11xxxx'}}, {'id': '5e0eb279-7688-4100-95d1-241f3d19xxxx', 'name': 'test.txt', 'created_at': 1719987921, 'word_count': 16886, 'enabled': True, 'meta': {'source': 'upload_file', 'file_id': '059e2ae2-1e3c-43ea-8b42-5d988f93xxxx'}}]
```

### 13、获取知识库全部文档`KnowledgeBase().get_all_documents()->list`

#### 方法参数
| 参数名称          | 参数类型 | 是否必传 | 描述         | 示例值           |
| ----------------- | -------- | -------- | ------------ | ---------------- |
| knowledge_base_id | string   | 是       | 线上知识库ID | "正确的知识库ID" |

#### 方法返回值

list 数据类型`list[Document]`

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

doc_list = knowledge.get_all_documents(my_knowledge_base_id)
for message in doc_list:
    print(message)
```

### 14. 创建切片`create_chunk(documentId: str, content: str) -> CreateChunkResponse`

#### 方法参数

| 参数名称   | 参数类型 | 是否必传 | 描述     | 示例值         |
| ---------- | -------- | -------- | -------- | -------------- |
| documentId | string   | 是       | 文档ID   | "正确的文档ID" |
| content    | string   | 是       | 切片内容 | "内容"         |

#### 方法返回值

`CreateChunkResponse`类定义如下：

```python
class CreateChunkResponse(BaseModel):
    id: str = Field(..., description="切片ID")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)
resp = my_knowledge.create_chunk("your_document_id", "content")
print("切片ID: ", resp.id)
chunk_id = resp.id
```

### 15. 修改切片信息`modify_chunk(chunkId: str, content: str, enable: bool)`

#### 方法参数

| 参数名称   | 参数类型 | 是否必传     | 描述         | 示例值         |
| ---------- | -------- | ------------ | -------------- | -------------- |
| chunkId | string   | 是      | 文档ID       | "正确的切片ID" |
| content    | string   | 是    | 切片内容     | "内容"         |
| enable     | bool     | 是 | 是否用该切片 | True          |

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)
my_knowledge.modify_chunk("your_chunk_id", "content", True)
```

### 16. 删除切片`delete_chunk(chunkId: str)`

#### 方法参数

| 参数名称 | 参数类型 | 是否必传 | 描述   | 示例值         |
| -------- | -------- | -------- | ------ | -------------- |
| chunkId  | string   | 是       | 文档ID | "正确的切片ID" |

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)
my_knowledge.delete_chunk("your_chunk_id")
```

### 17. 获取切片信息`describe_chunk(chunkId: str)`

#### 方法参数

| 参数名称 | 参数类型 | 是否必传 | 描述   | 示例值         |
| -------- | -------- | -------- | ------ | -------------- |
| chunkId  | string   | 是       | 文档ID | "正确的切片ID" |

#### 方法返回值

`DescribeChunkResponse`类定义如下:

```python
class DescribeChunkResponse(BaseModel):
    id: str = Field(..., description="切片ID")
    type: str = Field(..., description="切片类型")
    knowledgeBaseId: str = Field(..., description="知识库ID")
    documentId: str = Field(..., description="文档ID")
    content: str = Field(..., description="文档内容")
    enabled: bool = Field(..., description="是否启用")
    wordCount: int = Field(..., description="切片内字符数量")
    tokenCount: int = Field(..., description="切片内token数量")
    status: str = Field(..., description="切片状态")
    statusMessage: str = Field(..., description="切片状态信息")
    imageUrls: list[str] = Field(..., description="图片地址")
    createTime: int = Field(..., description="创建时间")
    updateTime: int = Field(None, description="更新时间")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)
resp = my_knowledge.describe_chunk("your_chunk_id")
print("切片详情：")
print(resp)
```

### 18. 获取切片列表`describe_chunks(documentId: str, marker: str = None, maxKeys: int = None, type: str = None) -> DescribeChunksResponse`

#### 方法参数

| 参数名称   | 参数类型 | 是否必传 | 描述                                                         | 示例值         |
| ---------- | -------- | -------- | ------------------------------------------------------------ | -------------- |
| documentId | string   | 是       | 文档ID                                                       | "正确的文档ID" |
| marker     | string   | 否       | 起始位置，切片ID                                             | "正确的切片ID" |
| maxKeys    | string   | 否       | 返回文档数量大小，默认10，最大值100                          | 10             |
| type       | string   | 否       | 根据类型获取切片列表(RAW、NEW、COPY)，RAW：原文切片，NEW：新增切片，COPY：复制切片 | "RAW"          |

#### 方法返回值

`DescribeChunksResponse` 类定义如下：

```python
class DescribeChunksResponse(BaseModel):
    data: list[DescribeChunkResponse] = Field(..., description="切片列表")
    marker: str = Field(..., description="起始位置")
    isTruncated: bool = Field(
        ..., description="true表示后面还有数据，false表示已经是最后一页"
    )
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(..., description="本次查询包含的最大结果集数量")
```

衍生类`DescribeChunkResponse`定义如下：

```python
class DescribeChunkResponse(BaseModel):
    id: str = Field(..., description="切片ID")
    type: str = Field(..., description="切片类型")
    knowledgeBaseId: str = Field(..., description="知识库ID")
    documentId: str = Field(..., description="文档ID")
    content: str = Field(..., description="文档内容")
    enabled: bool = Field(..., description="是否启用")
    wordCount: int = Field(..., description="切片内字符数量")
    tokenCount: int = Field(..., description="切片内token数量")
    status: str = Field(..., description="切片状态")
    statusMessage: str = Field(..., description="切片状态信息")
    imageUrls: list[str] = Field(..., description="图片地址")
    createTime: int = Field(..., description="创建时间")
    updateTime: int = Field(None, description="更新时间")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)
resp = my_knowledge.describe_chunks("your_document_id")
print("切片列表：")
print(resp)
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
  
    @Test
    public void testCreateKnowledgebase() throws IOException, AppBuilderServerException {
        Knowledgebase knowledgebase = new Knowledgebase();
        KnowledgeBaseDetail request = new KnowledgeBaseDetail();
        request.setName("test_knowledgebase");
        request.setDescription("test_knowledgebase");

        // 创建知识库
        KnowledgeBaseConfig.Index index = new KnowledgeBaseConfig.Index("public",
                "http://localhost:9200", "elastic", "changeme");
        KnowledgeBaseConfig config = new KnowledgeBaseConfig(index);
        request.setConfig(config);
        KnowledgeBaseDetail response = knowledgebase.createKnowledgeBase(request);
        String knowledgeBaseId = response.getId();
        System.out.println(knowledgeBaseId);
        assertNotNull(response.getId());

        // 获取知识库详情
        KnowledgeBaseDetail detail = knowledgebase.getKnowledgeBaseDetail(knowledgeBaseId);
        System.out.println(detail.getId());
        assertNotNull(detail.getId());

        // 获取知识库列表
        KnowledgeBaseListRequest listRequest =
                new KnowledgeBaseListRequest(knowledgeBaseId, 10, null);
        KnowledgeBaseListResponse knowledgeBases = knowledgebase.getKnowledgeBaseList(listRequest);
        System.out.println(knowledgeBases.getMarker());
        assertNotNull(knowledgeBases.getMarker());

        // 更新知识库
        KnowledgeBaseModifyRequest modifyRequest = new KnowledgeBaseModifyRequest();
        modifyRequest.setKnowledgeBaseId(knowledgeBaseId);
        modifyRequest.setName("test_knowledgebase2");
        modifyRequest.setDescription(knowledgeBaseId);
        knowledgebase.modifyKnowledgeBase(modifyRequest);

        // 导入知识库
        DocumentsCreateRequest.Source source = new DocumentsCreateRequest.Source("web",
                new String[] {"https://baijiahao.baidu.com/s?id=1802527379394162441"}, 1);
        DocumentsCreateRequest.ProcessOption.Parser parser =
                new DocumentsCreateRequest.ProcessOption.Parser(
                        new String[] {"layoutAnalysis", "ocr"});
        DocumentsCreateRequest.ProcessOption.Chunker.Separator separator =
                new DocumentsCreateRequest.ProcessOption.Chunker.Separator(new String[] {"。"}, 300,
                        0.25);
        DocumentsCreateRequest.ProcessOption.Chunker chunker =
                new DocumentsCreateRequest.ProcessOption.Chunker(new String[] {"separator"},
                        separator, null, new String[] {"title", "filename"});
        DocumentsCreateRequest.ProcessOption.KnowledgeAugmentation knowledgeAugmentation =
                new DocumentsCreateRequest.ProcessOption.KnowledgeAugmentation(
                        new String[] {"faq"});
        DocumentsCreateRequest.ProcessOption processOption =
                new DocumentsCreateRequest.ProcessOption("custom", parser, chunker,
                        knowledgeAugmentation);
        DocumentsCreateRequest documentsCreateRequest =
                new DocumentsCreateRequest(knowledgeBaseId, "rawText", source, processOption);
        knowledgebase.createDocuments(documentsCreateRequest);

        // 上传文档
        String filePath = "src/test/java/com/baidubce/appbuilder/files/test.pdf";
        DocumentsCreateRequest.Source source2 =
                new DocumentsCreateRequest.Source("file", null, null);
        DocumentsCreateRequest documentsCreateRequest2 =
                new DocumentsCreateRequest(knowledgeBaseId, "rawText", source2, processOption);
        knowledgebase.uploadDocuments(filePath, documentsCreateRequest2);

        // 删除知识库
        knowledgebase.deleteKnowledgeBase(knowledgeBaseId);
    }
  
    @Test
    public void testCreateChunk() throws IOException, AppBuilderServerException {
        String documentId = "";
        Knowledgebase knowledgebase = new Knowledgebase();
        // 创建切片
        String chunkId = knowledgebase.createChunk(documentId, "test");
        // 修改切片
        knowledgebase.modifyChunk(chunkId, "new test", true);
        // 获取切片详情
        knowledgebase.describeChunk(chunkId);
        // 获取切片列表
        knowledgebase.describeChunks(documentId, chunkId, 10, null);
        // 删除切片
        knowledgebase.deleteChunk(chunkId);
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

func TestCreateKnowledgeBase(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}

	// 创建知识库
	createKnowledgeBaseRes, err := client.CreateKnowledgeBase(KnowledgeBaseDetail{
		Name:        "test-go",
		Description: "test-go",
		Config: &KnowlegeBaseConfig{
			Index: KnowledgeBaseConfigIndex{
				Type:     "public",
				EsUrl:    "http://localhost:9200",
				Password: "elastic",
				Username: "elastic",
			},
		},
	})
	if err != nil {
		t.Fatalf("create knowledge base failed: %v", err)
	}
	knowledgeBaseID := createKnowledgeBaseRes.ID
	fmt.Println(knowledgeBaseID)

	// 获取知识库详情
	getKnowledgeBaseRes, err := client.GetKnowledgeBaseDetail(knowledgeBaseID)
	if err != nil {
		t.Fatalf("get knowledge base failed: %v", err)
	}
	fmt.Println(getKnowledgeBaseRes)

	// 获取知识库列表
	knowledgeBaseListRes, err := client.GetKnowledgeBaseList(
		GetKnowledgeBaseListRequest{
			Marker: knowledgeBaseID,
		},
	)
	if err != nil {
		t.Fatalf("get knowledge base list failed: %v", err)
	}
	fmt.Println(knowledgeBaseListRes)

	// 导入知识库
	err = client.CreateDocuments(CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type:     "web",
			Urls:     []string{"https://baijiahao.baidu.com/s?id=1802527379394162441"},
			UrlDepth: 1,
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err != nil {
		t.Fatalf("create documents failed: %v", err)
	}

	// 上传知识库文档
	err = client.UploadDocuments("./files/test.pdf", CreateDocumentsRequest{
		ID:            knowledgeBaseID,
		ContentFormat: "rawText",
		Source: DocumentsSource{
			Type: "file",
		},
		ProcessOption: &DocumentsProcessOption{
			Template: "custom",
			Parser: &DocumentsProcessOptionParser{
				Choices: []string{"layoutAnalysis", "ocr"},
			},
			Chunker: &DocumentsProcessOptionChunker{
				Choices: []string{"separator"},
				Separator: &DocumentsProcessOptionChunkerSeparator{
					Separators:   []string{"。"},
					TargetLength: 300,
					OverlapRate:  0.25,
				},
				PrependInfo: []string{"title", "filename"},
			},
			KnowledgeAugmentation: &DocumentsProcessOptionKnowledgeAugmentation{
				Choices: []string{"faq"},
			},
		},
	})
	if err != nil {
		t.Fatalf("upload documents failed: %v", err)
	}

	// 修改知识库
	name := "test-go"
	description := "22"
	err = client.ModifyKnowledgeBase(ModifyKnowlegeBaseRequest{
		ID:          knowledgeBaseID,
		Name:        &name,
		Description: &description,
	})
	if err != nil {
		t.Fatalf("modify knowledge base failed: %v", err)
	}

	// 删除知识库
	err = client.DeleteKnowledgeBase(knowledgeBaseID)
	if err != nil {
		t.Fatalf("delete knowledge base failed: %v", err)
	}
}

func TestChunk(t *testing.T) {
	os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
	os.Setenv("APPBUILDER_TOKEN", "")
	documentID := ""

	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBase(config)
	if err != nil {
		t.Fatalf("new Knowledge base instance failed")
	}
	// 创建切片
	chunkID, err := client.CreateChunk(CreateChunkRequest{
		DocumentID: documentID,
		Content:    "test",
	})
	if err != nil {
		t.Fatalf("create chunk failed: %v", err)
	}
	fmt.Println(chunkID)

	// 修改切片
	err = client.ModifyChunk(ModifyChunkRequest{
		ChunkID: chunkID,
		Content: "new test",
		Enable:  true,
	})
	if err != nil {
		t.Fatalf("modify chunk failed: %v", err)
	}

	// 获取切片详情
	describeChunkRes, err := client.DescribeChunk(chunkID)
	if err != nil {
		t.Fatalf("describe chunk failed: %v", err)
	}
	fmt.Println(describeChunkRes)

	// 获取切片列表
	describeChunksRes, err := client.DescribeChunks(DescribeChunksRequest{
		DocumnetID: documentID,
		Marker:     chunkID,
		MaxKeys:    10,
	})
	if err != nil {
		t.Fatalf("describe chunks failed: %v", err)
	}
	fmt.Println(describeChunksRes)

	// 删除切片
	err = client.DeleteChunk(chunkID)
	if err != nil {
		t.Fatalf("delete chunk failed: %v", err)
	}
}
```