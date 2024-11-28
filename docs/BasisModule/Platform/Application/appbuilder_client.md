# AppBuilderClient组件

## 简介

AppBuilderClient组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)
平台上通过AppBuilderClient构建并发布的智能体应用。

### 功能介绍

具体包括创建会话、上传文档、运行对话等

### 特色优势

与云端Console 应用能力打通，实现低代码会话

### 应用场景

快速、高效集成云端已发布智能体应用能力

## Python基本用法


### `AppBuilderClient().__init__()`


#### 方法参数

| 参数名称 | 参数类型 | 描述              | 示例值         |
| -------- | -------- | ----------------- | -------------- |
| app_id   | string   | 线上Agent应用的ID | "正确的应用ID" |

#### 方法返回值

```AppBuilderClient```实例化对象


### `AppBuilderClient().create_conversation()-> str`
#### 方法参数
无

#### 方法返回值

 | 参数名称        | 参数类型 | 描述     | 示例值                                 |
 | --------------- | -------- | -------- | -------------------------------------- |
 | conversation_id | string   | 会话的ID | "80c5bbee-931d-4ed9-a4ff-63e1971bd071" |


### `AppBuilderClient().upload_local_file(file_path: str)-> str`
#### 方法参数
| 参数名称  | 参数类型 | 描述     | 示例值           |
| --------- | -------- | -------- | ---------------- |
| file_path | string   | 文件路径 | "正确的文件路径" |
#### 方法返回值
| 参数名称 | 参数类型 | 描述   | 示例值                             |
| -------- | -------- | ------ | ---------------------------------- |
| file_id  | string   | 文件ID | "80c5bbee-931d-4ed9-a4ff-63e1971bd |


### `AppBuilderClient().run() -> Message`

#### 方法参数

| 参数名称        | 参数类型           | 是否必须 | 描述                                                         | 示例值            |
| --------------- | ------------------ | -------- | ------------------------------------------------------------ | ----------------- |
| conversation_id | String             | 是       | 会话ID                                                       |                   |
| query           | String             | 否       | query问题内容                                                | "今天天气怎么样?" |
| file_ids        | list[String]       | 否       | 对话可引用的文档ID                                           |                   |
| stream          | Bool               | 否       | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 | False             |
| end_user_id     | String             | 否       | 终端用户ID，限制6 - 64字符                                   |                   |
| tools           | List[Tool]         | 否       | 一个列表，其中每个字典对应一个工具的配置                     |                   |
| tools[0]        | Tool               | 否       | 工具配置                                                     |                   |
| +type           | String             | 否       | 枚举：<br/>**file_retrieval**: 知识库检索工具能够理解文档内容，支持用户针对文档内容的问答。<br/>**code_interpreter**: 代码解释器, 代码解释器能够生成并执行代码，从而协助用户解决复杂问题，涵盖科学计算（包括普通数学计算题）、数据可视化、文件编辑处理（图片、PDF文档、视频、音频等）、文件格式转换（如WAV、MP3、text、SRT、PNG、jpg、MP4、GIF、MP3等）、数据分析&清洗&处理（文件以excel、csv格式为主）、机器学习&深度学习建模&自然语言处理等多个领域。<br/>**function**: 支持fucntion call模式调用工具 |                   |
| +function       | Function           | 否       | Function工具描述<br/>仅当**type为**`**function**` 时需要且必须填写 |                   |
| ++name          | String             | 否       | 函数名<br/>只允许数字、大小写字母和中划线和下划线，最大长度为64个字符。一次运行中唯一。 |                   |
| ++description   | String             | 否       | 工具描述                                                     |                   |
| ++parameters    | Dict               | 否       | 工具参数, json_schema格式                                    |                   |
| tool_outputs    | List[ToolOutput]   | 否       | 内容为本地的工具执行结果，以自然语言/json dump str描述       |                   |
| tool_outputs[0] | ToolOutput         | 否       | 工具执行结果                                                 |                   |
| +tool_call_id   | String             | 否       | 工具调用ID                                                   |                   |
| +output         | String             | 否       | 工具输出                                                     |                   |
| tool_choice     | ToolChoice         | 否       | 控制大模型使用组件的方式，仅对自主规划Agent生效。            |                   |
| +type           | String             | 否       | auto/function，auto表示由LLM自动判断调什么组件；function表示由用户指定调用哪个组件。 |                   |
| +function       | ToolChoiceFunction | 否       | 组件对象，包括组件的英文名称和入参                           |                   |
| ++name          | String             | 否       | 组件的英文名称（唯一标识）                                   |                   |
| ++input         | String             | 否       | 组件入参，当组件没有入参时填入空对象{}                       |                   |
| action          | Action             | 否       | 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息 |                   |
| +action_type    | String             | 是       | 要执行的操作。<br/>可选值为：<br/>resume：回复“信息收集节点” 的消息 |                   |
| +parameters     | Object             | 是       | 执行操作时所需的参数                                         |                   |

#### Run方法非流式返回值

Run非流式方法返回一个`Message`对象，该对象包含以下属性：

| 参数名称       | 参数类型               | 描述                 | 示例值                                                                                  |
| -------------- | ---------------------- | -------------------- | --------------------------------------------------------------------------------------- |
| content        | AppBuilderClientAnswer | 对话返回结果         |                                                                                         |
| +answer        | String                 | 智能体应用返回的回答 |                                                                                         |
| +events        | List[Event]            | 事件列表             |                                                                                         |
| +events[0]     | Event                  | 具体事件内容         |                                                                                         |
| ++code         | String                 | 错误码               |                                                                                         |
| ++message      | String                 | 错误具体消息         |                                                                                         |
| ++status       | String                 | 事件状态             | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）      |
| ++event_type   | String                 | 事件类型             |                                                                                         |
| ++content_type | String                 | 内容类型             | 可选值包括：code text, image, status,image, function_call, rag, audio、video等          |
| ++detail       | Dict                   | 事件输出详情         | 代码解释器、文生图、工具组件、RAG等的详细输出内容                                       |
| ++usage        | Usage                  | 模型调用的token用量  | Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K') |

