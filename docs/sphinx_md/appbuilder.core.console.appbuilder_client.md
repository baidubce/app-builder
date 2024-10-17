# appbuilder.core.console.appbuilder_client package

## Submodules

## appbuilder.core.console.appbuilder_client.appbuilder_client module

AppBuilderClient组件

### *class* appbuilder.core.console.appbuilder_client.appbuilder_client.AgentBuilder(app_id: str)

基类：[`AppBuilderClient`](#appbuilder.core.console.appbuilder_client.appbuilder_client.AppBuilderClient)

AgentBuilder是继承自AppBuilderClient的一个子类，用于构建和管理智能体应用。
支持调用在[百度智能云千帆AppBuilder]([https://cloud.baidu.com/product/AppBuilder](https://cloud.baidu.com/product/AppBuilder))平台上
构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'
# 可在Console 应用页面获取
app_id = "app_id"
client = appbuilder.AppBuilderClient("app_id")
conversation_id = client.create_conversation()
file_id = client.upload_local_file(conversation_id, "/path/to/file")
message = client.run(conversation_id, "今天你好吗？")
# 打印对话结果
print(message.content)
```

### *class* appbuilder.core.console.appbuilder_client.appbuilder_client.AppBuilderClient(app_id: str, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

AppBuilderClient 组件支持调用在[百度智能云千帆AppBuilder]([https://cloud.baidu.com/product/AppBuilder](https://cloud.baidu.com/product/AppBuilder))平台上
构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'
# 可在Console 应用页面获取
app_id = "app_id"
client = appbuilder.AppBuilderClient("app_id")
conversation_id = client.create_conversation()
file_id = client.upload_local_file(conversation_id, "/path/to/file")
message = client.run(conversation_id, "今天你好吗？")
# 打印对话结果
print(message.content)
```

#### create_conversation() → str

创建会话并返回会话ID

会话ID在服务端用于上下文管理、绑定会话文档等，如需开始新的会话，请创建并使用新的会话ID

* **参数:**
  **无**
* **返回:**
  唯一会话ID
* **返回类型:**
  response (str)

#### run(conversation_id: str, query: str = '', file_ids: list = [], stream: bool = False, tools: list[Tool] = None, tool_outputs: list[ToolOutput] = None, tool_choice: ToolChoice = None, end_user_id: str = None, \*\*kwargs) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

运行智能体应用

* **参数:**
  * **query** (*str*) – query内容
  * **conversation_id** (*str*) – 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
  * **file_ids** (*list* *[**str* *]*) – 文件ID列表
  * **stream** (*bool*) – 为True时，流式返回，需要将message.content.answer拼接起来才是完整的回答；为False时，对应非流式返回
  * **tools** (*list* *[**data_class.Tools* *]*) – 一个Tools组成的列表，其中每个Tools对应一个工具的配置, 默认为None
  * **tool_outputs** (*list* *[**data_class.ToolOutput* *]*) – 工具输出列表，格式为list[ToolOutput], ToolOutputd内容为本地的工具执行结果，以自然语言/json dump str描述，默认为None
  * **tool_choice** (*data_class.ToolChoice*) – 控制大模型使用组件的方式，默认为None
  * **end_user_id** (*str*) – 用户ID，用于区分不同用户
  * **kwargs** – 其他参数
* **返回:**
  Message): 对话结果，一个Message对象，使用message.content获取内容。
* **返回类型:**
  message (obj

#### run_with_handler(conversation_id: str, query: str = '', file_ids: list = [], tools: list[Tool] | None = None, stream: bool = False, event_handler=None, \*\*kwargs)

运行智能体应用，并通过事件处理器处理事件

* **参数:**
  * **conversation_id** (*str*) – 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
  * **query** (*str*) – 查询字符串
  * **file_ids** (*list*) – 文件ID列表
  * **tools** (*list* *[**data_class.Tools* *]* *,*  *可选*) – 一个Tools组成的列表，其中每个Tools对应一个工具的配置, 默认为None
  * **stream** (*bool*) – 是否流式响应
  * **event_handler** (*EventHandler*) – 事件处理器
  * **kwargs** – 其他参数
* **返回:**
  事件处理器
* **返回类型:**
  EventHandler

#### upload_local_file(conversation_id, local_file_path: str) → str

上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式

该接口用于在对话中上传文件供大模型处理，文件的有效期为7天并且不超过对话的有效期。一次只能上传一个文件。

* **参数:**
  * **conversation_id** (*str*) – 会话ID
  * **local_file_path** (*str*) – 本地文件路径
* **返回:**
  唯一文件ID
* **返回类型:**
  response (str)

### appbuilder.core.console.appbuilder_client.appbuilder_client.get_all_apps()

获取所有应用列表。

* **参数:**
  **无参数。**
* **返回:**
  包含所有应用信息的列表，每个元素为一个App对象，
  其中App对象的结构取决于get_app_list函数的返回结果。
* **返回类型:**
  List[App]

### appbuilder.core.console.appbuilder_client.appbuilder_client.get_app_list(limit: int = 10, after: str = '', before: str = '', secret_key: str | None = None, gateway_v2: str | None = None) → list[AppOverview]

该接口查询用户下状态为已发布的应用列表

* **参数:**
  * **limit** (*int* *,* *optional*) – 返回结果的最大数量，默认值为10。
  * **after** (*str* *,* *optional*) – 返回结果中第一个应用的游标值，用于分页查询。默认值为空字符串。
  * **before** (*str* *,* *optional*) – 返回结果中最后一个应用的游标值，用于分页查询。默认值为空字符串。
  * **secret_key** (*Optional* *[**str* *]* *,* *optional*) – 认证密钥。如果未指定，则使用默认的密钥。默认值为None。
  * **gateway_v2** (*Optional* *[**str* *]* *,* *optional*) – 网关地址。如果未指定，则使用默认的地址。默认值为None。
* **返回:**
  应用列表。
* **返回类型:**
  list[data_class.AppOverview]

## appbuilder.core.console.appbuilder_client.data_class module

### *class* appbuilder.core.console.appbuilder_client.event_handler.AppBuilderClientRunContext

基类：`object`

### *class* appbuilder.core.console.appbuilder_client.event_handler.AppBuilderEventHandler

基类：`object`

#### done(run_context, run_response)

#### error(run_context, run_response)

#### init(appbuilder_client, conversation_id, query, file_ids=None, tools=None, stream: bool = False, event_handler=None, \*\*kwargs)

初始化类实例并设置相关参数。

* **参数:**
  * **appbuilder_client** (*object*) – AppBuilder客户端实例对象。
  * **conversation_id** (*str*) – 对话ID。
  * **query** (*str*) – 用户输入的查询语句。
  * **file_ids** (*list* *,* *optional*) – 文件ID列表，默认为None。
  * **tools** (*list* *,* *optional*) – 工具列表，默认为None。
  * **stream** (*bool* *,* *optional*) – 是否使用流式处理，默认为False。
  * **event_handler** (*callable* *,* *optional*) – 事件处理函数，默认为None。
  * **\*\*kwargs** – 其他可选参数。
* **返回:**
  None

#### interrupt(run_context, run_response)

#### preparing(run_context, run_response)

#### reset_state()

重置该对象的状态，将所有实例变量设置为默认值。

* **参数:**
  **无**
* **返回:**
  无

#### running(run_context, run_response)

#### success(run_context, run_response)

#### until_done()

迭代并遍历内部迭代器中的所有元素，直到迭代器耗尽。

* **参数:**
  **无参数。**
* **返回:**
  无返回值。
