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

### 1、新建知识库`KnowledgeBase().create_knowledge_base(name: str, description: str, type: str, clusterId: str, esUserName: str, esPassword: str, location: str) -> KnowledgeBaseDetailResponse`

#### 方法参数
| 参数名称    | 参数类型 | 是否必传 | 描述                                  | 示例值             |
| ----------- | -------- | -------- | ------------------------------------- | ------------------ |
| name        | string   | 是       | 希望创建的知识库名称                  | "我的知识库"       |
| description | string   | 否       | 知识库描述                            | "我的知识库"       |
| type        | string   | 是       | 知识库索引存储配置 (public、bes、vdb) | "public"           |
| clusterId   | string   | type=bes 和 vdb 时填写       | 集群/实例 ID<br>请在bes、vdb控制台中查看。                       | "clusterId" |
| esUserName  | string   | type=bes 和 vdb 时填写       | 用户名/账号<br>请在bes、vdb控制台中查看           | "username"         |
| esPassword  | string   | type=bes 和 vdb 时填写       | 密码/API密钥<br>请在bes、vdb控制台中查看              | "password"         |
|location|string|type=bes 和 vdb 时填写|托管资源的区域，type填vdb时填写<br>可选值：<br>- bj：北京<br>- bd：保定<br>- sz：苏州<br>- gz：广州|"bj"|
|pathPrefix|string|否|创建知识库的指定目录，最大层级为5，默认为根目录下|"/全部群组/##/##"|

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
    catalogue: Optional[KnowledgeBaseConfigCatalogue] = Field(None, description="知识库目录配置")
```

衍生类`KnowledgeBaseConfigIndex`定义如下：

```python
class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    clusterId: Optional[str] = Field(None, description="集群/实例 ID")
    username: Optional[str] = Field(None, description="bes用户名")
    password: Optional[str] = Field(None, description="bes密码")
    location: Optional[str] = Field(None, description="托管资源的区域", enum=["bj", "bd", "sz", "gz"])
```

衍生类`KnowledgeBaseConfigCatalogue`

```python
class KnowledgeBaseConfigCatalogue(BaseModel):
    pathPrefix: Optional[str] = Field(None, description="知识库所属目录绝对路径")
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
    catalogue: Optional[KnowledgeBaseConfigCatalogue] = Field(None, description="知识库目录配置")
```

衍生类`KnowledgeBaseConfigIndex`定义如下：

```python
class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    esUrl: Optional[str] = Field(..., description="ES地址")
    username: Optional[str] = Field(None, description="ES用户名")
    password: Optional[str] = Field(None, description="ES密码")
```

衍生类`KnowledgeBaseConfigCatalogue`

```python
class KnowledgeBaseConfigCatalogue(BaseModel):
    pathPrefix: Optional[str] = Field(None, description="知识库所属目录绝对路径")
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
| knowledge_base_id | string   | 否       | 起始位置，知识库id          | "正确的知识库ID" |
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
    catalogue: Optional[KnowledgeBaseConfigCatalogue] = Field(None, description="知识库目录配置")
```

衍生类`KnowledgeBaseConfigIndex`定义如下：

```python
class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    esUrl: Optional[str] = Field(..., description="ES地址")
    username: Optional[str] = Field(None, description="ES用户名")
    password: Optional[str] = Field(None, description="ES密码")
```

衍生类`KnowledgeBaseConfigCatalogue`

```python
class KnowledgeBaseConfigCatalogue(BaseModel):
    pathPrefix: Optional[str] = Field(None, description="知识库所属目录绝对路径")
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

| 参数名称          | 参数类型 | 是否必传 | 描述                                          | 示例值           |
| ----------------- | -------- | -------- | --------------------------------------------- | ---------------- |
| knowledge_base_id | string   | 是       | 起始位置，知识库id                            | "正确的知识库ID" |
| name              | string   | 否       | 修改后的知识库名称                            | "new_name"       |
| description       | string   | 否       | 修改后的知识库描述                            | "测试"           |
| pathPrefix        | string   | 否       | 知识库的指定目录，最大层级为5，默认为根目录下 |                  |

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
| contentFormat | string                | 是                                     | 文档格式：rawText (允许配置后续分割策略)              | "rawText"        |
| source        | DocumentSource        | 是                                     | 数据来源                                                     |                  |
| processOption | DocumentProcessOption | 当contentFormat参数配置为rawText时必传 | 文档处理策略                                                 |                  |

