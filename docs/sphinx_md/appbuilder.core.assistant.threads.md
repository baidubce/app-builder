# appbuilder.core.assistant.threads package

## Subpackages

* [appbuilder.core.assistant.threads.messages package](appbuilder.core.assistant.threads.messages.md)
  * [Submodules](appbuilder.core.assistant.threads.messages.md#submodules)
  * [appbuilder.core.assistant.threads.messages.messages module](appbuilder.core.assistant.threads.messages.md#module-appbuilder.core.assistant.threads.messages.messages)
    * [`Messages`](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages)
      * [`Messages.create()`](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages.create)
      * [`Messages.files()`](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages.files)
      * [`Messages.list()`](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages.list)
      * [`Messages.query()`](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages.query)
      * [`Messages.update()`](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages.update)
* [appbuilder.core.assistant.threads.runs package](appbuilder.core.assistant.threads.runs.md)
  * [Submodules](appbuilder.core.assistant.threads.runs.md#submodules)
  * [appbuilder.core.assistant.threads.runs.runs module](appbuilder.core.assistant.threads.runs.md#module-appbuilder.core.assistant.threads.runs.runs)
    * [`Runs`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs)
      * [`Runs.cancel()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.cancel)
      * [`Runs.list()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.list)
      * [`Runs.query()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.query)
      * [`Runs.run()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.run)
      * [`Runs.steps`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.steps)
      * [`Runs.stream_run()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.stream_run)
      * [`Runs.stream_run_with_handler()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.stream_run_with_handler)
      * [`Runs.submit_tool_outputs()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs.submit_tool_outputs)
  * [appbuilder.core.assistant.threads.runs.steps module](appbuilder.core.assistant.threads.runs.md#module-appbuilder.core.assistant.threads.runs.steps)
    * [`Steps`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.steps.Steps)
      * [`Steps.list()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.steps.Steps.list)
      * [`Steps.query()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.steps.Steps.query)
  * [appbuilder.core.assistant.threads.runs.stream_helper module](appbuilder.core.assistant.threads.runs.md#module-appbuilder.core.assistant.threads.runs.stream_helper)
    * [`AssistantEventHandler`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler)
      * [`AssistantEventHandler.message_creation()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.message_creation)
      * [`AssistantEventHandler.messages()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.messages)
      * [`AssistantEventHandler.run_begin()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.run_begin)
      * [`AssistantEventHandler.run_cancelling()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.run_cancelling)
      * [`AssistantEventHandler.run_end()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.run_end)
      * [`AssistantEventHandler.tool_calls()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.tool_calls)
      * [`AssistantEventHandler.tool_step_begin()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.tool_step_begin)
      * [`AssistantEventHandler.tool_step_end()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.tool_step_end)
      * [`AssistantEventHandler.tool_submitted_output()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.tool_submitted_output)
      * [`AssistantEventHandler.until_done()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler.until_done)
    * [`AssistantStreamManager`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantStreamManager)
    * [`StreamRunContext`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext)
      * [`StreamRunContext.current_event`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.current_event)
      * [`StreamRunContext.current_tool_calls`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.current_tool_calls)
      * [`StreamRunContext.current_run_id`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.current_run_id)
      * [`StreamRunContext.current_run_step_id`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.current_run_step_id)
      * [`StreamRunContext.current_thread_id`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.current_thread_id)
      * [`StreamRunContext.current_assistant_id`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.current_assistant_id)
      * [`StreamRunContext.current_assistant_id`](appbuilder.core.assistant.threads.runs.md#id0)
      * [`StreamRunContext.current_event`](appbuilder.core.assistant.threads.runs.md#id1)
      * [`StreamRunContext.current_run_id`](appbuilder.core.assistant.threads.runs.md#id2)
      * [`StreamRunContext.current_run_step_id`](appbuilder.core.assistant.threads.runs.md#id3)
      * [`StreamRunContext.current_thread_id`](appbuilder.core.assistant.threads.runs.md#id4)
      * [`StreamRunContext.current_tool_calls`](appbuilder.core.assistant.threads.runs.md#id5)
      * [`StreamRunContext.reset_step_context()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.reset_step_context)
      * [`StreamRunContext.set_current_assistant_id()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.set_current_assistant_id)
      * [`StreamRunContext.set_current_event()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.set_current_event)
      * [`StreamRunContext.set_current_run_id()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.set_current_run_id)
      * [`StreamRunContext.set_current_run_step_id()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.set_current_run_step_id)
      * [`StreamRunContext.set_current_thread_id()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.set_current_thread_id)
      * [`StreamRunContext.set_current_tool_calls()`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.StreamRunContext.set_current_tool_calls)

## Submodules

## appbuilder.core.assistant.threads.threads module

### *class* appbuilder.core.assistant.threads.threads.Threads

基类：`object`

#### create(messages: list[AssistantMessage] | None = []) → ThreadCreateResponse

创建一个新的对话线程。

* **参数:**
  **messages** – 要发送给助手的消息列表。如果不传入此参数，则会创建一个空对话线程。
* **返回:**
  一个ThreadCreateResponse对象，包含新创建的线程的相关信息。
* **抛出:**
  **ValueError** – 如果传入的messages参数不是列表类型。

#### delete(thread_id: str) → ThreadDeleteResponse

删除对话线程。
:param thread_id: 要删除的对话线程ID。

* **返回:**
  一个ThreadDeleteResponse对象，包含对话线程的相关信息。
* **抛出:**
  **ValueError** – 如果传入的thread_id参数不是字符串类型。

#### *property* messages *: [Messages](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages)*

获取消息实例

* **参数:**
  **无**
* **返回:**
  返回Messages实例
* **返回类型:**
  [Messages](appbuilder.core.assistant.threads.messages.md#appbuilder.core.assistant.threads.messages.messages.Messages)

#### query(thread_id: str) → ThreadQueryResponse

查询对话线程信息。

* **参数:**
  **thread_id** – 要查询的对话线程ID。
* **返回:**
  一个ThreadQueryResponse对象，包含对话线程的相关信息。
* **抛出:**
  **ValueError** – 如果传入的thread_id参数不是字符串类型。

#### *property* runs *: [Runs](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs)*

返回Runs对象。

* **参数:**
  **无**
* **返回:**
  一个Runs对象实例。
* **返回类型:**
  [Runs](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.runs.Runs)

#### update(thread_id: str, metadata: dict | None = {}) → ThreadUpdateResponse

更新线程信息

* **参数:**
  * **thread_id** (*str*) – 线程ID
  * **metadata** (*Optional* *[**dict* *]* *,* *optional*) – 线程元数据. 默认为空字典.
* **返回:**
  线程更新响应
* **返回类型:**
  thread_type.ThreadUpdateResponse
* **抛出:**
  * **TypeError** – 如果metadata不是字典类型
  * **ValueError** – 如果metadata的键超过64个字符或值超过512个字符
