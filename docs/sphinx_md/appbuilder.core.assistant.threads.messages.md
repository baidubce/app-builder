# appbuilder.core.assistant.threads.messages package

## Submodules

## appbuilder.core.assistant.threads.messages.messages module

### *class* appbuilder.core.assistant.threads.messages.messages.Messages

基类：`object`

#### create(thread_id: str, content: str, role: str | None = 'user', file_ids: list[str] | None = []) → AssistantMessageCreateResponse

创建一条消息。

* **参数:**
  * **thread_id** (*str*) – 线程ID。
  * **content** (*str*) – 消息内容。
  * **role** (*Optional* *[**str* *]* *,* *optional*) – 角色，可选值为”user”或”assistant”。默认为”user”。
  * **file_ids** (*Optional* *[**list* *[**str* *]* *]* *,* *optional*) – 消息中包含的文件ID列表。默认为空列表。
* **返回:**
  消息创建响应对象。
* **返回类型:**
  thread_type.AssistantMessageCreateResponse
* **抛出:**
  **HttpError** – 如果请求失败，则抛出HttpError异常。

#### files(thread_id: str, message_id: str, limit: int | None = 20, order: str | None = 'desc', after: str | None = '', before: str | None = '') → AssistantMessageFilesResponse

获取指定消息 ID 的附件信息。

* **参数:**
  * **thread_id** (*str*) – 线程 ID。
  * **messsages_id** (*str*) – 消息 ID。
  * **limit** (*Optional* *[**int* *]* *,* *optional*) – 返回结果的最大数量，默认为 20。
  * **order** (*Optional* *[**str* *]* *,* *optional*) – 排序方式，可选值为 “asc” 或 “desc”，默认为 “desc”。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 返回结果的时间范围，只返回时间晚于该时间戳的消息附件，默认为空。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 返回结果的时间范围，只返回时间早于该时间戳的消息附件，默认为空。
* **返回:**
  附件信息响应对象。
* **返回类型:**
  thread_type.AssistantMessageFilesResponse

#### list(thread_id: str, limit: int = 20, order: str = 'desc', after: str = '', before: str = '') → AssistantMessageListResponse

查询指定Thread下的Message列表

* **参数:**
  * **thread_id** (*str*) – 线程ID。
  * **limit** (*int* *,* *optional*) – 返回消息的最大数量，取值范围为[1,20]。默认为-20。
  * **order** (*Optional* *[**str* *]* *,* *optional*) – 排序方式，可选值为”asc”或”desc”。默认为”desc”。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 查询指定message_id之后创建的Message。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 查询指定message_id之前创建的Message
* **返回:**
  查询thread下的message列表响应对象。
* **返回类型:**
  thread_type.AssistantMessageListResponse
* **抛出:**
  **HttpError** – 如果请求失败，则抛出HttpError异常。

#### query(thread_id: str, message_id: str) → AssistantMessageQueryResponse

根据message_id查询指定Message的信息

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **message_id** (*str*) – 消息ID
* **返回:**
  消息信息响应
* **返回类型:**
  thread_type.AssistantMessageQueryResponse
* **抛出:**
  **HttpError** – 如果请求失败，则抛出HttpError异常。

#### update(thread_id: str, message_id: str, content: str | None, file_ids: list[str] | None = []) → AssistantMessageUpdateResponse

修改Message对象，允许content和file_ids字段

* **参数:**
  * **thread_id** (*str*) – 线程ID。
  * **message_id** (*str*) – 消息ID。
  * **content** (*Optional* *[**str* *]* *,* *optional*) – 消息内容。默认为空字符串。
  * **file_ids** (*Optional* *[**list* *[**str* *]* *]* *,* *optional*) – 消息中包含的文件ID列表。默认为空列表。
* **返回:**
  消息更新响应对象。
* **返回类型:**
  thread_type.AssistantMessageUpdateResponse
* **抛出:**
  **HttpError** – 如果请求失败，则抛出HttpError异常。
