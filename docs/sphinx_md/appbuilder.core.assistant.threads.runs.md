# appbuilder.core.assistant.threads.runs package

## Submodules

## appbuilder.core.assistant.threads.runs.runs module

### *class* appbuilder.core.assistant.threads.runs.runs.Runs

基类：`object`

#### cancel(run_id: str, thread_id: str) → RunResult

取消指定线程的运行

* **参数:**
  * **run_id** (*str*) – 运行的ID
  * **thread_id** (*str*) – 线程的ID
* **返回:**
  取消运行的结果
* **返回类型:**
  thread_type.RunResult

#### list(thread_id: str, limit: int = 20, order: str = 'desc', after: str = '', before: str = '') → RunListResponse

列出对应thread的历史run记录

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **limit** (*int* *,* *optional*) – 列表数量限制，默认为20
  * **order** (*str* *,* *optional*) – 排序方式，’asc’为升序，’desc’为降序，默认为’desc’
  * **after** (*str* *,* *optional*) – 返回在指定时间之后的运行列表，默认为空字符串
  * **before** (*str* *,* *optional*) – 返回在指定时间之前的运行列表，默认为空字符串
* **返回:**
  列出对应thread的历史run记录
* **返回类型:**
  thread_type.RunListResponse
* **抛出:**
  **无** – 

#### query(thread_id: str, run_id: str) → RunResult

根据thread_id和run_id，查询run的详情

* **参数:**
  * **thread_id** (*str*) – 线程ID。
  * **run_id** (*str*) – 运行ID。
* **返回:**
  查询到的运行结果。
* **返回类型:**
  thread_type.RunResult

#### run(assistant_id: str, thread_id: str | None = '', thread: AssistantThread | None = None, model: str | None = None, response_format: str | None = 'text', instructions: str | None = '', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], metadata: dict | None = {}, tool_output: ToolOutput | None = None, model_parameters: AssistantModelParameters | None = None, user_info: AssistantUserInfo | None = None, user_loc: AssistantUserLoc | None = None) → RunResult

* **参数:**
  * **assistant_id** (*str*) – 助手id
  * **thread_id** (*Optional* *[**str* *]* *,* *optional*) – 对话id. Defaults to “”.
  * **thread** (*Optional* *[**thread_type.AssistantThread* *]* *,* *optional*) – 对话信息. Defaults to None.
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 模型名称. Defaults to None.
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 返回格式. Defaults to “text”.
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 指令信息. Defaults to “”.
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思考指令信息. Defaults to “”.
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 闲聊指令信息. Defaults to “”.
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 工具列表. Defaults to [].
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据. Defaults to {}.
  * **tool_output** (*Optional* *[**thread_type.ToolOutput* *]* *,* *optional*) – 工具输出. Defaults to None.
  * **model_parameters** (*Optional* *[**public_type.AssistantModelParameters* *]* *,* *optional*) – 模型运行参数. Defaults to None.
  * **user_info** (*Optional* *[**public_type.AssistantUserInfo* *]* *,* *optional*) – 用户身份信息. Defaults to None.
  * **user_loc** (*Optional* *[**public_type.AssistantUserLoc* *]* *,* *optional*) – 用户定位信息. Defaults to None.
* **返回:**
  运行结果
* **返回类型:**
  thread_type.RunResult
* **抛出:**
  **ValueError** – thread_id和thread不能同时为空,model_parameters的各个参数不在规定范围内

#### NOTE
1. 如果thread_id没有传，则thread必须要传值
2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user

#### *property* steps *: [Steps](#appbuilder.core.assistant.threads.runs.steps.Steps)*

#### stream_run(assistant_id: str, thread_id: str | None = '', thread: AssistantThread | None = None, model: str | None = None, response_format: str | None = 'text', instructions: str | None = '', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], metadata: dict | None = {}, tool_output: ToolOutput | None = None, model_parameters: AssistantModelParameters | None = None, user_info: AssistantUserInfo | None = None, user_loc: AssistantUserLoc | None = None) → StreamRunStatus | StreamRunMessage | None

启动一个流式运行的对话，用于处理对话流中的消息。

