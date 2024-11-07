# appbuilder.core package

## Subpackages

* [appbuilder.core.assistant package](appbuilder.core.assistant.md)
  * [Subpackages](appbuilder.core.assistant.md#subpackages)
  * [Submodules](appbuilder.core.assistant.md#submodules)
* [appbuilder.core.components package](appbuilder.core.components.md)
  * [Subpackages](appbuilder.core.components.md#subpackages)
* [appbuilder.core.console package](appbuilder.core.console.md)
  * [Subpackages](appbuilder.core.console.md#subpackages)
  * [Submodules](appbuilder.core.console.md#submodules)

## Submodules

## appbuilder.core.agent module

### *class* appbuilder.core.agent.AgentRuntime(\*, component: [Component](#appbuilder.core.component.Component), user_session_config: Any | str | None = None, user_session: Any | None = None, tool_choice: ToolChoice = None)

基类：`BaseModel`

AgentRuntime 是对组件调用的服务化封装，开发者不是必须要用 AgentRuntime 才能运行自己的组件服务。
但 AgentRuntime 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。
此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。

* **参数:**
  * **component** ([*Component*](#appbuilder.core.component.Component)) – 可运行的 Component, 需要实现 run(message, stream, args) 方法
  * **user_session_config** (*sqlalchemy.engine.URL* *|**str* *|**None*) – Session 输出存储配置字符串。默认使用 sqlite:///user_session.db
    遵循 sqlalchemy 后端定义，参考文档：https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
  * **tool_choice** (*ToolChoice*) – 可用于Agent强制执行的组件工具

### 示例

```python
import os
import sys
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
agent = appbuilder.AgentRuntime(component=component)
message = appbuilder.Message({"query": "你好"})
print(agent.chat(message, stream=False))
```

```python
import os
import sys
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
user_session_config = "sqlite:///foo.db"
agent = appbuilder.AgentRuntime(
    component=component, user_session_config=user_session_config)
agent.serve(debug=False, port=8091)
```

```python
import os
import sys
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
agent = appbuilder.AgentRuntime(component=component)
agent.chainlit_demo(port=8091)
```

Session 数据管理 : 除去上述简单应用外，还支持 Session 数据管理，下面是一个例子

```python
import os
import sys
from appbuilder.core.component import Component
from appbuilder import (
    AgentRuntime, UserSession, Message, QueryRewrite, Playground,
)

os.environ["APPBUILDER_TOKEN"] = '...'

class PlaygroundWithHistory(Component):
    def __init__(self):
        super().__init__()
        self.query_rewrite = QueryRewrite(model="Qianfan-Agent-Speed-8k")
        self.play = Playground(
            prompt_template="{query}",
            model="eb-4"
        )

    def run(self, message: Message, stream: bool=False):
        user_session = UserSession()
        # 获取 Session 历史数据
        history_queries = user_session.get_history("query", limit=1)
        history_answers = user_session.get_history("answer", limit=1)

        if history_queries and history_answers:
            history = []
            for query, answer in zip(history_queries, history_answers):
                history.extend([query.content, answer.content])
            logging.info(f"history: {history}")
            message = self.query_rewrite(
                Message(history + [message.content]), rewrite_type="带机器人回复")
        logging.info(f"message: {message}")
        answer = self.play.run(message, stream)
        # 保存本轮数据
        user_session.append({
            "query": message,
            "answer": answer,
        })
        return answer

agent = AgentRuntime(component=PlaygroundWithHistory())
agent.chainlit_demo(port=8091)
```

请求时认证 : component在创建时可以不进行认证，由AgentRuntime服务化后带入AppbuilderToken

```python
import appbuilder

component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4",
    lazy_certification=True, # 在创建时不进行认证
)
agent = appbuilder.AgentRuntime(component=component)
agent.serve(debug=False, port=8091)
```

```shell
curl --location 'http://0.0.0.0:8091/chat' \
    --header 'Content-Type: application/json' \
    --header 'X-Appbuilder-Token: ...' \
    --data '{
        "message": "你是谁",
        "stream": false
    }'
```

Session 信息查看 : 查看本地user_session.db数据库内部信息，下面是一个例子

```python
import sqlite3
import json

# 连接到 SQLite 数据库
# 如果文件不存在，会自动在当前目录创建:
user_session_path = 'your_user_session.db地址'
conn = sqlite3.connect(user_session_path)
cursor = conn.cursor()

# 执行一条 SQL 语句，列出所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# 查询appbuilder_session_messages表的列信息
cursor.execute("PRAGMA table_info(appbuilder_session_messages);")
columns_info = cursor.fetchall()

column_names = [info[1] for info in columns_info]  # info[1]是列名的位置
for column_name in column_names:
    print(column_name)

# 查询特定表中的数据
cursor.execute("SELECT message_value FROM appbuilder_session_messages;")
for row in cursor.fetchall():
    print(json.loads(row[0]))

# 关闭 Connection:
conn.close()
```

#### *class* Config

基类：`object`

检查配置

#### extra

额外属性，默认为 Extra.forbid，即禁止添加任何额外的属性

* **Type:**
  Extra

#### arbitrary_types_allowed

任意类型是否允许，默认为 True

* **Type:**
  bool

#### arbitrary_types_allowed *= True*

#### extra *= 'forbid'*

#### chainlit_agent(host='0.0.0.0', port=8091)

将 appbuilder client 服务化，提供 chainlit demo 页面

* **参数:**
  * **host** (*str*) – 服务 host
  * **port** (*int*) – 服务 port
* **返回:**
  None

#### chainlit_demo(host='0.0.0.0', port=8091)

将 component 服务化，提供 chainlit demo 页面

* **参数:**
  * **host** (*str*) – 服务 host
  * **port** (*int*) – 服务 port
* **返回:**
  None

#### chat(message: [Message](#appbuilder.core.message.Message), stream: bool = False, \*\*args) → [Message](#appbuilder.core.message.Message)

执行一次对话

* **参数:**
  * **message** ([*Message*](#appbuilder.core.message.Message)) – 该次对话用户输入的 Message
  * **stream** (*bool*) – 是否流式请求
  * **\*\*args** – 其他参数，会被透传到 component
* **返回:**
  返回的 Message
* **返回类型:**
  [Message](#appbuilder.core.message.Message)([Message](#appbuilder.core.message.Message))

#### component *: [Component](#appbuilder.core.component.Component)*

#### create_flask_app(url_rule='/chat')

创建 Flask 应用，主要用于 Gunicorn 这样的 WSGI 服务器来运行服务。

* **参数:**
  **None**
* **返回:**
  Flask

#### *classmethod* init(values: Dict) → Dict

初始化 AgentRuntime，UserSession 会在这里被初始化

* **参数:**
  **values** (*Dict*) – 初始化参数
* **返回:**
  None

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'arbitrary_types_allowed': True, 'extra': 'forbid'}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'component': FieldInfo(annotation=Component, required=True), 'tool_choice': FieldInfo(annotation=ToolChoice, required=False), 'user_session': FieldInfo(annotation=Union[Any, NoneType], required=False), 'user_session_config': FieldInfo(annotation=Union[Any, str, NoneType], required=False)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### prepare_chainlit_readme()

准备 Chainlit 的 README 文件

* **参数:**
  **无**
* **返回:**
  无
* **抛出:**
  **无** – 

说明:
: 从 utils 文件夹中拷贝 chainlit.md 文件到当前工作目录下，如果当前工作目录下已存在 chainlit.md 文件，则不拷贝。

#### serve(host='0.0.0.0', debug=True, port=8092, url_rule='/chat')

将 component 服务化，提供 Flask http API 接口

* **参数:**
  * **host** (*str*) – 服务运行的host地址，默认为’0.0.0.0’
  * **debug** (*bool*) – 是否开启debug模式，默认为True
  * **port** (*int*) – 服务运行的端口号，默认为8092
  * **url_rule** (*str*) – 服务的URL规则，默认为”/chat”
* **返回:**
  None

#### tool_choice *: ToolChoice*

#### user_session *: Any | None*

#### user_session_config *: Any | str | None*

## appbuilder.core.message module

### *class* appbuilder.core.message.Message(content: \_T | None = None, \*, name: str | None = 'msg', mtype: str | None = 'dict', id: str | None = '88caf1fe-da8b-4dfb-a87c-32e88df1d5cb', \*\*data)

基类：`BaseModel`, `Generic`[`_T`]

Message class

#### content

The message content

* **Type:**
  appbuilder.core.message._T | None

#### name

The message name

* **Type:**
  str | None

#### mtype

The message type

* **Type:**
  str | None

#### id

The message id

* **Type:**
  str | None

#### content *: \_T | None*

#### id *: str | None*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'allow'}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'content': FieldInfo(annotation=Union[~_T, NoneType], required=False, default={}), 'id': FieldInfo(annotation=Union[str, NoneType], required=False, default='88caf1fe-da8b-4dfb-a87c-32e88df1d5cb'), 'mtype': FieldInfo(annotation=Union[str, NoneType], required=False, default='dict'), 'name': FieldInfo(annotation=Union[str, NoneType], required=False, default='msg')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### mtype *: str | None*

#### name *: str | None*

## appbuilder.core.component module

<a id="module-appbuilder.core.component"></a>

Component模块包括组件基类，用户自定义组件需要继承Component类，并至少实现run方法

### *class* appbuilder.core.component.Component(meta: [ComponentArguments](#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`object`

Component基类, 其它实现的Component子类需要继承该基类，并至少实现run方法.

* **参数:**
  * **meta** ([*ComponentArguments*](#appbuilder.core.component.ComponentArguments)) – component meta information.
  * **secret_key** (*str*) – user authentication token.
  * **gateway** (*str*) – backend gateway server address.
  * **lazy_certification** (*bool*) – lazy certification flag.

#### *async* abatch(\*args, \*\*kwargs) → List[[Message](#appbuilder.core.message.Message)]

abatch method,待子类重写实现

* **参数:**
  * **args** – list of arguments
  * **kwargs** – keyword arguments

#### *async* arun(\*args, \*\*kwargs) → [Message](#appbuilder.core.message.Message) | None

arun method,待子类重写实现

* **参数:**
  * **args** – list of arguments
  * **kwargs** – keyword arguments

#### batch(\*args, \*\*kwargs) → List[[Message](#appbuilder.core.message.Message)]

batch method,待子类重写实现

* **参数:**
  * **args** – list of arguments
  * **kwargs** – keyword arguments

#### create_langchain_tool(tool_name='', \*\*kwargs)

create_langchain_tool method,将AB-SDK的Tool转换为LangChain的StructuredTool

* **参数:**
  * **tool_name** – string, optional, default is empty string
  * **kwargs** – keyword arguments
* **返回:**
  StructuredTool

#### *property* http_client

获取 HTTP 客户端实例。

* **参数:**
  **无**
* **返回:**
  HTTP 客户端实例。
* **返回类型:**
  HTTPClient

#### manifests *= []*

#### run(\*inputs, \*\*kwargs)

run method,待子类重写实现

* **参数:**
  * **inputs** – list of arguments
  * **kwargs** – keyword arguments

#### set_secret_key_and_gateway(secret_key: str | None = None, gateway: str = '')

设置密钥和网关地址。

* **参数:**
  * **secret_key** (*Optional* *[**str* *]* *,* *optional*) – 密钥，默认为None。如果未指定，则使用实例当前的密钥。
  * **gateway** (*str* *,* *optional*) – 网关地址，默认为空字符串。如果未指定，则使用实例当前的网关地址。
* **返回:**
  None

#### tool_desc() → List[str]

tool_desc method,待子类重写实现

* **参数:**
  **None**
* **返回:**
  list of strings

#### tool_eval(\*\*kwargs)

tool_eval method,待子类重写实现

* **参数:**
  **kwargs** – keyword arguments

#### tool_name() → List[str]

tool_name method,待子类重写实现

* **参数:**
  **None**
* **返回:**
  list of strings

### *class* appbuilder.core.component.ComponentArguments(\*, name: str = '', tool_desc: Dict[str, Any] = {})

基类：`BaseModel`

ComponentArguments define Component meta fields

#### name

component name.

* **Type:**
  str

#### tool_desc

component description.

* **Type:**
  dict

#### extract_values_to_dict()

extract ComponentArguments fields to dict

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'name': FieldInfo(annotation=str, required=False, default=''), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### name *: str*

#### tool_desc *: Dict[str, Any]*