`AppBuilderClientAnswer`类型定义如下：
```python
class AppBuilderClientAnswer(BaseModel):
    """执行步骤的具体内容
        属性:
            answer(str): query回答内容
            events( list[Event]): 事件列表
       """
    answer: str = ""
    events: list[Event] = []
```

`Event`类型定义如下：
```python
class Event(BaseModel):
    """执行步骤的具体内容
        属性:
            code (int): 响应code码
            message (str): 错误详情
            status (str): 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）
            event_type（str）: 事件类型
            content_type（str）: 内容类型
            detail(dict): 事件详情
            usage(Usage): 大模型调用的token用量
    """
    code: int = 0
    message: str = ""
    status: str = ""
    event_type: str = ""
    content_type: str = ""
    detail: dict = {}
    usage: Optional[Usage] = None
```


#### Run方法流式返回值

| 参数名称 | 参数类型         | 描述                                           | 示例值 |
| -------- | ---------------- | ---------------------------------------------- | ------ |
| content  | Python Generator | 可迭代，每次迭代返回AppBuilderClientAnswer类型 | 无     |

#### 非流式调用示例

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AppBuilder应用ID，可在console端查看
# 初始化智能体
builder = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = builder.create_conversation()
# 运行对话
out = builder.run(conversation_id, "北京今天天气怎么样")
# 打印会话结果 
print(out.content.answer)
```

#### 流式调用示例

```python

import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'
app_id = '...'  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()

# 上传一个介绍某汽车产品的说明文档
file_id = client.upload_local_file(conversation_id, "/path/to/pdf/file")
# 引用上传的文档，开始对话
# 注意file_ids不是必填项，如果不需要引用特定文档，file_ids留空即可
message = client.run(conversation_id, "汽车性能参数怎么样", file_ids=[file_id, ], stream=True)

answer = ""

# 每次迭代返回AppBuilderClientAnswer结构，内可能包括多个事件内容
for content in message.content:
    # stream=True时，将answer拼接起来才是完整的的对话结果
    answer += content.answer
    for event in content.events:
        content_type = event.content_type
        detail = event.detail
        # 根据content类型对事件详情进行解析
        if content_type == "code":
            code_detail = data_class.CodeDetail(**detail)
            print(code_detail.code)
        elif content_type == "text":
            text_detail = data_class.TextDetail(**detail)
            print(text_detail.text)
        elif content_type == "image":
            image_detail = data_class.ImageDetail(**detail)
            print(image_detail.url)
        elif content_type == "rag":
            rag_detail = data_class.RAGDetail(**detail)
            if len(rag_detail.references) > 0:
                print(rag_detail.references)
        elif content_type == "function_call":
            function_call_detail = data_class.FunctionCallDetail(**detail)
            print(function_call_detail.video)
        elif content_type == "audio":
            audio_detail = data_class.AudioDetail(**detail)
            print(audio_detail)
        elif content_type == "video":
            video_detail = data_class.VideoDetail(**detail)
            print(video_detail)
        elif content_type == "status":
            status_detail = data_class.StatusDetail(**detail)
            print(status_detail)
        else:
            default_detail = data_class.DefaultDetail(**detail)
            print(default_detail)

# 打印完整的answer结果
print(answer)
```



#### Run方法带ToolCall调用示例

以下示例展示了三种方式来使用 ToolCall 进行调用，并演示了如何在 AppBuilder 环境中配置和执行会话调用。

**方式1：使用 JSONSchema 格式直接描述 tools 调用**

```python
import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."
app_id = "..."  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "仅支持中国城市的天气查询，参数location为中国城市名称，其他国家城市不支持天气查询",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名，举例：北京",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location", "unit"],
            },
        },
    }
]

msg = client.run(
    conversation_id=conversation_id, query="今天北京天气怎么样？", tools=tools
)
print(msg.model_dump_json(indent=4))

event = msg.content.events[-1]

msg_2 = client.run(
    conversation_id=conversation_id,
    tool_outputs=[{"tool_call_id": event.tool_calls[-1].id, "output": "北京今天35度"}],
)
print(msg_2.model_dump_json(indent=4))
```

**方式2: 使用 function_to_model 将函数对象传递为 ToolCall 的调用**

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."
app_id = "..."  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()
#注意：要使用此方法要为函数写好注释。最好按照谷歌规范来写

#定义示例函数
def get_current_weather(location: str, unit: str) -> str:
  """获取指定中国城市的当前天气信息。

  仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。

  Args:
      location (str): 城市名，例如："北京"。
      unit (int): 温度单位，支持 "celsius" 或 "fahrenheit"。

  Returns:
      str: 天气情况描述
  """
  return "北京今天25度"
  
#定义函数列表
functions = [get_current_weather]
function_map = {f.__name__: f for f in functions}
#调用大模型
msg = client.run(
  conversation_id=conversation_id,
  query="今天北京的天气怎么样？",
  tools = [appbuilder.Manifest.from_function(f) for f in functions]
  )
print(msg.model_dump_json(indent=4))
# 获取最后的事件和工具调用信息
event = msg.content.events[-1]
tool_call = event.tool_calls[-1]

# 获取函数名称和参数
name = tool_call.function.name
args = tool_call.function.arguments

# 将函数名称映射到具体的函数并执行
raw_result = function_map[name](**args)

# 传递工具的输出
msg_2 = client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call.id,
        "output": str(raw_result)
    }],
)
print(msg_2.model_dump_json(indent=4))
```

**方式3: 使用装饰器进行描述**