`DocumentSource`类定义如下：

```python
class DocumentSourceUrlConfig(BaseModel):
    frequency: int = Field(
        ...,
        description="更新频率，目前支持的更新频率为-1(不自动更新),1（每天）,3（每3天）,7（每7天）,30（每30天）。",
    )

class DocumentSource(BaseModel):
    type: str = Field(..., description="数据来源类型", enum=["bos", "web"])
    urls: list[str] = Field(None, description="文档URL")
    urlDepth: int = Field(None, description="url下钻深度，1时不下钻")
    urlConfigs: Optional[list[DocumentSourceUrlConfig]] = Field(None, description="该字段的长度需要和source、urls字段长度保持一致。")
```

`DocumentProcessOption`类及衍生类定义如下：

```python
class DocumentProcessOption(BaseModel):
    template: str = Field(
        ...,
        description="模板类型，ppt：模版配置—ppt幻灯片, resume：模版配置—简历文档, paper：模版配置—论文文档, custom：自定义配置—自定义切片, default：自定义配置—默认切分",
        enum=["ppt", "paper", "qaPair", "resume", " custom", "default"],
    )
    parser: Optional[DocumentChoices] = Field(None, description="解析方法(文字提取默认启动，参数不体现，layoutAnalysis版面分析，ocr光学字符识别，pageImageAnalysis文档图片解析，chartAnalysis图表解析，tableAnalysis表格深度解析，按需增加)")
    knowledgeAugmentation: Optional[DocumentChoices] = Field(
        None, description="知识增强，faq、spokenQuery、spo、shortSummary按需增加。问题生成:faq、spokenQuery，段落摘要:shortSummary，三元组知识抽取:spo"
    )
    chunker: Optional[DocumentChunker] = Field(None, description="分段器类型")

class DocumentChoices(BaseModel):
    choices: list[str] = Field(..., description="选择项")

class DocumentChunker(BaseModel):
    choices: list[str] = Field(..., description="使用哪些chunker方法 (separator | pattern | onePage)，separator：自定义切片—标识符，pattern：自定义切片—标识符中选择正则表达式，onePage：整文件切片")
    prependInfo: list[str] = Field(
        None,
        description="chunker关联元数据，可选值为title (增加标题), filename(增加文件名)",
    )
    separator: Optional[DocumentSeparator] = Field(None, description="分隔符配置")
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
    urlConfigs=[appbuilder.DocumentSourceUrlConfig(frequency=1)]
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
| content_format | string                | 否       | 文档格式：rawText (允许配置后续分割策略) | "rawText"        |
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
	file_path="./python/tests/data/qa_appbuilder_client_demo.pdf",
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

### 9、从知识库删除文档 `KnowledgeBase().delete_document()->KnowledgeBaseDeleteDocumentResponse`

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

### 10、获取知识库的文档列表`KnowledgeBase().get_documents_list()->KnowledgeBaseGetDocumentsListResponse` 

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
    source: Optional[str] = Field(None, description="文档来源")
    file_id: Optional[str] = Field(None, description="文档对应的文件ID")
    url: Optional[str] = Field(None, description="原文件下载链接")
    mime_type: Optional[str] = Field(
        None,
        description="文件类型，目前支持doc/txt/docx/pdf/ppt/pptx/xlsx/xls/csv/json这几种文件类型。如果是通过url方式导入的文档，该值为url",
    )
    file_size: Optional[int] = Field(None, description="文件大小，单位bytes")
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

### 11、获取知识库全部文档`KnowledgeBase().get_all_documents()->list`

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
    source: Optional[str] = Field(None, description="文档来源")
    file_id: Optional[str] = Field(None, description="文档对应的文件ID")
    url: Optional[str] = Field(None, description="原文件下载链接")
    mime_type: Optional[str] = Field(
        None,
        description="文件类型，目前支持doc/txt/docx/pdf/ppt/pptx/xlsx/xls/csv/json这几种文件类型。如果是通过url方式导入的文档，该值为url",
    )
    file_size: Optional[int] = Field(None, description="文件大小，单位bytes")
```

