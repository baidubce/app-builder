# appbuilder.core.assistant.assistants package

## Submodules

## appbuilder.core.assistant.assistants.assistants module

### *class* appbuilder.core.assistant.assistants.assistants.Assistants

基类：`object`

#### create(name: str, description: str, model: str | None = 'ERNIE-4.0-8K', response_format: str | None = 'text', instructions: str | None = '你是百度制作的AI助手', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], file_ids: list[str] | None = [], metadata: dict | None = {}) → AssistantCreateResponse

创建助手实例

* **参数:**
  * **name** (*str*) – 助手名称
  * **description** (*str*) – 助手描述
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 模型名称. Defaults to “ERNIE-4.0-8K”.
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 响应格式. Defaults to ‘text’.
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 指令. Defaults to “”.
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思考指令. Defaults to “”.
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 聊天指令. Defaults to “”.
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 工具列表. Defaults to [].
  * **file_ids** (*Optional* *[**list* *[**str* *]* *]* *,* *optional*) – 文件ID列表. Defaults to [].
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据. Defaults to {}.
* **返回:**
  助手创建响应
* **返回类型:**
  assistant_type.AssistantCreateResponse

#### delete(assistant_id: str | None) → AssistantDeleteResponse

根据assistant_id删除指定Assitant

* **参数:**
  **assistant_id** (*Optional* *[**str* *]*) – 待删除的助手实例ID。
* **返回:**
  删除助手实例后的响应结果。
* **返回类型:**
  assistant_type.AssistantDeleteResponse
* **抛出:**
  **HttpRequestError** – 发送HTTP请求时发生错误。

#### *property* files

获取当前工作目录下的文件对象。

* **参数:**
  **无**
* **返回:**
  返回当前工作目录下的文件对象。
