# AgentRuntime

## 简介
AgentRuntime 是对组件（Component）的服务化封装。

AgentRuntime 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。

## 功能介绍
1. 一键服务化组件: 使得组件能够以服务的形式运行，支持 API 调用和对话框交互。
2. Session 数据管理: 提供 Session 数据的管理功能，允许跟踪和存储用户会话数据。
3. 请求时鉴权: 支持在请求时进行认证，确保安全性。

## 使用依赖
AgentRuntime 服务化组件依赖 `appbuilder-sdk[serve]`，如果没有安装，可以执行下面的命令安装：

```shell
pip install 'appbuilder-sdk[serve]'
```

## 基本用法

### 快速开始

下面的示例会基于 Playground 组件，在 8091 端口部署 Web 服务: 

```python
import os
import appbuilder

# 使用组件之前，请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1、创建密钥
os.environ["APPBUILDER_TOKEN"] = '...'

component = appbuilder.Playground(
    prompt_template="{query}",
    model="ERNIE-Bot"
)

agent = appbuilder.AgentRuntime(component=component)
agent.serve(port=8091)
```

通过 Shell 命令测试启动的服务, 请求 Body 为组件 run 方法的入参: 

```shell
curl --location 'http://0.0.0.0:8091/chat' \
--header 'Content-Type: application/json' \
--data '{
    "message": "海淀区的面积是多少",
    "stream": false
}'
```

## AgentRuntime 参数说明

### 类初始化参数说明

AgentRuntime 初始化接受两个参数。

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
|--|--|--|--|--|
| component | Component | 是 | 可运行的 Component, 该 Component 需要实现 run(message, stream, **args) 方法。 | Playground(prompt_template="{query}", model="ERNIE-Bot") |
| user_session_config | sqlalchemy.engine.URL\|Str\|None | 否 | 会话 Session 数据存储的数据库配置，遵循 sqlalchemy 后端定义，可参考[文档](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)。默认使用 sqlite:///user_session.db，即本地的 SQLite 存储 | "sqlite:///user_session.db" |

### Web 服务 API 参数
API 通过 HTTP POST 进行请求。

#### 请求参数

**接口定义**

| URL | Method |
|--|--|
| /chat | POST |

**Header 参数**

| 参数名称 | 是否必须 | 描述 | 示例值 |
|--|--|--|--|
| Content-Type | 是 | 必须设置为"application/json" | "application/json" |
| X-Appbuilder-Token | 否 | 开启请求时认证能力时需要带入 APPBUILDER_TOKEN 进行鉴权 | 前往千帆AppBuilder官网创建密钥，流程详见[文档](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1、创建密钥) |

**Body 参数**

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
|--|--|--|--|--|
| message | Any | 是 | 透传到 component 的 run 方法的 message 参数 | "海淀区的面积是多少" |
| stream | Bool | 否 | 是否流式调用。透传到 component 的 run 方法的 stream 参数。默认为 false | false |
| session_id | Str | 否 | 用于标示同一个会话（Session）。如果不传该值，后端会自动生成 session_id，在响应参数中返回 | "99680089-5acb-4298-9ade-a1a3f6c28102" |
| 其他参数 | Any | 否 | 透传到 component 的 run 方法 | - |


#### 响应参数
分为非流式响应和流式响应。

**非流式响应**

| 参数名称 | 参数类型 | 描述 | 示例值 |
|--|--|--|--|
| code | Int | 错误码。值为0表示成功，否则为失败。非0错误详见错误码部分描述 | 0 |
| message | Str | 错误信息描述。 | "Missing input variable query in message ['海淀区的面积是多少']" |
| result | Object | 请求结果 | - |
| + answer_message | Object | 组件返回值，由返回的 Message 序列化得到 | {"content":"海淀区是北京市的一个区，位于北京市主城区西部和西北部，东与西城区、朝阳区相邻，南与丰台区毗连，西与石景山区、门头沟区交界，北与昌平区接壤。海淀区的面积为**431平方千米**，约占北京市总面积的2.6%。","extra":{},"id":"6b4e5019-a708-4bc5-a6ec-595fb4285677","mtype":"dict","name":"msg"} |
| + session_id | Str | 用于标示同一个会话（Session） | "99680089-5acb-4298-9ade-a1a3f6c28102" |

**流式响应**

流式数据以追加的形式返回。流式和非流式的数据结构一致，不再描述。

#### 响应示例

分为非流式响应和流式响应。

**非流式响应**

```shell
{
  "code": 0,
  "message": "",
  "result": {
    "answer_message": {
      "content": "海淀区是北京市的一个区，位于北京市主城区西部和西北部，东与西城区、朝阳区相邻，南与丰台区毗连，西与石景山区、门头沟区交界，北与昌平区接壤。海淀区的面积为**431平方千米**，约占北京市总面积的2.6%。",
      "extra": {},
      "id": "6b4e5019-a708-4bc5-a6ec-595fb4285677",
      "mtype": "dict",
      "name": "msg"
    },
    "session_id": "99680089-5acb-4298-9ade-a1a3f6c28102"
  }
}
```

**流式响应**

