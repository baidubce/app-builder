<a id="module-appbuilder.core.console.knowledge_base.knowledge_base"></a>

### *class* appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase(knowledge_id: str | None = None, knowledge_name: str | None = None, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

console知识库操作工具，用于创建、删除、查询、更新知识库等操作

Examples:

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

my_knowledge_base_id = "your_knowledge_base_id"
my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
print("知识库ID: ", my_knowledge.knowledge_id)

list_res = my_knowledge.get_documents_list(my_knowledge_base_id)
print("文档列表: ", list_res)
```

#### add_document(content_type: str, file_ids: list[str] = [], is_enhanced: bool = False, custom_process_rule: CustomProcessRule | None = None, knowledge_base_id: str | None = None, client_token: str | None = None) → KnowledgeBaseAddDocumentResponse

添加文档到知识库

* **参数:**
  * **content_type** (*str*) – 内容类型，可选值有”raw_text”, “qa”。
  * **file_ids** (*List* *[**str* *]* *,* *optional*) – 文件ID列表。默认为空列表。
  * **is_enhanced** (*bool* *,* *optional*) – 是否增强。默认为False。
  * **custom_process_rule** (*Optional* *[**data_class.CustomProcessRule* *]* *,* *optional*) – 自定义处理规则。默认为None。
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID。默认为None，此时使用当前类的knowledge_id属性。
  * **client_token** (*str*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  添加文档的相应结果。包含以下属性：
  - request_id (str): 请求ID
  - knowledge_base_id (str): 知识库ID
  - document_ids (list[str]): 成功新建的文档id集合
* **返回类型:**
  KnowledgeBaseAddDocumentResponse

#### create_chunk(documentId: str, content: str, client_token: str | None = None) → CreateChunkResponse

创建文档块

* **参数:**
  * **documentId** (*str*) – 文档ID
  * **content** (*str*) – 内容
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  创建文档块的相应消息, 包含以下属性：
  - id (str): 切片ID
* **返回类型:**
  CreateChunkResponse

#### create_documents(id: str | None = None, contentFormat: str = '', source: DocumentSource | None = None, processOption: DocumentProcessOption | None = None, client_token: str | None = None)

创建文档

* **参数:**
  * **id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
  * **contentFormat** (*str* *,* *optional*) – 文档内容格式，可以是”rawText”, “qa”之一。默认值为””。
  * **source** (*data_class.DocumentSource* *,* *optional*) – 文档源数据。默认值为None。
  * **processOption** (*data_class.DocumentProcessOption* *,* *optional*) – 文档处理选项。默认值为None。
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  响应数据，包含请求ID: requestId
* **返回类型:**
  dict

#### *classmethod* create_knowledge(knowledge_name: str) → [KnowledgeBase](#appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase)

创建知识库

Deprecated: use create_knowledge_base instead

* **参数:**
  **knowledge_name** (*str*) – 知识库名称
* **返回:**
  返回一个KnowledgeBase对象
* **返回类型:**
  [KnowledgeBase](#appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase)

#### create_knowledge_base(name: str, description: str, type: str = 'public', esUrl: str | None = None, esUserName: str | None = None, esPassword: str | None = None, client_token: str | None = None) → KnowledgeBaseDetailResponse

创建知识库

* **参数:**
  * **name** (*str*) – 知识库名称。
  * **description** (*str*) – 知识库描述。
  * **type** (*str* *,* *optional*) – 知识库类型。默认为”public”。
  * **esUrl** (*str* *,* *optional*) – Elasticsearch服务器地址。默认为None。
  * **esUserName** (*str* *,* *optional*) – Elasticsearch用户名。默认为None。
  * **esPassword** (*str* *,* *optional*) – Elasticsearch密码。默认为None。
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  创建知识库的响应消息,包含以下属性：
  - id (str): 知识库ID
  - name (str): 知识库名称
  - description (Optional[str], optional): 知识库描述
  - config (Optional[KnowledgeBaseConfig], optional): 知识库配置
* **返回类型:**
  KnowledgeBaseDetailResponse

#### delete_chunk(chunkId: str, client_token: str | None = None)

删除文档块

* **参数:**
  * **chunkId** (*str*) – 文档块ID
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  响应数据，包含请求ID: requestId
* **返回类型:**
  dict

#### delete_document(document_id: str, knowledge_base_id: str | None = None, client_token: str | None = None) → KnowledgeBaseDeleteDocumentResponse

删除知识库中的文档

* **参数:**
  * **document_id** (*str*) – 文档ID
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID。默认为None，此时使用当前类的knowledge_id属性。
  * **client_token** (*str*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  删除文档的响应消息,包含以下属性：
  - request_id (str): 请求ID
* **返回类型:**
  KnowledgeBaseDeleteDocumentResponse

#### delete_knowledge_base(knowledge_base_id: str | None = None, client_token: str | None = None)

删除知识库

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  requestId
* **返回类型:**
  响应数据，包含请求ID

#### describe_chunk(chunkId: str) → DescribeChunkResponse

获取文档块详情

* **参数:**
  **chunkId** (*str*) – 文档块ID
* **返回:**
  文档块详情，一个DescribeChunkResponse对象,包含以下属性：
  - id (str): 切片ID
  - type (str): 切片类型
  - knowledgeBaseId (str): 知识库ID
  - documentId (str): 文档ID
  - content (str): 文档内容
  - enabled (bool): 是否启用
  - wordCount (int): 切片内字符数量
  - tokenCount (int): 切片内token数量
  - status (str): 切片状态
  - statusMessage (str): 切片状态信息
  - createTime (int): 创建时间
  - updateTime (int): 更新时间
* **返回类型:**
  DescribeChunkResponse

#### describe_chunks(documentId: str, marker: str | None = None, maxKeys: int | None = None, type: str | None = None) → DescribeChunksResponse

获取文档块列表

* **参数:**
  * **documentId** (*str*) – 文档ID
  * **marker** (*str* *,* *optional*) – 分页标记，用于指定从哪个位置开始返回结果。默认为None，表示从头开始返回结果。
  * **maxKeys** (*int* *,* *optional*) – 最大返回数量，用于限制每次请求返回的最大文档块数目。默认为None，表示不限制返回数量。
  * **type** (*str* *,* *optional*) – 文档块类型。默认为None，表示不限定类型。
* **返回:**
  文档块列表，一个DescribeChunksResponse对象,包含以下属性：
  - data (list[DescribeChunkResponse]): 切片列表
  - marker (str): 起始位置
  - isTruncated (bool): true表示后面还有数据，false表示已经是最后一页
  - nextMarker (str): 下一页起始位置
  - maxKeys (int): 本次查询包含的最大结果集数量
* **返回类型:**
  DescribeChunksResponse

#### get_all_documents(knowledge_base_id: str | None = None) → list

获取知识库中所有文档。

* **参数:**
  **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库的ID。如果为None，则使用当前实例的knowledge_id。默认为None。
* **返回:**
  包含所有文档的列表。
* **返回类型:**
  list
* **抛出:**
  **ValueError** – 如果knowledge_base_id为空，且当前实例没有已创建的knowledge_id时抛出。

#### get_documents_list(limit: int = 10, after: str | None = '', before: str | None = '', knowledge_base_id: str | None = None) → KnowledgeBaseGetDocumentsListResponse

获取知识库中的文档列表

* **参数:**
  * **limit** (*int* *,* *optional*) – 限制数量。默认为10。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 起始位置。默认为空字符串””。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 结束位置。默认为空字符串””。
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID。默认为None，此时使用当前类的knowledge_id属性。
* **返回:**
  知识库文档列表服务的响应消息,包含以下属性：
  - request_id (str): 请求ID
  - data (list[Document]): 文档信息列表
* **返回类型:**
  KnowledgeBaseGetDocumentsListResponse

#### get_knowledge_base_detail(knowledge_base_id: str | None = None) → KnowledgeBaseDetailResponse

获取知识库详情

* **参数:**
  **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
* **返回:**
  知识库详情，返回一个KnowledgeBaseDetailResponse对象,包含以下属性：
  - id (str): 知识库ID
  - name(str): 知识库名称
  - description(Optional[str], optional): 知识库描述
  - config(Optional[KnowledgeBaseConfig], optional): 知识库配置
* **返回类型:**
  KnowledgeBaseDetailResponse

#### get_knowledge_base_list(knowledge_base_id: str | None = None, maxKeys: int = 10, keyword: str | None = None) → KnowledgeBaseGetListResponse

获取知识库列表

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
  * **maxKeys** (*int* *,* *optional*) – 最大键数。默认值为10。
  * **keyword** (*Optional* *[**str* *]* *,* *optional*) – 关键字。默认值为None。
* **返回:**
  获取知识库列表的响应消息，返回一个KnowledgeBaseGetListResponse对象，包含以下属性：
  - requestId (str): 请求ID
  - data (list[KnowledgeBaseDetailResponse]): 知识库详情列表
  - marker (str): 起始位置
  - nextMarker (str): 下一页起始位置
  - maxKeys (int): 返回文档数量大小，默认10，最大值100
  - isTruncated (bool): 是否有更多结果
* **返回类型:**
  KnowledgeBaseGetListResponse

#### modify_chunk(chunkId: str, content: str, enable: bool, client_token: str | None = None)

修改文档块

* **参数:**
  * **chunkId** (*str*) – 文档块ID
  * **content** (*str*) – 内容
  * **enable** (*bool*) – 是否启用
* **返回:**
  响应数据，包含请求ID: requestId
* **返回类型:**
  dict

#### modify_knowledge_base(knowledge_base_id: str | None = None, name: str | None = None, description: str | None = None, client_token: str | None = None)

修改知识库信息

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
  * **name** (*Optional* *[**str* *]* *,* *optional*) – 新的知识库名称。默认值为None。
  * **description** (*Optional* *[**str* *]* *,* *optional*) – 新的知识库描述。默认值为None。
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  响应数据，包含请求ID: requestId。
* **返回类型:**
  dict

#### upload_documents(file_path: str, content_format: str = 'rawText', id: str | None = None, processOption: DocumentProcessOption | None = None, client_token: str | None = None)

上传文档

* **参数:**
  * **file_path** (*str*) – 文件路径
  * **content_format** (*str* *,* *optional*) – 内容格式。默认值为”rawText”。
  * **id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
  * **processOption** (*data_class.DocumentProcessOption* *,* *optional*) – 文档处理选项。默认值为None。
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  响应数据，包含请求ID: requestId
* **返回类型:**
  dict

#### upload_file(file_path: str, client_token: str | None = None) → KnowledgeBaseUploadFileResponse

上传文件到知识库

* **参数:**
  * **file_path** (*str*) – 文件路径
  * **client_token** (*str* *,* *optional*) – 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
* **返回:**
  返回一个KnowledgeBaseUploadFileResponse对象，包含以下属性：
  - request_id (int): 请求id
  - id (str): 文件id
  - name (dict): 文件名称
* **返回类型:**
  KnowledgeBaseUploadFileResponse
