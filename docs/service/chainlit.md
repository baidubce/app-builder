# 交互式前端部署

## 基础组件基于Chainlit提供交互式前端页面

请参考 [组件服务化部署](https://github.com/baidubce/app-builder/blob/master/cookbooks/components/agent_runtime.ipynb)

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

````python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
component = appbuilder.Playground(
    prompt_template="{query}",
    model="eb-4"
)
agent = appbuilder.AgentRuntime(component=component)
agent.chainlit_demo(port=8091)
```