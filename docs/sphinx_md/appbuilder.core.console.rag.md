# appbuilder.core.console.rag package

## Submodules

## appbuilder.core.console.rag.rag module

### *class* appbuilder.core.console.rag.rag.RAG(app_id: str = '')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

console RAG组件，利用console端RAG应用进行问答

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

#### *property* http_client

#### integrated_url *: str* *= '/v1/ai_engine/agi_platform/v1/instance/integrated'*

#### name *= 'rag'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message), conversation_id: str = '', stream: bool = False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

RAG问答

* **参数:**
  * **query** – 用户输入的文本
  * **stream** – 是否开启流式模式
  * **conversation_id** – 会话ID，不传表示新建对话
* **返回:**
  rag答案
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
