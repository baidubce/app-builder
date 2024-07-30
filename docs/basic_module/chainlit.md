## 基础组件基于Chainlit提供交互式前端页面

## 交互式前端基本用法

### `AgentRuntime`


#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| component | Component | 可运行的 Component,需要实现 run(message, stream, **args) 方法  | "正确的component组件或client" |
| user_session_config | sqlalchemy.engine.URL、str、None | Session 输出存储配置字符串。默认使用 sqlite:///user_session.db | "正确的存储配置字符串" |

#### 方法返回值

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


### `AgentRuntime.chat(message: Message, stream: bool = False, **args) -> Message`


#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| message | Message | Agent的运行传入参数 | "正确的Message" |
| stream | bool | 设置Agent是否流式运行 | False |

#### 方法返回值

运行一个调试 Agent 的服务

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


### `AgentRuntime.chainlit_demo(host='0.0.0.0', port=8091)`


#### 方法参数

| 参数名称   | 参数类型   | 描述         | 示例值       |
|--------|--------|------------|-----------|
| host | string | host地址 | "0.0.0.0" |
| port | int | post接口 | 8091 |

#### 方法返回值

运行一个调试 Agent 的服务

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

### 通过user_session.db数据库查看历史对话信息

#### 示例代码

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