```python
import os
import json
import appbuilder
from appbuilder import manifest, manifest_parameter

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = ""
app_id = ""  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()

#使用manifest装饰描述函数，manifest_parameter装饰器描述参数，manifest_return装饰器描述函数返回值。
@manifest(description="获取指定中国城市的当前天气信息。仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。")
@manifest_parameter(name="location", description="城市名，例如：北京。")
@manifest_parameter(name="unit", description="温度单位，支持 'celsius' 或 'fahrenheit'")
#定义示例函数
def get_current_weather(location: str, unit: str) -> str:
  return "北京今天25度"

print(json.dumps(appbuilder.Manifest.from_function(get_current_weather), indent=4, ensure_ascii=False))
#定义函数列表
functions = [get_current_weather]
function_map = {f.__name__: f for f in functions}
#调用大模型
msg = client.run(
  conversation_id=conversation_id,
  query="今天北京的天气怎么样？",
  tools = [appbuilder.Manifest.from_function(f) for f in functions]
  )
print(msg.model_dump_json(indent=4))
# 获取最后的事件和工具调用信息
event = msg.content.events[-1]
tool_call = event.tool_calls[-1]

# 获取函数名称和参数
name = tool_call.function.name
args = tool_call.function.arguments

# 将函数名称映射到具体的函数并执行
raw_result = function_map[name](**args)

# 传递工具的输出
msg_2 = client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call.id,
        "output": str(raw_result)
    }],
)
print(msg_2.model_dump_json(indent=4))
```



#### Run方法带ToolChoice使用示例：

* 注意：当前功能为试运行阶段，可能存在如下问题，如使用过程遇到其他问题，欢迎提issue或微信群讨论。
  * 需开启"组件/知识库结论可直接作为回复"
  * 组件名称不是界面上的原始名字，而是个人空间组件列表中的英文名
  * 自定义组件的参数不能使用系统参数，可以使用用户添加的参数
  * 部分官方组件使用的参数与界面上的参数不一致

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."

app_id = "..."  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()

# 注意使用创建应用中用到的组件。名称、参数均以实际使用的组件为准。
answer = app_builder_client.run(
    conversation_id,
    "北京今天的天气",
    stream=False,
    end_user_id="user_id_toolchoice",
    tool_choice={
        "type": "function",
        "function": {"name": "WeatherQuery", "input": {"city": "北京"}},
    },
)
```



#### Run方法回复工作流Agent “信息收集节点”使用示例：

使用[“飞行客服小助手”](https://cloud.baidu.com/doc/AppBuilder/s/cm38k8nqr)作为工作流Agent的示例应用。

**方式1：** SDK直接进行对话（不推荐）

```python
import appbuilder
import os
from appbuilder.core.console.appbuilder_client import data_class

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = (
    "..."
)
appbuilder.logger.setLoglevel("ERROR")

# 飞行客服小助手的应用id
app_id = "..."
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()
interrupt_ids = []

msg = client.run(conversation_id, "查天气", stream=True)
interrupt_event_id = None
for ans in msg.content:
    for event in ans.events:
        if event.content_type == "publish_message":
            print(event.detail.get("message"))
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
            break
interrupt_ids.append(interrupt_event_id)

msg2 = client.run(
    conversation_id,
    "查航班",
    stream=True,
    action=data_class.Action.create_resume_action(interrupt_event_id),
)
interrupt_event_id = None
for ans in msg2.content:
    for event in ans.events:
        if event.content_type == "publish_message":
            print(event.detail.get("message"))
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
            break
        interrupt_ids.append(interrupt_event_id)

msg3 = client.run(
    conversation_id=conversation_id,
    query="CA1234",
    stream=True,
    action=data_class.Action.create_resume_action(interrupt_ids.pop()),
)
interrupt_event_id = None
for ans in msg3.content:
    for event in ans.events:
        if event.content_type == "text":
            print(event.detail.get("text"))
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
            break
interrupt_ids.append(interrupt_event_id)

msg4 = client.run(
    conversation_id=conversation_id,
    query="北京的",
    stream=True,
    action=data_class.Action.create_resume_action(interrupt_ids.pop()),
)
has_multiple_dialog_event = False
for ans in msg4.content:
    for event in ans.events:
        if event.content_type == "text":
            print(event.detail.get("text"))
        if event.content_type == "multiple_dialog_event":
            has_multiple_dialog_event = True
            break

```

**方式2：** 实现自己的EventHandler，更方便地进行对话（推荐）

```python
import os
import appbuilder
from appbuilder.core.console.appbuilder_client.event_handler import (
    AppBuilderEventHandler,
)


class MyEventHandler(AppBuilderEventHandler):
    def __init__(self):
        super().__init__()
        self.interrupt_ids = []

    def handle_content_type(self, run_context, run_response):
        interrupt_event_id = None
        event = run_response.events[-1]
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
        if interrupt_event_id is not None:
            self.interrupt_ids.append(interrupt_event_id)

    def _create_action(self):
        if len(self.interrupt_ids) == 0:
            return None
        event_id = self.interrupt_ids.pop()
        return {
            "action_type": "resume",
            "parameters": {"interrupt_event": {"id": event_id, "type": "chat"}},
        }

    def run(self, query=None):
        super().new_dialog(
            query=query,
            action=self._create_action(),
        )


def main():
    # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
    # 设置环境变量
    os.environ["APPBUILDER_TOKEN"] = "..."
    appbuilder.logger.setLoglevel("DEBUG")

    # 飞行客服小助手的应用id
    app_id = "..."
    # 初始化智能体
    client = appbuilder.AppBuilderClient(app_id)
    conversation_id = client.create_conversation()

    event_handler = MyEventHandler()
    event_handler.init(
        appbuilder_client=client,
        conversation_id=conversation_id,
        stream=True,
        query="查天气",
    )
    for data in event_handler:
        pass
    event_handler.run(
        query="查航班",
    )
    for data in event_handler:
        pass
    event_handler.run(
        query="CA1234",
    )
    for data in event_handler:
        pass
    event_handler.run(
        query="北京的",
    )
    for data in event_handler:
        pass