#### 方法示例
```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

doc_list = my_knowledge.get_all_documents(my_knowledge_base_id)
for message in doc_list:
    print(message)
```

### 12. 创建切片`create_chunk(documentId: str, content: str) -> CreateChunkResponse`

#### 方法参数

| 参数名称        | 参数类型 | 是否必传 | 描述     | 示例值         |
| --------------- | -------- | -------- | -------- | -------------- |
| knowledgeBaseId | string   | 是       | 知识库ID |                |
| documentId      | string   | 是       | 文档ID   | "正确的文档ID" |
| content         | string   | 是       | 切片内容 | "内容"         |

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
resp = my_knowledge.create_chunk("your_document_id", "content", knowledgebase_id=knowledge_base_id)
print("切片ID: ", resp.id)
chunk_id = resp.id
```

### 13. 修改切片信息`modify_chunk(chunkId: str, content: str, enable: bool)`

#### 方法参数

| 参数名称   | 参数类型 | 是否必传     | 描述         | 示例值         |
| ---------- | -------- | ------------ | -------------- | -------------- |
| knowledgeBaseId | string | 是 | 知识库ID |  |
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
my_knowledge.modify_chunk("your_chunk_id", "content", True, knowledgebase_id=my_knowledge_base_id)
```

### 14. 删除切片`delete_chunk(chunkId: str)`

#### 方法参数

| 参数名称        | 参数类型 | 是否必传 | 描述     | 示例值         |
| --------------- | -------- | -------- | -------- | -------------- |
| knowledgeBaseId | string   | 是       | 知识库ID |                |
| chunkId         | string   | 是       | 文档ID   | "正确的切片ID" |

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)
my_knowledge.delete_chunk("your_chunk_id", knowledgebase_id=my_knowledge_base_id)
```

### 15. 获取切片信息`describe_chunk(chunkId: str)`

#### 方法参数

| 参数名称        | 参数类型 | 是否必传 | 描述     | 示例值         |
| --------------- | -------- | -------- | -------- | -------------- |
| knowledgeBaseId | string   | 是       | 知识库ID |                |
| chunkId         | string   | 是       | 文档ID   | "正确的切片ID" |

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
resp = my_knowledge.describe_chunk("your_chunk_id", knowledgebase_id=my_knowledge_base_id)
print("切片详情：")
print(resp)
```

### 16. 获取切片列表`describe_chunks(documentId: str, marker: str = None, maxKeys: int = None, type: str = None) -> DescribeChunksResponse`

#### 方法参数

| 参数名称        | 参数类型 | 是否必传 | 描述                                                         | 示例值         |
| --------------- | -------- | -------- | ------------------------------------------------------------ | -------------- |
| knowledgeBaseId | string   | 是       | 知识库ID                                                     |                |
| documentId      | string   | 是       | 文档ID                                                       | "正确的文档ID" |
| marker          | string   | 否       | 起始位置，切片ID                                             | "正确的切片ID" |
| maxKeys         | string   | 否       | 返回文档数量大小，默认10，最大值100                          | 10             |
| type            | string   | 否       | 根据类型获取切片列表(RAW、NEW、COPY)，RAW：原文切片，NEW：新增切片，COPY：复制切片 | "RAW"          |
| keyword         | string   | 否       | 根据关键字模糊匹配切片，最大长度2000字符。                   | "test"         |

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
resp = my_knowledge.describe_chunks("your_document_id", knowledgebase_id=my_knowledge_base_id)
print("切片列表：")
print(resp)
```

### 17. 知识库检索`query_knowledge_base(query: str, knowledgebase_ids: list[str], type: Optional[data_class.QueryType] = None, metadata_filters: data_class.MetadataFilter = None,pipeline_config: data_class.QueryPipelineConfig = None, rank_score_threshold: Optional[float] = 0.4, top: int = 6, skip: int = None) -> data_class.QueryKnowledgeBaseResponse`

#### 方法参数

| 参数名称        | 参数类型 | 是否必传 | 描述                                                         | 示例值         |
| --------------- | -------- | -------- | ------------------------------------------------------------ | -------------- |
| query | string   | 是       | 检索query，最长为1024字符，超过自动截断                                                   |民法典第三条                |
| knowledgebase_ids      | list[str]   | 是       | 指定知识库的id集合                                                       | ["kb-1", "kb-2"] |
| type          | string   | 否       | 检索策略。<br>可选值：<br>* fulltext，全文检索<br>* semantic，语义检索<br>* hybird，混合检索| "fulltext" |
| metadata_filters         | data_class.MetadataFilters | 否       | 元数据过滤条件，详细见MetadataFilters                          | -             |
| pipeline_config            | data_class.QueryPipelineConfig   | 否       | 检索配置，详细见QueryPipelineConfig | -          |
| rank_score_threshold         | float   | 否       | 重排序匹配分阈值，只有rank_score大于等于该分值的切片重排序时才会被筛选出来。<br>当且仅当，pipeline_config中配置了ranking节点时，该过滤条件生效。<br>取值范围： [0, 1]。<br>默认0.4                          | 0.4             |
| top            | int   | 否       | 返回前多少的条目。默认值6。如果检索结果的数量未达到top值，则按实际检索到的结果数量返回 | 6          |
| skip         | int   | 否       | 跳过条目数（通过top和skip可以实现类似分页的效果，比如top 10 skip 0，取第一页的10个，top 10 skip 10，取第二页的10个）| 0             |

`data_class.MetadataFilters` 类定义如下：

```python
class MetadataFilters(BaseModel):
    filters: list[MetadataFilter] = Field(..., description="过滤条件")
    condition: str = Field(..., description="文档组合条件。and:与，or:或")
