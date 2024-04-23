# AppBuilder Assistant SDK

## 简介

百度智能云千帆 AppBuilder 在提供零代码、低代码的AI原生应用搭建功能之外，也提供全代码灵活开发与集成能力。基于官方 API/SDK，开放丰富的组件服务，提供具备强大对话、思考及工具调用能力的 Agent 应用框架。

封装程度由高至低，提供了三种类型的SDK
| 分类   | 场景及使用方式   | 百度云文档链接         | SDK 文档链接|
|--------|--------|------------|------------|
| 端到端应用 | 在 AppBuilder 产品界面上通过零代码、低代码方式创建的 AI 原生应用，支持通过应用 API/SDK 进行调用 | [应用API及SDK](https://cloud.baidu.com/doc/AppBuilder/s/Flpv3oxup) | [Agent SDK](./agent_builder.md) |
| 代码态智能体 | 基于 Assistants API，可通过全代码形式创建和调试专属智能体（Agent） | [AssistantAPI](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben) | *当前文档* |
| 工具组件 | 基于组件 SDK，可调用包括大模型组件、AI能力组件等在内的多种组件 | [组件SDK](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz) | [组件列表](../appbuilder/core/components) |

Assistants API/SDK 全新开放，火热邀测中。点击[免费申请邀请测试资格](https://cloud.baidu.com/survey/assistantsapi.html)

</span>

### 功能介绍

Assistant SDK允许您在自己的应用程序中，使用纯代码构建人工智能助手。该助手可以利用模型、工具和文件来响应用户的诉求，提供关键的FunctionCall能力。

### 特色优势

与端到端应用相比，Assistants API/SDK 提供了更灵活、更强大的FunctionCall能力，可以满足更复杂的业务场景。基础功能对标 [OpenAI Assistant SDK](https://platform.openai.com/docs/assistants/overview?context=with-streaming)，且会结合国内开发者习惯 与 最广泛的ToB场景，提供更多的易用功能与端到端示例。

### 应用场景

使用SDK纯代码构建Assistant助手，适合有进阶开发能力的开发者。

## 基本用法

以下是使用SDK进行构建的代码示例，更多详细信息请参考[Assistant API文档](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben) 与 [Assistant SDK 数据类型文档](./assistant_type.md)

### 总览
一个标准的Assistant构建及使用过程如下：
1. 创建一个Assistant
2. 创建一个Thread
3. 为Thread添加一个Message
4. 创建并运行一个Thread.Run

下面的QuickStart会分别介绍每一个步骤的最简上手步骤

### QuickStart


#### Step1：创建一个Assistant

Assistant 是一个助手的实例，助手可以添加多种参数，包括但不限于
- 名称 `name`
- 模型 `model`
- 人设指令 `instruction`: 概述`Assistant`的整体功能和定位，需要它扮演一个什么样的『角色』
- 思维指令 `thought_instruction`: 与业务逻辑和规则相关的指令。希望模型遵守的行为规范、准则及要求，尽可能清晰、详尽的在这里给出描述
- 对话指令 `chat_instruction`: 与模型最终给出的回复内容相关的指令


以下是一个创建Assistant的示例，更多支持的创建参数参考[Assistant API文档](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben)
```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

assistant = appbuilder.assistant.assistants.create(
				name="my_first_assistant",
				description="你是一个热心肠的朋友，可以回答一些问题",
				instruction="请用亲切的语气回答用户的每一个问题",
			)

```


#### Step2：创建一个Thread

`thread` 代表一组对话，等价为`agent sdk`中的`conversation`，该`thread`对话中存储多组 `user <-> assistant`的对话

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

thread = appbuilder.assistant.threads.create()

```

#### Step3：为Thread添加一个Message

用户或应用程序的消息内容，可以作为消息对象添加到`thread`中。消息可以包含文本`content`及`file_id`。添加到`thread`中的消息，需要遵循一唱一和的 `user问-assistant答` 顺序，并保证最后`thread`的最后一个`message`的`role`为`user`。

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

thread = appbuilder.assistant.threads.create()
message = appbuilder.assistant.threads.messages.create(
	thread_id=thread.id, content="hello world")

```

#### Step4：创建并运行一个Thread.Run
将所有消息都添加到`thread`后，您可以使用`runs`下的方法，创建`run`，并使用相应的`assistant`来生成回复。assistant的回复将被自动添加到`thread`中。

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

assistant = appbuilder.assistant.assistants.create(
				name="my_first_assistant",
				description="你是一个热心肠的朋友，可以回答一些问题",
				instruction="请用亲切的语气回答用户的每一个问题")

thread = appbuilder.assistant.threads.create()

message = appbuilder.assistant.threads.messages.create(
				thread_id=thread.id,
				content="你好",)

run_result = appbuilder.assistant.threads.runs.run(
				thread_id=thread.id,
				assistant_id=assistant.id,
			)
```


## 进阶用法

- [Assistant SDK 数据类型文档](./assistant_type.md)
- [Assistant SDK 基础能力CookBook](./assistant_example.md)