if __name__ == "__main__":
    main()
```

**方式3:** 实现自己的EventHandler，更方便地进行多轮对话（推荐）

```python
import os
import appbuilder
from appbuilder.core.console.appbuilder_client.event_handler import (
    AppBuilderEventHandler,
)


class MyEventHandler(AppBuilderEventHandler):
    def __init__(self):
        super().__init__()
        self.interrupt_ids = []

    def handle_content_type(self, run_context, run_response):
        interrupt_event_id = None
        event = run_response.events[-1]
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
        if interrupt_event_id is not None:
            self.interrupt_ids.append(interrupt_event_id)

    def _create_action(self):
        if len(self.interrupt_ids) == 0:
            return None
        event_id = self.interrupt_ids.pop()
        return {
            "action_type": "resume",
            "parameters": {"interrupt_event": {"id": event_id, "type": "chat"}},
        }

    def gen_action(self):
        while True:
            yield self._create_action()


def main():
    # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
    # 设置环境变量
    os.environ["APPBUILDER_TOKEN"] = "..."
    appbuilder.logger.setLoglevel("DEBUG")

    # 飞行客服小助手的应用id
    app_id = "..."
    # 初始化智能体
    client = appbuilder.AppBuilderClient(app_id)
    conversation_id = client.create_conversation()

    queries = ["查天气", "查航班", "CA1234", "北京的"]
    event_handler = MyEventHandler()
    event_handler = client.run_multiple_dialog_with_handler(
        conversation_id=conversation_id,
        queries=queries,
        event_handler=event_handler,
        stream=True,
        actions=event_handler.gen_action(),
    )
    for data in event_handler:
        for ans in data:
            pass


if __name__ == "__main__":
    main()
```



## Java基本用法

### ```new AppBuilderClient(appId)```

#### 方法参数

| 参数名称 | 参数类型 | 描述              | 示例值         |
| -------- | -------- | ----------------- | -------------- |
| appID    | String   | 线上Agent应用的ID | "正确的应用ID" |


#### 方法返回值

```AppBuilderClient```实例化对象

### ```AppBuilderClient().createConversation()```

#### 方法参数
无

#### 方法返回值

| 参数名称       | 参数类型 | 描述         | 示例值         |
| -------------- | -------- | ------------ | -------------- |
| conversationId | String   | 创建的会话ID | "正确的会话ID" |

### ```AppBuilderClient().run()```

#### Run方法入参`AppBuilderCientRunRequest`

| 参数名称        | 参数类型           | 是否必须 | 描述                                                         | 示例值               |
| --------------- | ------------------ | -------- | ------------------------------------------------------------ | -------------------- |
| query           | String             | 是       | query内容                                                    | "汽车性能参数怎么样" |
| conversationId  | String             | 是       | 对话id，可以通过createConversation()获取                     |                      |
| stream          | boolean            | 是       | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |                      |
| tools           | List[Tool]         | 否       | 一个列表，其中每个字典对应一个工具的配置                     |                      |
| tools[0]        | Tool               | 否       | 工具配置                                                     |                      |
| +type           | String             | 否       | 枚举：<br/>**file_retrieval**: 知识库检索工具能够理解文档内容，支持用户针对文档内容的问答。<br/>**code_interpreter**: 代码解释器, 代码解释器能够生成并执行代码，从而协助用户解决复杂问题，涵盖科学计算（包括普通数学计算题）、数据可视化、文件编辑处理（图片、PDF文档、视频、音频等）、文件格式转换（如WAV、MP3、text、SRT、PNG、jpg、MP4、GIF、MP3等）、数据分析&清洗&处理（文件以excel、csv格式为主）、机器学习&深度学习建模&自然语言处理等多个领域。<br/>**function**: 支持fucntion call模式调用工具 |                      |
| +function       | Function           | 否       | Function工具描述<br/>仅当**type为**`**function**` 时需要且必须填写 |                      |
| ++name          | String             | 否       | 函数名<br/>只允许数字、大小写字母和中划线和下划线，最大长度为64个字符。一次运行中唯一。 |                      |
| ++description   | String             | 否       | 工具描述                                                     |                      |
| ++parameters    | Dict               | 否       | 工具参数, json_schema格式                                    |                      |
| tool_outputs    | List[ToolOutput]   | 否       | 内容为本地的工具执行结果，以自然语言/json dump str描述       |                      |
| tool_outputs[0] | ToolOutput         | 否       | 工具执行结果                                                 |                      |
| +tool_call_id   | String             | 否       | 工具调用ID                                                   |                      |
| +output         | String             | 否       | 工具输出                                                     |                      |
| tool_choice     | ToolChoice         | 否       | 控制大模型使用组件的方式，仅对自主规划Agent生效。            |                      |
| +type           | String             | 否       | auto/function，auto表示由LLM自动判断调什么组件；function表示由用户指定调用哪个组件。 |                      |
| +function       | ToolChoiceFunction | 否       | 组件对象，包括组件的英文名称和入参                           |                      |
| ++name          | String             | 否       | 组件的英文名称（唯一标识）                                   |                      |
| ++input         | String             | 否       | 组件入参，当组件没有入参时填入空对象{}                       |                      |
| action          | Action             | 否       | 对话时要进行的特殊操作。如回复工作流agent中“信息收集节点“的消息 |                      |
| +action_type    | String             | 是       | 要执行的操作。<br/>可选值为：<br/>resume：回复“信息收集节点” 的消息 |                      |
| +parameters     | Object             | 是       | 执行操作时所需的参数                                         |                      |

#### Run方法出参
| 参数名称                 | 参数类型                 | 描述                                                                             | 示例值 |
| ------------------------ | ------------------------ | -------------------------------------------------------------------------------- | ------ |
| AppBuilderClientIterator | AppBuilderClientIterator | 回答迭代器，流式/非流式均统一返回该类型,每次迭代返回AppBuilderClientIterator类型 |        |

#### 迭代AppBuilderClientIterator
| 参数名称      | 参数类型            | 描述                 | 示例值                                                                                  |
| ------------- | ------------------- | -------------------- | --------------------------------------------------------------------------------------- |
| +answer       | String              | 智能体应用返回的回答 |                                                                                         |
| +events       | Event[]             | 事件列表             |                                                                                         |
| +events[0]    | Event               | 具体事件内容         |                                                                                         |
| ++code        | string              | 错误码               |                                                                                         |
| ++message     | string              | 错误具体消息         |                                                                                         |
| ++status      | string              | 事件状态             | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）      |
| ++eventType   | string              | 事件类型             |                                                                                         |
| ++contentType | string              | 内容类型             | 可选值包括：code text, image, status,image, function_call, rag, audio、video等          |
| ++detail      | Map<String, Object> | 事件输出详情         | 代码解释器、文生图、工具组件、RAG等的详细输出内容                                       |
| ++usage       | Usage               | 模型调用的token用量  | Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K') |


#### 示例代码

```Java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String appId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        // 填写上传文件路径
        String fileId = builder.uploadLocalFile(conversationId, "/Users/zhangxiaoyu15/PycharmProjects/app-builder/test_app_builder_client/test.pdf");
        // 输入query
        // 注意file_ids不是必填项，如果不需要引用特定文档，则将new String[]{fileId}更换为new String[]{}即可
        AppBuilderClientIterator itor = builder.run("中国四大传统节日是哪四个", conversationId, new String[]{fileId}, false);
        StringBuilder answer = new StringBuilder();
        // itor.hasNext()返回false时，表示流式调用结束
        while(itor.hasNext())
        {
            AppBuilderClientResult response = itor.next();
            answer.append(response.getAnswer());
            for (Event event : response.getEvents()) {
                switch (event.getContentType()) {
                    case "rag":
                        List<Object> references = (List<Object>)event.getDetail().get("references");
                        for (Object reference : references) {
                            ReferenceDetail ragDetail = JsonUtils.deserialize(JsonUtils.serialize(reference), ReferenceDetail.class);
                            System.out.println("-----------------------------------");
                            System.out.println("参考文献ID:"+ragDetail.getId());
                            System.out.println("参考文献内容:"+ragDetail.getContent());
                            System.out.println("来源:"+ragDetail.getFrom());
                            System.out.println("BaiduSearch链接:"+ragDetail.getUrl());
                            System.out.println("类型:"+ragDetail.getType());
                            System.out.println("文档片段ID:"+ragDetail.getSegmentId());
                            System.out.println("文档ID:"+ragDetail.getDocumentId());
                            System.out.println("文档名称:"+ragDetail.getDocumentName());
                            System.out.println("文档所属数据集ID:"+ragDetail.getDatasetId());
                            System.out.println("-----------------------------------");
                        }
                        break;
                    default:
                        // System.out.println(event);
                }
            }
        }
        System.out.print("输出：");
        System.out.println(answer);
    }
}

