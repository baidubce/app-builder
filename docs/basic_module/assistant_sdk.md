# AppBuilder Assistant SDK

## 简介

百度智能云千帆 AppBuilder 在提供零代码、低代码的AI原生应用搭建功能之外，也提供全代码灵活开发与集成能力。基于官方 API/SDK，开放丰富的组件服务，提供具备强大对话、思考及工具调用能力的 Agent 应用框架。

封装程度由高至低，提供了三种类型的SDK
| 分类   | 场景及使用方式   | 百度云文档链接         | SDK 文档链接|
|--------|--------|------------|------------|
| 端到端应用 | 在 AppBuilder 产品界面上通过零代码、低代码方式创建的 AI 原生应用，支持通过应用 API/SDK 进行调用 | [应用API及SDK](https://cloud.baidu.com/doc/AppBuilder/s/Plvggbuzc) | [Agent SDK](https://github.com/baidubce/app-builder/blob/master/docs/basic_module/appbuilder_client.md) |
| 代码态智能体 | 基于 Assistants API，可通过全代码形式创建和调试专属智能体（Agent） | [AssistantAPI](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben) | *当前文档* |
| 工具组件 | 基于组件 SDK，可调用包括大模型组件、AI能力组件等在内的多种组件 | [组件SDK](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz) | [组件列表](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#3%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1) |

Assistants API/SDK 正在内测中，敬请期待公测版本。

</span>

### 功能介绍

Assistant SDK允许您在自己的应用程序中，使用纯代码构建人工智能助手。该助手可以利用模型、工具和文件来响应用户的诉求，提供关键的FunctionCall能力。

### 特色优势

与端到端应用相比，Assistants API/SDK 提供了更灵活、更强大的FunctionCall能力，可以满足更复杂的业务场景。基础功能对标 [OpenAI Assistant SDK](https://platform.openai.com/docs/assistants/overview?context=with-streaming)，且会结合国内开发者习惯 与 最广泛的ToB场景，提供更多的易用功能与端到端示例。

### 应用场景

使用SDK纯代码构建Assistant助手，适合有进阶开发能力的开发者。

## 基本用法

以下是使用SDK进行构建的代码示例，更多详细信息请参考[Assistant API文档](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben) 与 [Assistant SDK 数据类型文档](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben)

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
- 人设指令 `instructions`: 概述`Assistant`的整体功能和定位，需要它扮演一个什么样的『角色』
- 思维指令 `thought_instructions`: 与业务逻辑和规则相关的指令。希望模型遵守的行为规范、准则及要求，尽可能清晰、详尽的在这里给出描述
- 对话指令 `chat_instructions`: 与模型最终给出的回复内容相关的指令


以下是一个创建Assistant的示例，更多支持的创建参数参考[Assistant API文档](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben)
```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

assistant = appbuilder.assistant.assistants.create(
				name="my_first_assistant",
				description="你是一个热心肠的朋友，可以回答一些问题",
				instructions="请用亲切的语气回答用户的每一个问题",
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
				instructions="请用亲切的语气回答用户的每一个问题")

thread = appbuilder.assistant.threads.create()

message = appbuilder.assistant.threads.messages.create(
	thread_id=thread.id,
	content="你好",
)

run_result = appbuilder.assistant.threads.runs.run(
	thread_id=thread.id,
	assistant_id=assistant.id,
)
```

### assistant其余功能展示


#### Step1：创建一个Assistant

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

assistant = appbuilder.assistant.assistants.create(
	model = "ERNIE-4.0-8K",
	name="test-assistant",
	description="test",
)
```

#### Step2：查询当前用户创建的Assistant列表

```python
assistants_list = appbuilder.assistant.assistants.list()
```

#### Step3：查询Assistant详情

```python
# 这里的assistant_id为创建的Assistant的id
assistant_query = appbuilder.assistant.assistants.query(assistant_id=assistant.id)
```

#### Step4：更新Assistant

```python
# 更新Assistant的name和description
assistant_update = appbuilder.assistant.assistants.update(
	assistant_id = assistant.id,
	model="ERNIE-4.0-8K",
	name="Test_Name",
	description = "test_description"
)
```

#### Step5：Assistant关于Files的操作

```python
# 上传一个File
file_path = "Your File address"
file = appbuilder.assistant.assistants.files.create(file_path=file_path)

# 挂载File到Assistant
assistant_mount = appbuilder.assistant.assistants.mount_files(
	assistant_id = assistant.id,
	file_id = file.id,
)

# 查询Assistant挂载的File列表
assistant_files_list = appbuilder.assistant.assistants.mounted_files_list(
	assistant_id = assistant.id,
)

# 取消Assistant挂载的File
assistant_files_delete = appbuilder.assistant.assistants.unmount_files(
	assistant_id = assistant.id,
	file_id = file.id,
)
```

#### Step6：删除Assistant

```python
assistant_delete = appbuilder.assistant.assistants.delete(assistant_id=assistant.id)
```

### files其余功能展示


#### Step1：上传一个File

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"
file_path = "Your File address"
file = appbuilder.assistant.assistants.files.create(file_path=file_path)
```

#### Step2：file的相关操作

```python
# 查询已上传的文件列表
files_list = appbuilder.assistant.assistants.files.list()

# 查询已上传的文件信息
files_query = appbuilder.assistant.assistants.files.query(file_id=file.id)

# 下载已上传的文件
# file_path：下载文件保存的地址
file_download = appbuilder.assistant.assistants.files.download(file_id=file.id，file_path="Your File address")

# 查看已上传文件的内容
files_content=appbuilder.assistant.assistants.files.content(file_id=file.id)

# 删除已上传的文件
files_delete = appbuilder.assistant.assistants.files.delete(file_id=file.id)
```

### thread其余功能展示


#### Step1：创建一个Thread

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"
thread = appbuilder.assistant.threads.create()
```

#### Step2：Tread的相关操作

```python
# 根据thread_id查询Thread对象的信息
thr_query = appbuilder.assistant.threads.query(thread_id=thread.id)

# 根据thread_id，对thread进行修改。当前Thread 仅可以修改metadata字段
thr_update = appbuilder.assistant.threads.update(thread_id=thread.id,metadata={"test":"123"})

# 根据thread_id，删除Thread对象
thr_delete = appbuilder.assistant.threads.delete(thread_id=thread.id)
```

### Message其余功能展示

#### Step1：创建一个Message

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"
msg = appbuilder.assistant.threads.messages.create(thread_id=thread.id,content="hello world")
```

#### Step2：Message的相关操作

```python
# 查询指定Thread下的Message列表
# 默认返回20条，limit可以指定返回的条数
msg_list = appbuilder.assistant.threads.messages.list(
	thread_id=msg.thread_id,
	limit=1
) 

# 根据message_id查询Message对象的信息
msg_query = appbuilder.assistant.threads.messages.query(
	thread_id=msg.thread_id,
	message_id=msg.id
)

# 根据message_id，对Message进行修改。当前Message 允许content和file_ids字段
msg_update= appbuilder.assistant.threads.messages.update(
	thread_id=msg.thread_id,
	message_id=msg.id,
	content='你好'
)

# 查询一个Message对象下的文件列表
# 默认返回20条，limit可以指定返回的条数
msg_files = appbuilder.assistant.threads.messages.files(
	thread_id=msg_update.thread_id,
	message_id=msg_update.id,
	limit=1
)
```


## 进阶用法

- [Assistant SDK 数据类型文档](https://cloud.baidu.com/doc/AppBuilder/s/nluzkdben)
- [Assistant SDK 基础能力CookBook](https://github.com/baidubce/app-builder/blob/master/cookbooks/README.md)