* **参数:**
  * **assistant_id** (*str*) – 助理ID。
  * **thread_id** (*Optional* *[**str* *]* *,* *optional*) – 线程ID，用于恢复历史对话。默认为空字符串。
  * **thread** (*Optional* *[**thread_type.AssistantThread* *]* *,* *optional*) – 线程对象，用于恢复历史对话。默认为None。
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 使用的模型名称。默认为None。
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 响应格式，支持”text”和”json”两种格式。默认为”text”。
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 指令文本。默认为空字符串。
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思考指令文本。默认为空字符串。
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 聊天指令文本。默认为空字符串。
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 使用的工具列表。默认为空列表。
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据字典。默认为空字典。
  * **tool_output** (*Optional* *[**thread_type.ToolOutput* *]* *,* *optional*) – 工具输出对象。默认为None。
  * **model_parameters** (*Optional* *[**public_type.AssistantModelParameters* *]* *,* *optional*) – 模型参数对象。默认为None。
* **返回:**
  返回一个迭代器，每次迭代返回一个处理结果对象，可能是 StreamRunStatus 或 StreamRunMessage。
* **返回类型:**
  Union[thread_type.StreamRunStatus, thread_type.StreamRunMessage, None]
* **抛出:**
  **ValueError** – 如果thread_id和thread参数同时为空，则会引发ValueError异常。

#### NOTE
1. 如果thread_id没有传，则thread必须要传值。
2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user。
3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user。

#### stream_run_with_handler(assistant_id: str, thread_id: str | None = '', thread: AssistantThread | None = None, model: str | None = None, response_format: str | None = 'text', instructions: str | None = '', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], metadata: dict | None = {}, tool_output: ToolOutput | None = None, event_handler: [AssistantEventHandler](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler) | None = None, model_parameters: AssistantModelParameters | None = None, user_info: AssistantUserInfo | None = None, user_loc: AssistantUserLoc | None = None) → [AssistantStreamManager](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantStreamManager)

使用带有事件处理器的流运行助手