class ReferenceDetail {
    private int id;
    private String content;
    private String from;
    private String url;
    private String type;
    @SerializedName("segment_id")
    private String segmentId;
    @SerializedName("document_id")
    private String documentId;
    @SerializedName("document_name")
    private String documentName;
    @SerializedName("dataset_id")
    private String datasetId;
    @SerializedName("knowledgebase_id")
    private String knowledgebaseId;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getSegmentId() {
        return segmentId;
    }

    public void setSegmentId(String segmentId) {
        this.segmentId = segmentId;
    }

    public String getDocumentId() {
        return documentId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }

    public String getDocumentName() {
        return documentName;
    }

    public void setDocumentName(String documentName) {
        this.documentName = documentName;
    }

    public String getDatasetId() {
        return datasetId;
    }

    public void setDatasetId(String datasetId) {
        this.datasetId = datasetId;
    }

    public String getKnowledgebaseId() {
        return knowledgebaseId;
    }

    public void setKnowledgebaseId(String knowledgebaseId) {
        this.knowledgebaseId = knowledgebaseId;
    }

    @Override
    public String toString() {
        return "RAGReference{" +
                "id=" + id +
                ", content='" + content + '\'' +
                ", from='" + from + '\'' +
                ", url='" + url + '\'' +
                ", type='" + type + '\'' +
                ", segmentId='" + segmentId + '\'' +
                ", documentId='" + documentId + '\'' +
                ", documentName='" + documentName + '\'' +
                ", datasetId='" + datasetId + '\'' +
                ", knowledgebaseId='" + knowledgebaseId + '\'' +
                '}';
    }
}
```

#### Run方法带ToolCall调用示例

**创建tool的json文件**

```json
{
    "type": "function",
    "function": {
        "name": "get_cur_whether",
        "description": "这是一个获得指定地点天气的工具",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "省，市名，例如：河北省"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "摄氏度",
                        "华氏度"
                    ]
                }
            },
            "required": [
                "location"
            ]
        }
    }
}
```

```java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String appId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
       
        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "今天北京的天气怎么样?", false);

        String toolJson = new String(Files.readAllBytes(Paths.get("json文件所在的路径")));
        request.setTools(toolJson);

        AppBuilderClientIterator itor = builder.run(request);
        String ToolCallID = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            ToolCallID = result.getEvents()[0].getToolCalls()[0].getId();
            System.out.println(result);
        }

        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest(appId, conversationId);
        request2.setToolOutputs(ToolCallID, "北京今天35度");
        AppBuilderClientIterator itor2 = builder.run(request2);
        while (itor2.hasNext()) {
            AppBuilderClientResult result = itor2.next();
            System.out.println(result);
        }
    }
}