```

`data_class.MetadataFilter` 类定义如下：

```python
class MetadataFilter(BaseModel):
    operator: str = Field(..., description="操作符名称。==:等于，in:在数组中，not_in:不在数组中")
    field: str = Field(None, description="字段名，目前支持doc_id")
    value: Union[str, list[str]] = Field(
        ..., description="字段值，如果是in操作符，value为数组"
    )
```


`data_class.QueryPipelineConfig` 类定义如下：

```python
class QueryPipelineConfig(BaseModel):
    id: str = Field(
        None, description="配置唯一标识，如果用这个id，则引用已经配置好的QueryPipeline"
    )
    pipeline: list[Union[ElasticSearchRetrieveConfig, RankingConfig, VectorDBRetrieveConfig, SmallToBigConfig]] = Field(
        None, description="配置的Pipeline，如果没有用id，可以用这个对象指定一个新的配置"
    )
```

`data_class.ElasticSearchRetrieveConfig` 类定义如下：

```python
class ElasticSearchRetrieveConfig(BaseModel): # 托管资源为共享资源 或 BES资源时使用该配置
    name: str = Field(..., description="配置名称")
    type: str = Field(None, description="elastic_search标志，该节点为es全文检索")
    threshold: float = Field(None, description="得分阈值，默认0.1")
    top: int = Field(None, description="召回数量，默认400")
```

`data_class.RankingConfig` 类定义如下：

```python
class RankingConfig(BaseModel):
    name: str = Field(..., description="配置名称")
    type: str = Field(None, description="ranking标志，该节点为ranking节点")
    inputs: list[str] = Field(
        ...,
        description='输入的节点名，如es检索配置的名称为pipeline_001，则该inputs为["pipeline_001"]',
    )
    model_name: str = Field(None, description="ranking模型名（当前仅一种，暂不生效）")
    top: int = Field(None, description="取切片top进行排序，默认20，最大400")
```

`data_class.VectorDBRetrieveConfig` 类定义如下：

```python
class VectorDBRetrieveConfig(BaseModel):
    name: str = Field(..., description="该节点的自定义名称。")
    type: str = Field("vector_db", description="该节点的类型，默认为vector_db。")
    threshold: Optional[float] = Field(0.1, description="得分阈值。取值范围：[0, 1]", ge=0.0, le=1.0)
    top: Optional[int] = Field(400, description="召回数量。取值范围：[0, 800]", ge=0, le=800)
    pre_ranking: Optional[PreRankingConfig] = Field(None, description="粗排配置")
