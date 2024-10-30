# `AgentRuntime`类

## 简介

AgentRuntime 是对组件调用的服务化封装，开发者不是必须要用 AgentRuntime 才能运行自己的组件服务。但 AgentRuntime 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。


## Python基本用法

### 1、实例化`AgentRuntime() -> AgentRuntime`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| component | Component | 可运行的 Component,需要实现 run(message, stream, **args) 方法  | "正确的component组件或client" |
| user_session_config | sqlalchemy.engine.URL、str、None | Session 输出存储配置字符串。默认使用 sqlite:///user_session.db | "正确的存储配置字符串" |

#### 方法功能

返回一个调试 Agent 的服务

#### 示例代码

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
agent = appbuilder.AgentRuntime(component=component)
```

### 2、运行Agent服务`AgentRuntime.chat(message: Message, stream: bool = False, **args) -> Message`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| message | Message | 该次对话用户输入的 Message | "正确的Message" |
| stream | bool | 是否使用流式请求。默认为 False | False |

#### 方法功能

运行一个 Agent 服务，执行一次对话

#### 示例代码

```python
import os
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

### 3、提供 Flask http API 接口`AgentRuntime.serve(self, host='0.0.0.0', debug=True, port=8092, url_rule="/chat"`

#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| host | String | 服务主机地址，默认为 '0.0.0.0' | '0.0.0.0' |
| debug | bool | 是否是调试模式，默认为 True | False |
| port | int | 服务端口号，默认为 8092 | 8092 |
| url_rule | String | Flask 路由规则，默认为 '/chat' | '/chat' |

#### 方法功能

将 component 服务化，提供 Flask http API 接口

#### 示例代码

```python
import os
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


### 4、提供 chainlit demo 页面`AgentRuntime.chainlit_demo(host='0.0.0.0', port=8091)`


#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| host | string | 服务主机地址，默认为 '0.0.0.0' | "0.0.0.0" |
| port | int | 服务端口号，默认为 8092 | 8091 |

#### 方法功能

将 component 服务化，提供 chainlit demo 页面

#### 示例代码

```python
import os
import logging
from appbuilder.core.component import Component
from appbuilder import (
    AgentRuntime, UserSession, Message, QueryRewrite, Playground,
)
os.environ["APPBUILDER_TOKEN"] = 'YOUR_APPBUILDER_TOKEN'
class PlaygroundWithHistory(Component):
    def __init__(self):
        super().__init__()
        self.query_rewrite = QueryRewrite(model="ERNIE Speed-AppBuilder")
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

### 5、将 appbuilder client 服务化，提供 chainlit demo 页面`AgentRuntime.chainlit_agent(host='0.0.0.0', port=8091)`


#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| host | string | 服务主机地址，默认为 '0.0.0.0' | "0.0.0.0" |
| port | int | 服务端口号，默认为 8092 | 8091 |

#### 方法返回值

将 appbuilder client 服务化，提供 chainlit demo 页面

#### 示例代码

```python
import appbuilder
import os

os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AppBuilder应用ID，可在console端查看
builder = appbuilder.AppBuilderClient(app_id)
conversation_id = builder.create_conversation()
agent = appbuilder.AgentRuntime(component=builder)
message = appbuilder.Message({"query": "北京今天天气怎么样"})
print(agent.chat(message, stream=False))
```