```

#### Run方法带Toolchoice使用示例

* 注意：当前功能为试运行阶段，可能存在如下问题，如使用过程遇到其他问题，欢迎提issue或微信群讨论。

  * 需开启"组件/知识库结论可直接作为回复"

  * 组件名称不是界面上的原始名字，而是个人空间组件列表中的英文名

  * 自定义组件的参数不能使用系统参数，可以使用用户添加的参数

  * 部分官方组件使用的参数与界面上的参数不一致

```java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String appId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();

        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "你能干什么", false);
        request.setEndUserId("java_toolchoice_demo");
      
        // 注意使用创建应用中用到的组件。名称、参数均以实际使用的组件为准。
        Map<String, Object> input = new HashMap<>();
        input.put("city", "北京");
        AppBuilderClientRunRequest.ToolChoice.Function func = new AppBuilderClientRunRequest.ToolChoice.Function(
                "WeatherQuery", input);
        AppBuilderClientRunRequest.ToolChoice choice = new AppBuilderClientRunRequest.ToolChoice("function", func);
        request.setToolChoice(choice);

        AppBuilderClientIterator itor = builder.run(request);
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }
}

```

#### Run方法回复工作流Agent “信息收集节点”使用示例：

使用[“飞行客服小助手”](https://cloud.baidu.com/doc/AppBuilder/s/cm38k8nqr)作为工作流Agent的示例应用

```java
package org.example;

import java.io.IOException;
import java.util.*;

import com.google.gson.annotations.SerializedName;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

class AppBuilderClientDemo {

    public static void main(String[] args) throws IOException, AppBuilderServerException {
        System.setProperty("APPBUILDER_TOKEN", "请设置正确的应用密钥");
        String chatflowAppId = "请设置正确的应用ID";
        AppBuilderClient builder = new AppBuilderClient(chatflowAppId);
        String conversationId = builder.createConversation();

				AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "查天气", true);
        Stack<String> interruptStack = new Stack<String>();
        AppBuilderClientIterator itor = builder.run(request);
        String interruptEventId = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            for (Event event : result.getEvents()) {
                if (event.getContentType().equals(EventContent.PublishMessageContentType)) {
                    String message = event.getDetail().get("message").toString();
                    System.out.println(message);
                }
                if (event.getContentType().equals(EventContent.ChatflowInterruptContentType)) {
                    interruptEventId = event.getDetail().get("interrupt_event_id").toString();
                    interruptStack.push(interruptEventId);
                    break;
                }
            }
        }
      
        interruptEventId = "";
        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "我先查个航班动态", true);
        request2.setAction(AppBuilderClientRunRequest.Action.createAction(interruptStack.pop()));
        AppBuilderClientIterator itor2 = builder.run(request2);
        while (itor2.hasNext()) {
            AppBuilderClientResult result2 = itor2.next();
            for (Event event : result2.getEvents()) {
                if (event.getContentType().equals(EventContent.PublishMessageContentType)) {
                    String message = event.getDetail().get("message").toString();
                    System.out.println(message);
                }
                if (event.getContentType().equals(EventContent.ChatflowInterruptContentType)) {
                    interruptEventId = event.getDetail().get("interrupt_event_id").toString();
                    interruptStack.push(interruptEventId);
                    break;
                }
            }
        }
      
        interruptEventId = "";
        AppBuilderClientRunRequest request3 = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "CA1234", true);
        request3.setAction(AppBuilderClientRunRequest.Action.createAction(interruptStack.pop()));
        AppBuilderClientIterator itor3 = builder.run(request3);
        while (itor3.hasNext()) {
            AppBuilderClientResult result3 = itor3.next();
            for (Event event : result3.getEvents()) {
                if (event.getContentType().equals(EventContent.TextContentType)) {
                    String text = event.getDetail().get("text").toString();
                    System.out.println(text);
                }
                if (event.getContentType().equals(EventContent.ChatflowInterruptContentType)) {
                    interruptEventId = event.getDetail().get("interrupt_event_id").toString();
                    interruptStack.push(interruptEventId);
                    break;
                }
            }
        }
      
        boolean hasMultipleContentType = false;
        AppBuilderClientRunRequest request4 = new AppBuilderClientRunRequest(chatflowAppId, conversationId, "北京的",
                true);
        request4.setAction(AppBuilderClientRunRequest.Action.createAction(interruptStack.pop()));
        AppBuilderClientIterator itor4 = builder.run(request4);
        while (itor4.hasNext()) {
            AppBuilderClientResult result4 = itor4.next();
            for (Event event : result4.getEvents()) {
                if (event.getContentType().equals(EventContent.TextContentType)) {
                    String text = event.getDetail().get("text").toString();
                    System.out.println(text);
                }
                if (event.getContentType().equals(EventContent.MultipleDialogEventContentType)) {
                    hasMultipleContentType = true;
                    break;
                }
            }
        }
    }
}

```



## Go基本用法

### ```NewAppBuilderClient()```

#### 方法参数

| 参数名称 | 参数类型  | 描述              | 示例值         |
| -------- | --------- | ----------------- | -------------- |
| app_id   | string    | 线上Agent应用的ID | "正确的应用ID" |
| config   | SDKConfig | SDK配置信息       |                |

### ```CreateConversation()```
#### 方法入参
无
#### 方法出参
| 参数名称       | 参数类型 | 描述                                         | 示例值 |
| -------------- | -------- | -------------------------------------------- | ------ |
| ConversationId | str      | 创建成功的对话对象，后续操作都基于该对象进行 |        |


### `Run()`
#### Run方法入参`AppBuilderClientRunRequest`

| 参数名称       | 参数类型   | 是否必须 | 描述                                                         | 示例值               |
| -------------- | ---------- | -------- | ------------------------------------------------------------ | -------------------- |
| ConversationID | string     | 是       | 对话ID，可以通过CreateConversation()获取                     |                      |
| Query          | string     | 是       | query内容                                                    | "汽车性能参数怎么样" |
| Stream         | bool       | 是       | 为true时则流式返回，为false时则一次性返回所有内容, 推荐设为true，降低首token时延 |                      |
| AppID          | string     | 是       | 应用ID，线上Agent应用的ID                                    |                      |
| Tools          | []Tool     | 否       | 一个列表，其中每个字典对应一个工具的配置                     |                      |
| ToolOuptus     | []ToolOupt | 否       | 内容为本地的工具执行结果，以自然语言/json dump str描述       |                      |
| ToolChoice     | ToolChoice | 否       | 控制大模型使用组件的方式，仅对自主规划Agent生效。            |                      |

`Tool`、`ToolOutput`、`ToolChoice`定义如下：

```go
type Tool struct {
	Type     string   `json:"type"`
	Function Function `json:"function"`
}