```shell
data: {"code": 0, "message": "", "result": {"session_id": "663303a9-d83d-481f-a084-872ece87989c", "answer_message": {"content": "海淀区", "extra": {}}}}

data: {"code": 0, "message": "", "result": {"session_id": "663303a9-d83d-481f-a084-872ece87989c", "answer_message": {"content": "，隶属于北京市，位于北京市主城区西部和西北部，东与西城区、朝阳区相邻，南与丰台区毗连，", "extra": {}}}}

data: {"code": 0, "message": "", "result": {"session_id": "663303a9-d83d-481f-a084-872ece87989c", "answer_message": {"content": "西与石景山区、门头沟区交界，北与昌平区接壤，总面积**431平方千米**。", "extra": {}}}}

data: {"code": 0, "message": "", "result": {"session_id": "663303a9-d83d-481f-a084-872ece87989c", "answer_message": {"content": "", "extra": {}}}}
```

#### 错误码
| 错误码 | 描述 |
|--|--|
| 400 | 客户端请求参数错误 |
| 1000 | 服务端执行错误 |


## 高级用法

### 一键服务化组件 
AgentRuntime 可以快速组件以服务的形式运行，支持 API 调用和对话框交互。

API 调用在快速开始小结已经给出，这里介绍基于 chainlit 的对话框交互方式。基于 chainlit 的对话框交互要求被服务化的组件的 message 参数能够接受 Str 的基础类型。

执行下面的代码，会启动一个 chainlit 页面，页面地址：0.0.0.0:8091

```python
import os
import appbuilder

# 使用组件之前，请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1、创建密钥
os.environ["APPBUILDER_TOKEN"] = '...'

component = appbuilder.Playground(
    prompt_template="{query}",
    model="ERNIE-Bot"
)

agent = appbuilder.AgentRuntime(component=component)
agent.chainlit_demo(port=8091)
```


### Session 数据管理
AgentRuntime 提供 Session 数据的管理功能，允许跟踪和存储用户会话数据。一般只有在二次开发的组件需要使用该能力。

**二次开发组件**

二次开发的组件需要重写组件的 run(message, stream, **args)方法，并且至少需要有 message 和 stream 两个参数。

下面基于 QueryRewrite 和 Playground 两个组件，开发 PlaygroundWithHistory 组件，该组件需要对会话数据进行操作。

当使用 Component 独立运行时，会话数据会被存储于内存。

```python
import os
import logging
from appbuilder.core.component import Component
from appbuilder import (
    AgentRuntime, UserSession, Message, QueryRewrite, Playground,
)

# 使用组件之前，请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1、创建密钥
os.environ["APPBUILDER_TOKEN"] = '...'

class PlaygroundWithHistory(Component):
    def __init__(self):
        super().__init__()
        self.query_rewrite = QueryRewrite(model="EB-turbo-AppBuilder专用版")
        self.playground = Playground(
            prompt_template="{query}",
            model="ERNIE-Bot"
        )

    def run(self, message: Message, stream: bool=False):
        user_session = UserSession()
        # 获取 Session 历史数据
        history_queries = user_session.get_history("query", limit=1)
        history_answers = user_session.get_history("answer", limit=1)

        # query 改写
        if history_queries and history_answers:
            history = []
            for query, answer in zip(history_queries, history_answers):
                history.extend([query.content, answer.content])
            logging.info(f"history: {history}")
            message = self.query_rewrite(
                Message(history + [message.content]), rewrite_type="带机器人回复")
        logging.info(f"message: {message}") 

        # 执行 playground
        answer = self.playground.run(message, stream)

        # 保存本轮数据
        user_session.append({
            "query": message,
            "answer": answer,
        }) 
        return answer

# component 可以独立运行，session数据会被保存于内存
playground_with_history_component = PlaygroundWithHistory()
print(playground_with_history_component.run(Message("海淀区的面积是多少"), stream=False))
```

**会话数据存储数据库**

使用 AgentRuntime 对 Component 服务化，会话数据会被存储于数据库。
下面的代码以 SQLite 为例展示该能力，更多数据库配置详见[文档](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)

```python
user_session_config = "sqlite:///foo.db"
agent = appbuilder.AgentRuntime(
    component=playground_with_history_component, 
    user_session_config=user_session_config)
agent.serve( port=8091)
```


### 请求时鉴权
AgentRuntime 支持在请求时进行认证，确保安全性。

使用该能力，在初始化组件时需要设置 lazy 鉴权：

```python
import appbuilder

# 无需配置 APPBUILDER_TOKEN 环境变量

component = appbuilder.Playground(
    prompt_template="{query}",
    model="ERNIE-Bot",
    lazy_certification=True, # 设置 lazy 鉴权，在创建时不进行认证
)

agent = appbuilder.AgentRuntime(component=component)
agent.serve(port=8091)
```

请求时使用 Token 鉴权：

```shell
curl --location 'http://0.0.0.0:8091/chat' \
    --header 'Content-Type: application/json' \
    --header 'X-Appbuilder-Token: ...' \
    --data '{
        "message": "海淀区的面积是多少",
        "stream": false
    }'
```