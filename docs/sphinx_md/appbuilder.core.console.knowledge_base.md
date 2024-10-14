<a id="module-appbuilder.core.console.knowledge_base.knowledge_base"></a>

### *class* appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase(knowledge_id: str | None = None, knowledge_name: str | None = None, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

#### add_document(content_type: str, file_ids: list[str] = [], is_enhanced: bool = False, custom_process_rule: [CustomProcessRule](appbuilder.md#appbuilder.CustomProcessRule) | None = None, knowledge_base_id: str | None = None, client_token: str = None) → KnowledgeBaseAddDocumentResponse

向知识库中添加文档。

* **参数:**
  * **content_type** (*str*) – 文档的类型，例如 ‘TEXT’ 或 ‘PDF’。
  * **file_ids** (*list* *[**str* *]* *,* *optional*) – 文档ID列表，默认为空列表。文档ID通常由文件上传接口返回。
  * **is_enhanced** (*bool* *,* *optional*) – 是否启用增强模式，默认为False。启用后会对文档进行语义理解和结构化处理。
  * **custom_process_rule** (*Optional* *[*[*data_class.CustomProcessRule*](appbuilder.md#appbuilder.CustomProcessRule) *]* *,* *optional*) – 自定义处理规则，默认为None。
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，默认为None。如果未指定，则使用当前实例的知识库ID。
  * **client_token** (*str* *,* *optional*) – 客户端请求的唯一标识，默认为None。如果不指定，则自动生成。
* **返回:**
  添加文档后的响应对象。
* **返回类型:**
  data_class.KnowledgeBaseAddDocumentResponse
* **抛出:**
  **ValueError** – 如果知识库ID为空且未先调用\`create\`方法或未指定现有知识库ID，则抛出ValueError异常。

#### create_chunk(documentId: str, content: str, client_token: str = None) → CreateChunkResponse

创建一个知识块。

* **参数:**
  * **documentId** (*str*) – 文档ID。
  * **content** (*str*) – 知识块内容。
  * **client_token** (*str* *,* *optional*) – 用于支持幂等性，默认为None。如果为None，则使用uuid4生成一个唯一的client_token。
* **返回:**
  创建知识块响应。
* **返回类型:**
  data_class.CreateChunkResponse
* **抛出:**
  **HTTPError** – 如果请求失败，将抛出HTTPError异常。

#### create_documents(id: str | None = None, contentFormat: str = '', source: [DocumentSource](appbuilder.md#appbuilder.DocumentSource) = None, processOption: [DocumentProcessOption](appbuilder.md#appbuilder.DocumentProcessOption) = None, client_token: str = None)

创建文档。

* **参数:**
  * **id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，默认为None。如果为None，则使用当前知识库ID。默认为None。
  * **contentFormat** (*str*) – 文档内容格式，默认为空字符串。
  * **source** ([*data_class.DocumentSource*](appbuilder.md#appbuilder.DocumentSource) *,* *optional*) – 文档来源信息，默认为None。
  * **processOption** ([*data_class.DocumentProcessOption*](appbuilder.md#appbuilder.DocumentProcessOption) *,* *optional*) – 文档处理选项，默认为None。
  * **client_token** (*str* *,* *optional*) – 用于标识请求的客户端令牌，默认为None。如果不提供，将自动生成一个UUID。
* **返回:**
  API响应结果。
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果当前知识库ID为空且未提供id参数，则抛出ValueError异常。

#### *classmethod* create_knowledge(knowledge_name: str) → [KnowledgeBase](#appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase)

创建一个新的知识库。

* **参数:**
  * **cls** (*type*) – 类对象，用于调用此方法时不需要显式传递。
  * **knowledge_name** (*str*) – 要创建的知识库名称。
* **返回:**
  创建的知识库对象。
* **返回类型:**
  [KnowledgeBase](#appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase)
* **抛出:**
  * **HTTPError** – 如果HTTP请求失败或响应状态码不为200。
  * **JSONDecodeError** – 如果响应数据不是有效的JSON格式。

#### NOTE
此方法已被弃用，请使用 create_knowledge_base 方法代替。

#### create_knowledge_base(name: str, description: str, type: str = 'public', esUrl: str = None, esUserName: str = None, esPassword: str = None, client_token: str = None) → KnowledgeBaseDetailResponse

创建一个知识库

* **参数:**
  * **name** (*str*) – 知识库名称
  * **description** (*str*) – 知识库描述
  * **type** (*str* *,* *optional*) – 知识库类型，默认为’public’。默认为 “public”。
  * **esUrl** (*str* *,* *optional*) – Elasticsearch 服务地址。默认为 None。
  * **esUserName** (*str* *,* *optional*) – Elasticsearch 用户名。默认为 None。
  * **esPassword** (*str* *,* *optional*) – Elasticsearch 密码。默认为 None。
  * **client_token** (*str* *,* *optional*) – 客户端token，用于区分请求来源。默认为 None。
* **返回:**
  创建知识库后的响应对象
* **返回类型:**
  data_class.KnowledgeBaseDetailResponse
* **抛出:**
  **requests.exceptions.HTTPError** – 请求失败时抛出

#### delete_chunk(chunkId: str, client_token: str = None)

删除知识库中的一个块

* **参数:**
  * **chunkId** (*str*) – 要删除的块的ID
  * **client_token** (*str* *,* *optional*) – 客户端令牌，用于请求的唯一标识，默认为None。
* **返回:**
  包含删除操作结果的字典。
* **返回类型:**
  dict

#### delete_document(document_id: str, knowledge_base_id: str | None = None, client_token: str = None) → KnowledgeBaseDeleteDocumentResponse

删除知识库中的文档

* **参数:**
  * **document_id** (*str*) – 要删除的文档ID
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果为None，则使用类的知识库ID。默认为None。
  * **client_token** (*str* *,* *optional*) – 请求的唯一标识，用于服务器追踪问题。默认为None，如果不传则自动生成。
* **返回:**
  删除文档响应对象
* **返回类型:**
  data_class.KnowledgeBaseDeleteDocumentResponse
* **抛出:**
  **ValueError** – 如果未设置类的知识库ID且未提供知识库ID，则抛出ValueError异常。

#### delete_knowledge_base(knowledge_base_id: str | None = None, client_token: str = None)

删除知识库

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID. 如果未提供，则使用当前实例的knowledge_id. Defaults to None.
  * **client_token** (*str* *,* *optional*) – 请求的唯一标识，用于服务端去重. 如果未提供，则自动生成一个UUID. Defaults to None.
* **返回:**
  API响应数据
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果既没有提供knowledge_base_id，且当前实例的knowledge_id也为None，则抛出异常

#### describe_chunk(chunkId: str) → DescribeChunkResponse

获取知识库片段信息

* **参数:**
  **chunkId** (*str*) – 知识库片段的ID
* **返回:**
  知识库片段信息响应对象
* **返回类型:**
  DescribeChunkResponse

#### describe_chunks(documentId: str, marker: str = None, maxKeys: int = None, type: str = None) → DescribeChunksResponse

查询文档分块信息

* **参数:**
  * **documentId** (*str*) – 文档ID
  * **marker** (*str* *,* *optional*) – 分页标记，默认为None。用于分页查询，如果第一页调用此API后，还有更多数据，API会返回一个Marker值，使用此Marker值调用API可以查询下一页数据，直到没有更多数据，API将不再返回Marker值。
  * **maxKeys** (*int* *,* *optional*) – 最大返回记录数，默认为None。指定本次调用最多可以返回的文档分块信息条数，最大值为100。
  * **type** (*str* *,* *optional*) – 文档分块类型，默认为None。指定要查询的文档分块类型。
* **返回:**
  包含文档分块信息的响应对象
* **返回类型:**
  DescribeChunksResponse

#### get_all_documents(knowledge_base_id: str | None = None) → dict

获取知识库中所有文档。

* **参数:**
  **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库的ID。如果为None，则使用当前实例的knowledge_id。默认为None。
* **返回:**
  包含所有文档的列表。
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果knowledge_base_id为空，且当前实例没有已创建的knowledge_id时抛出。

#### get_documents_list(limit: int = 10, after: str | None = '', before: str | None = '', knowledge_base_id: str | None = None) → KnowledgeBaseGetDocumentsListResponse

获取文档列表。

* **参数:**
  * **limit** (*int* *,* *optional*) – 返回的文档数量上限，默认为10。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 返回时间戳大于指定值的文档。默认为空字符串。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 返回时间戳小于指定值的文档。默认为空字符串。
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果未指定，则使用当前实例的知识库ID。默认为None。
* **返回:**
  包含文档列表的响应对象。
* **返回类型:**
  data_class.KnowledgeBaseGetDocumentsListResponse
* **抛出:**
  **ValueError** – 如果知识库ID为空，且未通过调用create方法创建知识库，则抛出此异常。

#### get_knowledge_base_detail(knowledge_base_id: str | None = None) → KnowledgeBaseDetailResponse

获取知识库详情。

* **参数:**
  **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID. 如果为None，则使用实例中的knowledge_id.
  默认为None.
* **返回:**
  知识库详情响应对象.
* **返回类型:**
  data_class.KnowledgeBaseDetailResponse
* **抛出:**
  **ValueError** – 如果knowledge_base_id为空且实例中的knowledge_id也为空，则抛出异常.

#### get_knowledge_base_list(knowledge_base_id: str | None = None, maxKeys: int = 10, keyword: str | None = None) → KnowledgeBaseGetListResponse

获取知识库列表

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID. 如果为None，则使用self.knowledge_id. 默认为None.
  * **maxKeys** (*int* *,* *optional*) – 最大返回数量. 默认为10.
  * **keyword** (*Optional* *[**str* *]* *,* *optional*) – 搜索关键字. 默认为None.
* **返回:**
  知识库列表响应对象.
* **返回类型:**
  data_class.KnowledgeBaseGetListResponse
* **抛出:**
  **ValueError** – 如果self.knowledge_id和knowledge_base_id都为None，则抛出异常，提示需要先调用create方法或使用已存在的知识库ID.

#### modify_chunk(chunkId: str, content: str, enable: bool, client_token: str = None)

修改知识库片段

* **参数:**
  * **chunkId** (*str*) – 知识库片段ID
  * **content** (*str*) – 修改后的内容
  * **enable** (*bool*) – 是否启用该知识库片段
  * **client_token** (*str* *,* *optional*) – 请求的唯一标识，默认为 None. 如果不指定，则自动生成.
* **返回:**
  修改后的知识库片段信息
* **返回类型:**
  dict
* **抛出:**
  * **HttpClientError** – 如果请求失败，则抛出 HttpClientError 异常
  * **ConsoleResponseError** – 如果控制台响应错误，则抛出 ConsoleResponseError 异常

#### modify_knowledge_base(knowledge_base_id: str | None = None, name: str | None = None, description: str | None = None, client_token: str = None)

修改知识库信息

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果为None，则使用当前实例的知识库ID. 默认为 None.
  * **name** (*Optional* *[**str* *]* *,* *optional*) – 知识库名称. 默认为 None.
  * **description** (*Optional* *[**str* *]* *,* *optional*) – 知识库描述. 默认为 None.
  * **client_token** (*str* *,* *optional*) – 客户端唯一标识符，用于保证幂等性. 默认为 None.
* **返回:**
  修改后的知识库信息
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果既没有提供knowledge_base_id，且当前实例没有设置knowledge_id，则抛出此异常.

#### upload_documents(file_path: str, content_format: str = 'rawText', id: str | None = None, processOption: [DocumentProcessOption](appbuilder.md#appbuilder.DocumentProcessOption) = None, client_token: str = None)

上传文档到知识库

* **参数:**
  * **file_path** (*str*) – 文件路径
  * **content_format** (*str* *,* *optional*) – 内容格式，默认为 ‘rawText’。可选项包括 ‘rawText’, ‘markdown’, ‘html’ 等
  * **id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，默认为None，此时将使用当前实例的知识库ID
  * **processOption** ([*data_class.DocumentProcessOption*](appbuilder.md#appbuilder.DocumentProcessOption) *,* *optional*) – 文档处理选项，默认为None
  * **client_token** (*str* *,* *optional*) – 客户端token，默认为None，将自动生成一个UUID
* **返回:**
  上传文档后的响应数据
* **返回类型:**
  dict
* **抛出:**
  **FileNotFoundError** – 如果指定的文件路径不存在，将抛出 FileNotFoundError 异常

#### upload_file(file_path: str, client_token: str = None) → KnowledgeBaseUploadFileResponse

上传文件到知识库服务器。

* **参数:**
  * **file_path** (*str*) – 要上传的文件的路径。
  * **client_token** (*str* *,* *optional*) – 客户端令牌，用于标识请求的唯一性。如果未提供，则自动生成。
* **返回:**
  上传文件的响应。
* **返回类型:**
  data_class.KnowledgeBaseUploadFileResponse
* **抛出:**
  **FileNotFoundError** – 如果指定的文件路径不存在，则抛出 FileNotFoundError 异常。

# Module contents