type Function struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	Parameters  map[string]interface{} `json:"parameters"`
}

type ToolOutput struct {
	ToolCallID string `json:"tool_call_id" description:"工具调用ID"`
	Output     string `json:"output" description:"工具输出"`
}

type ToolChoice struct {
	Type     string             `json:"type"`
	Function ToolChoiceFunction `json:"function"`
}

type ToolChoiceFunction struct {
	Name  string                 `json:"name"`
	Input map[string]interface{} `json:"input"`
}
```

#### Run方法出参

| 参数名称                 | 参数类型                 | 描述                                    | 示例值 |
| ------------------------ | ------------------------ | --------------------------------------- | ------ |
| AppBuilderClientIterator | AppBuilderClientIterator | 回答迭代器，流式/非流式均统一返回该类型 |        |
| error                    | error                    | 存在错误时error不为nil，反之            |        |

#### 迭代AgentBuilderIterator

| 参数名称      | 参数类型    | 描述                 | 示例值                                                                                  |
| ------------- | ----------- | -------------------- | --------------------------------------------------------------------------------------- |
| +Answer       | string      | 智能体应用返回的回答 |                                                                                         |
| +Events       | []Event     | 事件列表             |                                                                                         |
| +Events[0]    | Event       | 具体事件内容         |                                                                                         |
| ++Code        | string      | 错误码               |                                                                                         |
| ++Message     | string      | 错误具体消息         |                                                                                         |
| ++Status      | string      | 事件状态             | 状态描述，preparing（准备运行）running（运行中）error（执行错误） done（执行完成）      |
| ++EventType   | string      | 事件类型             |                                                                                         |
| ++ContentType | string      | 内容类型             | 可选值包括：code text, image, status,image, function_call, rag, audio、video等          |
| ++Detail      | interface{} | 事件输出详情         | 代码解释器、文生图、工具组件、RAG等的详细输出内容                                       |
| ++Usage       | Usage       | 模型调用的token用量  | Usage(prompt_tokens=1322, completion_tokens=80, total_tokens=1402, name='ERNIE-4.0-8K') |


#### Run示例代码


```Go
// 安装说明：
// go get github.com/baidubce/app-builder/go/appbuilder

package main

import (
    "errors"
    "fmt"
    "io"
    "os"

    "github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
    // 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取
    os.Setenv("APPBUILDER_TOKEN", "bce-v3/ALTAK-xxx90ea58")
    // 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
    appID := "4678492a-xxx-654538d3503c"
    config, err := appbuilder.NewSDKConfig("", "")
    if err != nil {
        fmt.Println("new config failed: ", err)
        return
    }

    builder, err := appbuilder.NewAppBuilderClient(appID, config)
    if err != nil {
        fmt.Println("new agent builder failed: ", err)
        return
    }
    conversationID, err := builder.CreateConversation()
    if err != nil {
        fmt.Println("create conversation failed: ", err)
        return
    }

    i, err := builder.Run(conversationID, "你好，你能做什么？", nil, false)
    if err != nil {
        fmt.Println("run failed: ", err)
        return
    }

	var answer *appbuilder.AppBuilderClientAnswer
	for answer, err = i.Next(); err == nil; answer, err = i.Next() {
		fmt.Println(answer.Answer)
	}
}
```

#### ToolCall功能示例代码

```go
package main

import (
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL_V2环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://qianfan.baidubce.com
	os.Setenv("GATEWAY_URL_V2", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	builder, err := appbuilder.NewAppBuilderClient(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := builder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}

	jsonStr := `
	{
		"type": "function",
		"function": {
			"name": "get_cur_whether",
			"description": "这是一个获得指定地点天气的工具",
			"parameters": {
				"type": "object",
				"properties": {
					"location": {
						"type": "string",
						"description": "省，市名，例如：河北省"
					},
					"unit": {
						"type": "string",
						"enum": ["摄氏度", "华氏度"]
					}
				},
				"required": ["location"]
			}
		}
	}`

	var tool Tool
	err = json.Unmarshal([]byte(jsonStr), &tool)
	if err != nil {
		fmt.Println("unmarshal tool error:", err)
        return
	}

	i, err := client.Run(appbuilder.AppBuilderClientRunRequest{
		AppID:          appID,
		Query:          "今天北京的天气怎么样?",
		ConversationID: conversationID,
		Stream:         true,
		Tools: []appbuilder.Tool{tool},
	})
	if err != nil {
		fmt.Println("run failed:", err)
	}
	totalAnswer := ""
	toolCallID := ""
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			toolCallID = ev.ToolCalls[0].ID
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
		}
	}

	i2, err := client.Run(appbuilder.AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		ToolOutputs: []appbuilder.ToolOutput{
			{
				ToolCallID: toolCallID,
				Output:     "北京今天35度",
			},
		},
		Stream: true,
	})

	if err != nil {
		fmt.Println("run failed: ", err)
	}

	for answer, err := i2.Next(); err == nil; answer, err = i2.Next() {
		totalAnswer = totalAnswer + answer.Answer
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
		}
	}

	fmt.Println("----------------answer-------------------")
	fmt.Println(totalAnswer)
}
```

#### ToolChoice示例代码

* 注意：当前功能为试运行阶段，可能存在如下问题，如使用过程遇到其他问题，欢迎提issue或微信群讨论。

  * 需开启"组件/知识库结论可直接作为回复"

  * 组件名称不是界面上的原始名字，而是个人空间组件列表中的英文名
  
  * 自定义组件的参数不能使用系统参数，可以使用用户添加的参数

  * 部分官方组件使用的参数与界面上的参数不一致


```go
package main