```

`data_class.PreRankingConfig` 类定义如下：

```python
class PreRankingConfig(BaseModel):
    bm25_weight: float = Field(
        None, description="粗排bm25比重，取值范围在 [0, 1]，默认0.75"
    )
    vec_weight: float = Field(
        None, description="粗排向量余弦分比重，取值范围在 [0, 1]，默认0.25"
    )
    bm25_b: float = Field(
        None, description="控制文档长度对评分影响的参数，取值范围在 [0, 1]，默认0.75"
    )
    bm25_k1: float = Field(
        None,
        description="词频饱和因子，控制词频（TF）对评分的影响，常取值范围在 [1.2, 2.0]，默认1.5",
    )
    bm25_max_score: float = Field(
        None, description="得分归一化参数，不建议修改，默认50"
    )
```

#### 方法返回值

`data_class.QueryKnowledgeBaseResponse` 类定义如下：

```python
class QueryKnowledgeBaseResponse(BaseModel):
    requestId: str = Field(None, description="请求ID")
    code: str = Field(None, description="状态码")
    message: str = Field(None, description="状态信息")
    chunks: list[Chunk] = Field(..., description="切片列表")
    total_count: int = Field(..., description="切片总数")
```

衍生类`Chunk`定义如下：

```python
class Chunk(BaseModel):
    chunk_id: str = Field(..., description="切片ID")
    knowledgebase_id: str = Field(..., description="知识库ID")
    document_id: str = Field(..., description="文档ID")
    document_name: str = Field(None, description="文档名称")
    meta: dict = Field(None, description="文档元数据")
    chunk_type: str = Field(..., description="切片类型")
    content: str = Field(..., description="切片内容")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    retrieval_score: float = Field(..., description="粗检索得分")
    rank_score: float = Field(..., description="rerank得分")
    locations: ChunkLocation = Field(None, description="切片位置")
    children: List[Chunk] = Field(None, description="子切片")
```

#### 方法示例

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

knowledge = appbuilder.KnowledgeBase()
client = appbuilder.KnowledgeBase()
res = client.query_knowledge_base(
    query="民法典第三条",
    type="fulltext",
    knowledgebase_ids=["70c6375a-1595-41f2-9a3b-e81bc9060b7f"],
    top=5,
    skip=0,
    metadata_filters=data_class.MetadataFilters(filters=[], condition="or"),
    pipeline_config=data_class.QueryPipelineConfig(
        id="pipeline_001",
        pipeline=[
            {
                "name": "step1",
                "type": "elastic_search",
                "threshold": 0.1,
                "top": 400,
                "pre_ranking": {
                    "bm25_weight": 0.25,
                    "vec_weight": 0.75,
                    "bm25_b": 0.75,
                    "bm25_k1": 1.5,
                    "bm25_max_score": 50,
                },
            },
            {
                "name": "step2",
                "type": "ranking",
                "inputs": ["step1"],
                "model_name": "ranker-v1",
                "top": 20,
            },
        ],
    ),
)
chunk_id = res.chunks[0].chunk_id
for chunk in res.chunks:
    print(chunk.content)
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
    public void testDocument() throws IOException, AppBuilderServerException {
        // 实例化Knowledgebase
        String knowledgeBaseId  = "";
        Knowledgebase knowledgebase = new Knowledgebase();

        // 获取知识库文档列表
        DocumentListRequest listRequest = new DocumentListRequest(); 
        listRequest.setKonwledgeBaseId(knowledgeBaseId);
        listRequest.setLimit(10);
        Document[] documents = knowledgebase.getDocumentList(listRequest);

        // 从知识库删除文档
        DocumentDeleteRequest deleteRequest = new DocumentDeleteRequest();
        deleteRequest.setKonwledgeBaseId(knowledgeBaseId);
        deleteRequest.setDocumentId("期望删除的DocumentId");
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
                "", "", "", "");
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
        // 知识库ID
        String knowledgeBaseId = "";
        // Appbuilder Token
        String secretKey = "";
        Knowledgebase knowledgebase = new Knowledgebase(knowledgeBaseID, secretKey);
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

    // 从知识库中删除文档
	err = client.DeleteDocument(DeleteDocumentRequest{
		KnowledgeBaseID: knowledgeBaseID,
		DocumentID:      "期望删除的DocumentID"})
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
  knowledgeBaseID := "";
	config, err := NewSDKConfig("", "")
	if err != nil {
		t.Fatalf("new http client config failed: %v", err)
	}

	client, err := NewKnowledgeBaseWithKnowledgeBaseID(knowledgeBaseID, config)
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