* **参数:**
  * **assistant_id** (*str*) – 助手的唯一标识符
  * **thread_id** (*Optional* *[**str* *]* *,* *optional*) – 会话线程的标识符，默认为空字符串. 默认为 “”.
  * **thread** (*Optional* *[**thread_type.AssistantThread* *]* *,* *optional*) – 会话线程对象，默认为None. 默认为 None.
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 模型标识符，默认为None. 默认为 None.
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 响应格式，可选值为”text”或”json”，默认为”text”. 默认为 “text”.
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 主要指令，默认为空字符串. 默认为 “”.
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思维指令，默认为空字符串. 默认为 “”.
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 聊天指令，默认为空字符串. 默认为 “”.
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 助手工具列表，默认为空列表. 默认为 [].
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据字典，默认为空字典. 默认为 {}.
  * **tool_output** (*Optional* *[**thread_type.ToolOutput* *]* *,* *optional*) – 工具输出对象，默认为None. 默认为 None.
  * **event_handler** (*Optional* *[*[*AssistantEventHandler*](appbuilder.md#appbuilder.AssistantEventHandler) *]* *,* *optional*) – 事件处理器对象，默认为None. 默认为 None.
  * **model_parameters** (*Optional* *[**public_type.AssistantModelParameters* *]* *,* *optional*) – 模型参数对象，默认为None. 默认为 None.
  * **user_info** (*Optional* *[**public_type.AssistantUserInfo* *]* *,* *optional*) – 用户信息对象，默认为None. 默认为 None.
  * **user_loc** (*Optional* *[**public_type.AssistantUserLoc* *]* *,* *optional*) – 用户位置信息对象，默认为None. 默认为 None.
* **返回:**
  返回的流管理器对象
* **返回类型:**
  [AssistantStreamManager](appbuilder.md#appbuilder.AssistantStreamManager)
* **抛出:**
  **HTTPError** – 如果HTTP响应状态码不为200，则抛出HTTPError异常

#### submit_tool_outputs(run_id: str, thread_id: str, tool_outputs: list[ToolOutput] | None) → RunResult

向服务端提交工具输出

* **参数:**
  * **run_id** (*str*) – 运行ID
  * **thread_id** (*str*) – 线程ID
  * **tool_outputs** (*Optional* *[**list* *[**thread_type.ToolOutput* *]* *]*) – 工具输出列表，可选
* **返回:**
  运行结果
* **返回类型:**
  thread_type.RunResult

## appbuilder.core.assistant.threads.runs.steps module

### *class* appbuilder.core.assistant.threads.runs.steps.Steps

基类：`object`

#### list(thread_id: str, run_id: str, limit: int = 20, order: str = 'desc', after: str = '', before: str = '') → RunStepListResponse

根据thread_id和run_id，列出对应run的历史step记录

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **run_id** (*str*) – 运行ID
  * **limit** (*int* *,* *optional*) – 步骤数量限制，默认为20
  * **order** (*str* *,* *optional*) – 排序方式，’asc’表示升序，’desc’表示降序，默认为’desc’
  * **after** (*str* *,* *optional*) – 过滤出时间戳晚于此值的步骤，默认为空
  * **before** (*str* *,* *optional*) – 过滤出时间戳早于此值的步骤，默认为空
* **返回:**
  线程运行步骤列表的响应对象
* **返回类型:**
  thread_type.RunStepListResponse

#### query(thread_id: str, run_id: str, step_id: str) → RunStepResult

根据thread_id，run_id和step_id，查询对应step的信息

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **run_id** (*str*) – 运行ID
  * **step_id** (*str*) – 步骤ID
* **返回:**
  步骤运行结果
* **返回类型:**
  thread_type.RunStepResult

## appbuilder.core.assistant.threads.runs.stream_helper module

### *class* appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler

基类：`object`

AssistantEventHandler类用于处理Assistant流式返回的相关事件。

这个类作为Assistant流式事件的处理中心，负责接收和处理来自Assistant的各种事件，
如用户交互、数据更新、状态变化等。通过实现不同的事件处理方法，
可以定义Assistant在不同事件下的行为逻辑。

Assistant事件处理程序通常与具体的Assistant实例相关联，用于管理和控制Assistant的运行流程，
以及与其他系统组件的交互。

该类包含多个方法，每个方法对应一种特定事件的处理逻辑。
当相应的事件发生时，Assistant或相关系统会调用这些方法，以执行预定义的操作。

通过继承AssistantEventHandler类并重写其方法，可以实现自定义的Assistant流式事件处理逻辑，
从而满足特定的业务需求。

#### message_creation(status_event: StreamRunStatus)

#### messages(messages_event: StreamRunMessage)

#### run_begin(status_event: StreamRunStatus)

#### run_cancelling(status_event: StreamRunStatus)

#### run_end(status_event: StreamRunStatus)

#### tool_calls(status_event: StreamRunStatus)

#### tool_step_begin(status_event: StreamRunStatus)

#### tool_step_end(status_event: StreamRunStatus)

#### tool_submitted_output(status_event: StreamRunStatus)

#### until_done()

### *class* appbuilder.core.assistant.threads.runs.stream_helper.AssistantStreamManager(response, event_handler: [AssistantEventHandler](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler))

基类：[`AssistantEventHandler`](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler)

### *class* appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext

基类：`object`

StreamRunContext类用于管理和维护流式运行时的上下文信息。

这个类提供了存储和获取当前流事件、工具调用、运行ID、运行步骤ID、线程ID和助手ID等属性的功能。
通过创建StreamRunContext的实例，可以方便地跟踪和处理流式运行时的各种状态和数据。

#### current_event

当前流事件的对象。

#### current_tool_calls

当前工具调用的相关信息。

#### current_run_id

当前运行的唯一标识符。

#### current_run_step_id

当前运行步骤的唯一标识符。

#### current_thread_id

当前线程的唯一标识符。

#### current_assistant_id

当前助手的唯一标识符。

#### NOTE
这个类通常作为其他流式处理类（如StreamProcessor、StreamHandler等）的组成部分，
用于在流式处理过程中传递和共享上下文信息。

#### *property* current_assistant_id *: str | None*

#### *property* current_event *: StreamRunStatus | StreamRunMessage | None*

#### *property* current_run_id *: str | None*

#### *property* current_run_step_id *: str | None*

#### *property* current_thread_id *: str | None*

#### *property* current_tool_calls *: list[ToolCall] | None*

#### reset_step_context()

#### set_current_assistant_id(assistant_id)

#### set_current_event(event)

#### set_current_run_id(run_id)

#### set_current_run_step_id(run_step_id)

#### set_current_thread_id(thread_id)

#### set_current_tool_calls(tool_calls)

## Module contents

### *class* appbuilder.core.assistant.threads.runs.AssistantEventHandler

基类：`object`

AssistantEventHandler类用于处理Assistant流式返回的相关事件。

这个类作为Assistant流式事件的处理中心，负责接收和处理来自Assistant的各种事件，
如用户交互、数据更新、状态变化等。通过实现不同的事件处理方法，
可以定义Assistant在不同事件下的行为逻辑。

Assistant事件处理程序通常与具体的Assistant实例相关联，用于管理和控制Assistant的运行流程，
以及与其他系统组件的交互。

该类包含多个方法，每个方法对应一种特定事件的处理逻辑。
当相应的事件发生时，Assistant或相关系统会调用这些方法，以执行预定义的操作。

通过继承AssistantEventHandler类并重写其方法，可以实现自定义的Assistant流式事件处理逻辑，
从而满足特定的业务需求。

#### message_creation(status_event: StreamRunStatus)

#### messages(messages_event: StreamRunMessage)

#### run_begin(status_event: StreamRunStatus)

#### run_cancelling(status_event: StreamRunStatus)

#### run_end(status_event: StreamRunStatus)

#### tool_calls(status_event: StreamRunStatus)

#### tool_step_begin(status_event: StreamRunStatus)

#### tool_step_end(status_event: StreamRunStatus)

#### tool_submitted_output(status_event: StreamRunStatus)

#### until_done()

### *class* appbuilder.core.assistant.threads.runs.AssistantStreamManager(response, event_handler: [AssistantEventHandler](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler))

基类：[`AssistantEventHandler`](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler)

### *class* appbuilder.core.assistant.threads.runs.Runs

基类：`object`

#### cancel(run_id: str, thread_id: str) → RunResult

取消指定线程的运行

* **参数:**
  * **run_id** (*str*) – 运行的ID
  * **thread_id** (*str*) – 线程的ID
* **返回:**
  取消运行的结果
* **返回类型:**
  thread_type.RunResult

#### list(thread_id: str, limit: int = 20, order: str = 'desc', after: str = '', before: str = '') → RunListResponse

列出对应thread的历史run记录

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **limit** (*int* *,* *optional*) – 列表数量限制，默认为20
  * **order** (*str* *,* *optional*) – 排序方式，’asc’为升序，’desc’为降序，默认为’desc’
  * **after** (*str* *,* *optional*) – 返回在指定时间之后的运行列表，默认为空字符串
  * **before** (*str* *,* *optional*) – 返回在指定时间之前的运行列表，默认为空字符串
* **返回:**
  列出对应thread的历史run记录
* **返回类型:**
  thread_type.RunListResponse
* **抛出:**
  **无** – 

#### query(thread_id: str, run_id: str) → RunResult

根据thread_id和run_id，查询run的详情

* **参数:**
  * **thread_id** (*str*) – 线程ID。
  * **run_id** (*str*) – 运行ID。
* **返回:**
  查询到的运行结果。
* **返回类型:**
  thread_type.RunResult

#### run(assistant_id: str, thread_id: str | None = '', thread: AssistantThread | None = None, model: str | None = None, response_format: str | None = 'text', instructions: str | None = '', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], metadata: dict | None = {}, tool_output: ToolOutput | None = None, model_parameters: AssistantModelParameters | None = None, user_info: AssistantUserInfo | None = None, user_loc: AssistantUserLoc | None = None) → RunResult

* **参数:**
  * **assistant_id** (*str*) – 助手id
  * **thread_id** (*Optional* *[**str* *]* *,* *optional*) – 对话id. Defaults to “”.
  * **thread** (*Optional* *[**thread_type.AssistantThread* *]* *,* *optional*) – 对话信息. Defaults to None.
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 模型名称. Defaults to None.
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 返回格式. Defaults to “text”.
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 指令信息. Defaults to “”.
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思考指令信息. Defaults to “”.
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 闲聊指令信息. Defaults to “”.
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 工具列表. Defaults to [].
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据. Defaults to {}.
  * **tool_output** (*Optional* *[**thread_type.ToolOutput* *]* *,* *optional*) – 工具输出. Defaults to None.
  * **model_parameters** (*Optional* *[**public_type.AssistantModelParameters* *]* *,* *optional*) – 模型运行参数. Defaults to None.
  * **user_info** (*Optional* *[**public_type.AssistantUserInfo* *]* *,* *optional*) – 用户身份信息. Defaults to None.
  * **user_loc** (*Optional* *[**public_type.AssistantUserLoc* *]* *,* *optional*) – 用户定位信息. Defaults to None.
* **返回:**
  运行结果
* **返回类型:**
  thread_type.RunResult
* **抛出:**
  **ValueError** – thread_id和thread不能同时为空,model_parameters的各个参数不在规定范围内

#### NOTE
1. 如果thread_id没有传，则thread必须要传值
2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user

#### *property* steps *: [Steps](#appbuilder.core.assistant.threads.runs.steps.Steps)*

#### stream_run(assistant_id: str, thread_id: str | None = '', thread: AssistantThread | None = None, model: str | None = None, response_format: str | None = 'text', instructions: str | None = '', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], metadata: dict | None = {}, tool_output: ToolOutput | None = None, model_parameters: AssistantModelParameters | None = None, user_info: AssistantUserInfo | None = None, user_loc: AssistantUserLoc | None = None) → StreamRunStatus | StreamRunMessage | None

启动一个流式运行的对话，用于处理对话流中的消息。

* **参数:**
  * **assistant_id** (*str*) – 助理ID。
  * **thread_id** (*Optional* *[**str* *]* *,* *optional*) – 线程ID，用于恢复历史对话。默认为空字符串。
  * **thread** (*Optional* *[**thread_type.AssistantThread* *]* *,* *optional*) – 线程对象，用于恢复历史对话。默认为None。
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 使用的模型名称。默认为None。
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 响应格式，支持”text”和”json”两种格式。默认为”text”。
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 指令文本。默认为空字符串。
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思考指令文本。默认为空字符串。
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 聊天指令文本。默认为空字符串。
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 使用的工具列表。默认为空列表。
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据字典。默认为空字典。
  * **tool_output** (*Optional* *[**thread_type.ToolOutput* *]* *,* *optional*) – 工具输出对象。默认为None。
  * **model_parameters** (*Optional* *[**public_type.AssistantModelParameters* *]* *,* *optional*) – 模型参数对象。默认为None。
* **返回:**
  返回一个迭代器，每次迭代返回一个处理结果对象，可能是 StreamRunStatus 或 StreamRunMessage。
* **返回类型:**
  Union[thread_type.StreamRunStatus, thread_type.StreamRunMessage, None]
* **抛出:**
  **ValueError** – 如果thread_id和thread参数同时为空，则会引发ValueError异常。

#### NOTE
1. 如果thread_id没有传，则thread必须要传值。
2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user。
3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user。

#### stream_run_with_handler(assistant_id: str, thread_id: str | None = '', thread: AssistantThread | None = None, model: str | None = None, response_format: str | None = 'text', instructions: str | None = '', thought_instructions: str | None = '', chat_instructions: str | None = '', tools: list[AssistantTool] | None = [], metadata: dict | None = {}, tool_output: ToolOutput | None = None, event_handler: [AssistantEventHandler](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler) | None = None, model_parameters: AssistantModelParameters | None = None, user_info: AssistantUserInfo | None = None, user_loc: AssistantUserLoc | None = None) → [AssistantStreamManager](#appbuilder.core.assistant.threads.runs.stream_helper.AssistantStreamManager)

使用带有事件处理器的流运行助手

* **参数:**
  * **assistant_id** (*str*) – 助手的唯一标识符
  * **thread_id** (*Optional* *[**str* *]* *,* *optional*) – 会话线程的标识符，默认为空字符串. 默认为 “”.
  * **thread** (*Optional* *[**thread_type.AssistantThread* *]* *,* *optional*) – 会话线程对象，默认为None. 默认为 None.
  * **model** (*Optional* *[**str* *]* *,* *optional*) – 模型标识符，默认为None. 默认为 None.
  * **response_format** (*Optional* *[**str* *]* *,* *optional*) – 响应格式，可选值为”text”或”json”，默认为”text”. 默认为 “text”.
  * **instructions** (*Optional* *[**str* *]* *,* *optional*) – 主要指令，默认为空字符串. 默认为 “”.
  * **thought_instructions** (*Optional* *[**str* *]* *,* *optional*) – 思维指令，默认为空字符串. 默认为 “”.
  * **chat_instructions** (*Optional* *[**str* *]* *,* *optional*) – 聊天指令，默认为空字符串. 默认为 “”.
  * **tools** (*Optional* *[**list* *[**assistant_type.AssistantTool* *]* *]* *,* *optional*) – 助手工具列表，默认为空列表. 默认为 [].
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 元数据字典，默认为空字典. 默认为 {}.
  * **tool_output** (*Optional* *[**thread_type.ToolOutput* *]* *,* *optional*) – 工具输出对象，默认为None. 默认为 None.
  * **event_handler** (*Optional* *[*[*AssistantEventHandler*](#appbuilder.core.assistant.threads.runs.AssistantEventHandler) *]* *,* *optional*) – 事件处理器对象，默认为None. 默认为 None.
  * **model_parameters** (*Optional* *[**public_type.AssistantModelParameters* *]* *,* *optional*) – 模型参数对象，默认为None. 默认为 None.
  * **user_info** (*Optional* *[**public_type.AssistantUserInfo* *]* *,* *optional*) – 用户信息对象，默认为None. 默认为 None.
  * **user_loc** (*Optional* *[**public_type.AssistantUserLoc* *]* *,* *optional*) – 用户位置信息对象，默认为None. 默认为 None.
* **返回:**
  返回的流管理器对象
* **返回类型:**
  [AssistantStreamManager](#appbuilder.core.assistant.threads.runs.AssistantStreamManager)
* **抛出:**
  **HTTPError** – 如果HTTP响应状态码不为200，则抛出HTTPError异常

#### submit_tool_outputs(run_id: str, thread_id: str, tool_outputs: list[ToolOutput] | None) → RunResult

向服务端提交工具输出

* **参数:**
  * **run_id** (*str*) – 运行ID
  * **thread_id** (*str*) – 线程ID
  * **tool_outputs** (*Optional* *[**list* *[**thread_type.ToolOutput* *]* *]*) – 工具输出列表，可选
* **返回:**
  运行结果
* **返回类型:**
  thread_type.RunResult

### *class* appbuilder.core.assistant.threads.runs.Steps

基类：`object`

#### list(thread_id: str, run_id: str, limit: int = 20, order: str = 'desc', after: str = '', before: str = '') → RunStepListResponse

根据thread_id和run_id，列出对应run的历史step记录

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **run_id** (*str*) – 运行ID
  * **limit** (*int* *,* *optional*) – 步骤数量限制，默认为20
  * **order** (*str* *,* *optional*) – 排序方式，’asc’表示升序，’desc’表示降序，默认为’desc’
  * **after** (*str* *,* *optional*) – 过滤出时间戳晚于此值的步骤，默认为空
  * **before** (*str* *,* *optional*) – 过滤出时间戳早于此值的步骤，默认为空
* **返回:**
  线程运行步骤列表的响应对象
* **返回类型:**
  thread_type.RunStepListResponse

#### query(thread_id: str, run_id: str, step_id: str) → RunStepResult

根据thread_id，run_id和step_id，查询对应step的信息

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **run_id** (*str*) – 运行ID
  * **step_id** (*str*) – 步骤ID
* **返回:**
  步骤运行结果
* **返回类型:**
  thread_type.RunStepResult

### *class* appbuilder.core.assistant.threads.runs.StreamRunContext

基类：`object`

StreamRunContext类用于管理和维护流式运行时的上下文信息。

这个类提供了存储和获取当前流事件、工具调用、运行ID、运行步骤ID、线程ID和助手ID等属性的功能。
通过创建StreamRunContext的实例，可以方便地跟踪和处理流式运行时的各种状态和数据。

#### current_event

当前流事件的对象。

#### current_tool_calls

当前工具调用的相关信息。

#### current_run_id

当前运行的唯一标识符。

#### current_run_step_id

当前运行步骤的唯一标识符。

#### current_thread_id

当前线程的唯一标识符。

#### current_assistant_id

当前助手的唯一标识符。

#### NOTE
这个类通常作为其他流式处理类（如StreamProcessor、StreamHandler等）的组成部分，
用于在流式处理过程中传递和共享上下文信息。

#### *property* current_assistant_id *: str | None*

#### *property* current_event *: StreamRunStatus | StreamRunMessage | None*

#### *property* current_run_id *: str | None*

#### *property* current_run_step_id *: str | None*

#### *property* current_thread_id *: str | None*

#### *property* current_tool_calls *: list[ToolCall] | None*

#### reset_step_context()

#### set_current_assistant_id(assistant_id)

#### set_current_event(event)

#### set_current_run_id(run_id)

#### set_current_run_step_id(run_step_id)

#### set_current_thread_id(thread_id)

#### set_current_tool_calls(tool_calls)