import (
	"errors"
	"fmt"
	"io"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL_V2环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://qianfan.baidubce.com
	os.Setenv("GATEWAY_URL_V2", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	builder, err := appbuilder.NewAppBuilderClient(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := builder.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}

    // 注意使用创建应用中用到的组件。名称、参数均以实际使用的组件为准。
	input := make(map[string]any)
	input["city"] = "北京"
	end_user_id := "go_toolchoice_demo"
	i, err := client.Run(AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "",
		EndUserID:      &end_user_id,
		Stream:         false,
		ToolChoice: &ToolChoice{
			Type: "function",
			Function: ToolChoiceFunction{
				Name:  "WeatherQuery",
				Input: input,
			},
		},
	})
  
	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}

    for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		for _, ev := range answer.Events {
			evJSON, _ := json.Marshal(ev)
			fmt.Println(string(evJSON))
		}
	}
}
```

#### Run方法回复工作流Agent “信息收集节点”使用示例：

使用[“飞行客服小助手”](https://cloud.baidu.com/doc/AppBuilder/s/cm38k8nqr)作为工作流Agent的示例应用

```go
package main

import (
	"fmt"
	"os"

	"github.com/baidubce/app-builder/go/appbuilder"
)

func main() {
	// 设置APPBUILDER_TOKEN、GATEWAY_URL_V2环境变量
	os.Setenv("APPBUILDER_TOKEN", "请设置正确的应用密钥")
	// 默认可不填，默认值是 https://qianfan.baidubce.com
	os.Setenv("GATEWAY_URL_V2", "")
	config, err := appbuilder.NewSDKConfig("", "")
	if err != nil {
		fmt.Println("new config failed: ", err)
		return
	}
	// 初始化实例
	appID := "请填写正确的应用ID"
	client, err := appbuilder.NewAppBuilderClient(appID, config)
	if err != nil {
		fmt.Println("new agent builder failed: ", err)
		return
	}
	// 创建对话ID
	conversationID, err := client.CreateConversation()
	if err != nil {
		fmt.Println("create conversation failed: ", err)
		return
	}
	i, err := client.Run(appbuilder.AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "查天气",
		Stream:         true,
	})

	if err != nil {
		fmt.Println("run failed: ", err)
		return
	}

	var interruptId string
	interruptStack := make([]string, 0)
	for answer, err := i.Next(); err == nil; answer, err = i.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == appbuilder.PublishMessageContentType {
				detail := ev.Detail.(appbuilder.PublishMessageDetail)
				message := detail.Message
				fmt.Println(message)
				break
			}
			if ev.ContentType == appbuilder.ChatflowInterruptContentType {
				deatil := ev.Detail.(appbuilder.ChatflowInterruptDetail)
				interruptId = deatil.InterruptEventID
				interruptStack = append(interruptStack, interruptId)
				break
			}
		}
	}
	if len(interruptId) == 0 {
		fmt.Println("interrupt id is empty")
		return
	}

	interruptId = ""
	i2, err := client.Run(appbuilder.AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "我先查个航班动态",
		Stream:         true,
		Action:         appbuilder.NewResumeAction(interruptStack[len(interruptStack)-1]),
	})
	if err != nil {
		fmt.Println("run failed:", err)
		return
	}
	interruptStack = interruptStack[:len(interruptStack)-1]
	for answer, err := i2.Next(); err == nil; answer, err = i2.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == appbuilder.PublishMessageContentType {
				detail := ev.Detail.(appbuilder.PublishMessageDetail)
				message := detail.Message
				fmt.Println(message)
				break
			}
			if ev.ContentType == appbuilder.ChatflowInterruptContentType {
				deatil := ev.Detail.(appbuilder.ChatflowInterruptDetail)
				interruptId = deatil.InterruptEventID
				interruptStack = append(interruptStack, interruptId)
				break
			}
		}
	}
	if len(interruptId) == 0 {
		fmt.Println("interrupt id is empty")
		return
	}

	interruptId = ""
	i3, err := client.Run(appbuilder.AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "CA1234",
		Stream:         true,
		Action:         appbuilder.NewResumeAction(interruptStack[len(interruptStack)-1]),
	})
	if err != nil {
		fmt.Println("run failed:", err)
		return
	}
	interruptStack = interruptStack[:len(interruptStack)-1]
	for answer, err := i3.Next(); err == nil; answer, err = i3.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == appbuilder.TextContentType {
				detail := ev.Detail.(appbuilder.TextDetail)
				text := detail.Text
				fmt.Println(text)
				break
			}
			if ev.ContentType == appbuilder.ChatflowInterruptContentType {
				deatil := ev.Detail.(appbuilder.ChatflowInterruptDetail)
				interruptId = deatil.InterruptEventID
				interruptStack = append(interruptStack, interruptId)
				break
			}
		}
	}
	if len(interruptId) == 0 {
		fmt.Println("interrupt id is empty")
		return
	}

	i4, err := client.Run(appbuilder.AppBuilderClientRunRequest{
		ConversationID: conversationID,
		AppID:          appID,
		Query:          "北京的",
		Stream:         true,
		Action:         appbuilder.NewResumeAction(interruptStack[len(interruptStack)-1]),
	})
	if err != nil {
		fmt.Println("run failed:", err)
		return
	}
	for answer, err := i4.Next(); err == nil; answer, err = i4.Next() {
		for _, ev := range answer.Events {
			if ev.ContentType == appbuilder.TextContentType {
				detail := ev.Detail.(appbuilder.TextDetail)
				text := detail.Text
				fmt.Println(text)
				break
			}
		}
	}
}

```