* **返回类型:**
  [Files](#appbuilder.core.assistant.assistants.files.Files)

#### list(limit: int | None = 20, order: str | None = 'desc', after: str | None = '', before: str | None = '') → AssistantListResponse

查询当前用户已创建的assistant列表

* **参数:**
  * **limit** (*Optional* *[**int* *]* *,* *optional*) – 返回助手列表的最大数量，默认为20。
  * **order** (*Optional* *[**str* *]* *,* *optional*) – 返回助手列表的排序方式，可选值为”asc”或”desc”，默认为”desc”。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 返回助手列表中id在指定id之后的助手，默认为空字符串。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 返回助手列表中id在指定id之前的助手，默认为空字符串。
* **返回:**
  助手列表响应体。
* **返回类型:**
  assistant_type.AssistantListResponse

#### mount_files(assistant_id: str | None, file_id: str | None) → AssistantFilesResponse

指定file_id和assistant_id，挂载File到对应的Assistant

* **参数:**
  * **assistant_id** (*Optional* *[**str* *]*) – 助理ID。
  * **file_id** (*Optional* *[**str* *]*) – 文件ID。
* **返回:**
  助理文件列表响应对象。
* **返回类型:**
  assistant_type.AssistantFilesResponse

#### mounted_files_list(assistant_id: str | None, limit: int | None = 20, order: str | None = 'desc', after: str | None = '', before: str | None = '') → AssistantMountedFilesListResponse

查询Assistant挂载的File列表

* **参数:**
  * **assistant_id** (*Optional* *[**str* *]*) – 助手ID，为空时获取当前登录用户的助手文件列表。
  * **limit** (*Optional* *[**int* *]* *,* *optional*) – 每页最多显示多少个文件。默认为20。
  * **order** (*Optional* *[**AssistantListRole* *]* *,* *optional*) – 文件列表排序方式。可选值为 ‘asc’ 或 ‘desc’。默认为 ‘desc’。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 返回文件ID大于该值的文件列表。默认为空字符串。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 返回文件ID小于该值的文件列表。默认为空字符串。
* **返回:**
  包含文件列表信息的响应对象。
* **返回类型:**
  assistant_type.AssistantFilesListResponse

#### query(assistant_id: str | None) → AssistantQueryResponse

根据assistant_id查询Assistant信息

* **参数:**
  **assistant_id** (*Optional* *[**str* *]*) – 助手ID
* **返回:**
  助手查询响应结果
* **返回类型:**
  assistant_type.AssistantQueryResponse
* **抛出:**
  **HTTPError** – 请求失败，抛出HTTPError异常

#### unmount_files(assistant_id: str | None, file_id: str | None) → AssistantFilesDeleteResponse

指定assistant_id和file_id，解绑Assistant中对应File的关联

* **参数:**
  * **assistant_id** (*Optional* *[**str* *]*) – 助理ID。
  * **file_id** (*Optional* *[**str* *]*) – 文件ID。
* **返回:**
  响应对象。
* **返回类型:**
  assistant_type.AssistantFilesDeleteResponse

#### update(assistant_id: str, model: str | None, name: str | None, description: str | None, instructions: str | None = '', tools: list[AssistantTool] | None = [], thought_instructions: str | None = '', chat_instructions: str | None = '', response_format: str | None = 'text', file_ids: list[str] | None = [], metadata: dict | None = {}) → AssistantUpdateResponse

根据assistant_id修改一个已创建的Assistant

* **参数:**
  * **assistant_id** (*str*) – 助手ID。
  * **model** (*Optional* *[**str* *]*) – 助手模型。
  * **name** (*Optional* *[**str* *]*) – 助手名称。
  * **description** (*Optional* *[**str* *]*) – 助手描述。
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 响应格式。默认为None。
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 助手指令。默认为None。
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思考指令。默认为None。
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 聊天指令。默认为None。
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 助手工具列表。默认为空列表。
  * **file_ids** (*Optional* *[**list* *[**str* *]* *]* *,* *optional*) – 文件ID列表。默认为空列表。
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 助手元数据。默认为空字典。
* **返回:**
  助手更新响应。
* **返回类型:**
  assistant_type.AssistantUpdateResponse

## appbuilder.core.assistant.assistants.files module

### *class* appbuilder.core.assistant.assistants.files.Files

基类：`object`

#### content(file_id: str, timeout: int | None = None)

获取指定文件的内容

* **参数:**
  * **file_id** (*str*) – 文件ID
  * **timeout** (*Optional* *[**int* *]* *,* *optional*) – 请求超时时间，单位秒. Defaults to None.
* **返回:**
  包含文件内容的响应对象
* **返回类型:**
  assistant_type.AssistantFilesContentResponse
* **抛出:**
  * **TypeError** – 当file_id不是字符串类型时引发此异常
  * **FileNotFoundError** – 当指定的文件路径不存在时引发此异常
  * **HTTPConnectionException** – 当请求失败时引发此异常

#### create(file_path: str, purpose: str = 'assistant') → AssistantFilesCreateResponse

上传文件到助理存储中。

* **参数:**
  * **file_path** (*str*) – 要上传的文件路径。
  * **purpose** (*str* *,* *optional*) – 上传文件的用途。默认为 “assistant”。
* **返回:**
  上传文件后返回的响应对象。
* **返回类型:**
  assistant_type.AssistantFilesCreateResponse
* **抛出:**
  **ValueError** – 如果指定的文件路径不存在，则会引发此异常。

#### delete(file_id: str) → AssistantFilesDeleteResponse

删除文件

* **参数:**
  **file_id** (*str*) – 文件ID
* **返回:**
  删除文件后的响应对象。
* **返回类型:**
  assistant_type.AssistantFilesDeleteResponse
* **抛出:**
  **无** – 

#### download(file_id: str, file_path: str = '', timeout: int | None = None)

下载文件

* **参数:**
  * **file_id** (*str*) – 文件ID
  * **file_path** (*str* *,* *optional*) – 文件保存路径，默认为空字符串。如果未指定，则使用文件名的默认值。要求若文件路径不为空，需要以/结尾。
  * **timeout** (*Optional* *[**int* *]* *,* *optional*) – 请求超时时间，单位秒。如果未指定，则使用默认超时时间。
* **返回:**
  None
* **抛出:**
  * **TypeError** – 当file_path或file_id类型不为str时引发此异常。
  * **ValueError** – 当file_id为空或None时，或file_path不是文件目录时引发此异常。
  * **FileNotFoundError** – 当指定的文件路径或文件不存在时引发此异常。
  * **OSError** – 当磁盘空间不足时引发此异常。
  * **HTTPConnectionException** – 当请求失败时引发此异常。
  * **Exception** – 当发生其他异常时引发此异常。

#### list() → AssistantFilesListResponse

列出存储中的文件列表。

此方法向存储服务发送请求，获取已上传的文件列表。返回的文件列表包含每个文件的详细信息，
包括文件ID、大小、用途、审核状态、创建时间、文件名、文件分类ID等。

* **参数:**
  **无**
* **返回:**
  文件列表的响应对象，包含以下属性：
  - object (str): 表示对象类型，默认值为 “list”
  - data (list[AssistantFilesListData]): 包含文件信息的列表，列表中的每个元素为 AssistantFilesListData 对象。该对象包含以下属性：
    > - id (str): 文件ID
    > - bytes (int): 文件大小（字节）
    > - object (str): 文件对象标识
    > - purpose (str): 文件用途
    > - censored (AuditStatus): 文件的审核状态
    > - create_at (int): 文件创建时间戳
    > - filename (str): 文件名
    > - classification_id (str): 文件分类ID
    > - file_type (str): 文件类型
* **返回类型:**
  assistant_type.AssistantFilesListResponse
* **抛出:**
  **assistant_type.AssistantError** – 请求发生错误时抛出，具体错误信息可通过 error_msg 属性获取。

#### query(file_id: str) → AssistantFilesQueryResponse

根据文件ID查询文件信息

* **参数:**
  **file_id** (*str*) – 文件ID
* **返回:**
  文件查询响应对象
* **返回类型:**
  assistant_type.AssistantFilesQueryResponse
* **抛出:**
  * **TypeError** – 如果file_id不是str类型
  * **ValueError** – 如果file_id不存在
