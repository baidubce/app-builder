# appbuilder.core.console.rag package

## Submodules

## appbuilder.core.console.rag.rag module

### *class* appbuilder.core.console.rag.rag.RAG(app_id: str = '')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

console RAG组件，利用console端RAG应用进行问答，即将上线

Examples:

```python
import appbuilder
import os

os.environ["APPBUILDER_TOKEN"] = '...'
conversation_id = '...'
app_id = '...' # 线上知识库ID
conversation_id = '...' # 会话ID，可选参数，不传默认新建会话
rag_app = appbuilder.console.RAG(app_id)
query = "中国的首都在哪里"
answer = rag_app.run(appbuilder.Message(query)) # 新建会话
print(answer)
conversation_id = answer.conversation_id # 获取会话ID，可用于下次会话
print(conversation_id)
query = "它有哪些旅游景点"
answer = rag_app.run(appbuilder.Message(query), conversation_id) # 接上次会话
print(answer.content)
print(answer.extra)  # 获取结果来源
```

#### debug(query: [Message](appbuilder.core.md#appbuilder.core.message.Message))

调试函数(RAG暂时无DEBUG服务)

* **参数:**
  **query** ([*Message*](appbuilder.md#appbuilder.Message)) – 待调试的消息对象
* **返回:**
  None

说明:
: 这是一个用于调试的函数，接收一个消息对象作为参数，但并不返回任何值。
  你可以在这里添加任何用于调试的代码，比如打印日志或输出消息内容等。

#### *property* http_client

获取HTTP客户端对象。

* **参数:**
  **无参数**
* **返回:**
  返回HTTPClient对象，如果尚未创建则创建新对象。
* **返回类型:**
  HTTPClient

#### integrated_url *: str* *= '/v1/ai_engine/agi_platform/v1/instance/integrated'*

#### name *= 'rag'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message), conversation_id: str = '', stream: bool = False)

RAG问答

* **参数:**
  * **query** ([*Message*](appbuilder.md#appbuilder.Message)) – 用户输入的文本
  * **conversation_id** (*str* *,* *optional*) – 会话ID，默认为空字符串，表示新建对话。
  * **stream** (*bool* *,* *optional*) – 是否开启流式模式，默认为False。
* **返回:**
  RAG问答的答案
* **返回类型:**
  [Message](appbuilder.md#appbuilder.Message)

## Module contents
