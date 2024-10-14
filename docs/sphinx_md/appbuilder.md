# appbuilder package

## Subpackages

* [appbuilder.core package](appbuilder.core.md)
  * [Subpackages](appbuilder.core.md#subpackages)
    * [appbuilder.core.assistant package](appbuilder.core.assistant.md)
      * [Subpackages](appbuilder.core.assistant.md#subpackages)
      * [Submodules](appbuilder.core.assistant.md#submodules)
      * [Module contents](appbuilder.core.assistant.md#module-appbuilder.core.assistant)
    * [appbuilder.core.components package](appbuilder.core.components.md)
      * [Subpackages](appbuilder.core.components.md#subpackages)
      * [Module contents](appbuilder.core.components.md#module-appbuilder.core.components)
    * [appbuilder.core.console package](appbuilder.core.console.md)
      * [Subpackages](appbuilder.core.console.md#subpackages)
      * [Submodules](appbuilder.core.console.md#submodules)
      * [Module contents](appbuilder.core.console.md#module-appbuilder.core.console)
  * [Submodules](appbuilder.core.md#submodules)
  * [appbuilder.core.agent module](appbuilder.core.md#module-appbuilder.core.agent)
    * [`AgentRuntime`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime)
      * [`AgentRuntime.Config`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.Config)
      * [`AgentRuntime.chainlit_agent()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.chainlit_agent)
      * [`AgentRuntime.chainlit_demo()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.chainlit_demo)
      * [`AgentRuntime.chat()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.chat)
      * [`AgentRuntime.component`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.component)
      * [`AgentRuntime.create_flask_app()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.create_flask_app)
      * [`AgentRuntime.init()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.init)
      * [`AgentRuntime.model_computed_fields`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.model_computed_fields)
      * [`AgentRuntime.model_config`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.model_config)
      * [`AgentRuntime.model_fields`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.model_fields)
      * [`AgentRuntime.prepare_chainlit_readme()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.prepare_chainlit_readme)
      * [`AgentRuntime.serve()`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.serve)
      * [`AgentRuntime.user_session`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.user_session)
      * [`AgentRuntime.user_session_config`](appbuilder.core.md#appbuilder.core.agent.AgentRuntime.user_session_config)
  * [appbuilder.core.component module](appbuilder.core.md#module-appbuilder.core.component)
    * [`Component`](appbuilder.core.md#appbuilder.core.component.Component)
      * [`Component.abatch()`](appbuilder.core.md#appbuilder.core.component.Component.abatch)
      * [`Component.arun()`](appbuilder.core.md#appbuilder.core.component.Component.arun)
      * [`Component.batch()`](appbuilder.core.md#appbuilder.core.component.Component.batch)
      * [`Component.create_langchain_tool()`](appbuilder.core.md#appbuilder.core.component.Component.create_langchain_tool)
      * [`Component.http_client`](appbuilder.core.md#appbuilder.core.component.Component.http_client)
      * [`Component.manifests`](appbuilder.core.md#appbuilder.core.component.Component.manifests)
      * [`Component.run()`](appbuilder.core.md#appbuilder.core.component.Component.run)
      * [`Component.set_secret_key_and_gateway()`](appbuilder.core.md#appbuilder.core.component.Component.set_secret_key_and_gateway)
      * [`Component.tool_desc()`](appbuilder.core.md#appbuilder.core.component.Component.tool_desc)
      * [`Component.tool_eval()`](appbuilder.core.md#appbuilder.core.component.Component.tool_eval)
      * [`Component.tool_name()`](appbuilder.core.md#appbuilder.core.component.Component.tool_name)
    * [`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)
      * [`ComponentArguments.extract_values_to_dict()`](appbuilder.core.md#appbuilder.core.component.ComponentArguments.extract_values_to_dict)
      * [`ComponentArguments.model_computed_fields`](appbuilder.core.md#appbuilder.core.component.ComponentArguments.model_computed_fields)
      * [`ComponentArguments.model_config`](appbuilder.core.md#appbuilder.core.component.ComponentArguments.model_config)
      * [`ComponentArguments.model_fields`](appbuilder.core.md#appbuilder.core.component.ComponentArguments.model_fields)
      * [`ComponentArguments.name`](appbuilder.core.md#appbuilder.core.component.ComponentArguments.name)
      * [`ComponentArguments.tool_desc`](appbuilder.core.md#appbuilder.core.component.ComponentArguments.tool_desc)
  * [appbuilder.core.constants module](appbuilder.core.md#module-appbuilder.core.constants)
  * [appbuilder.core.context module](appbuilder.core.md#module-appbuilder.core.context)
    * [`SessionContext`](appbuilder.core.md#appbuilder.core.context.SessionContext)
      * [`SessionContext.id`](appbuilder.core.md#appbuilder.core.context.SessionContext.id)
      * [`SessionContext.request_id`](appbuilder.core.md#appbuilder.core.context.SessionContext.request_id)
      * [`SessionContext.session_id`](appbuilder.core.md#appbuilder.core.context.SessionContext.session_id)
      * [`SessionContext.session_vars_dict`](appbuilder.core.md#appbuilder.core.context.SessionContext.session_vars_dict)
      * [`SessionContext.user_id`](appbuilder.core.md#appbuilder.core.context.SessionContext.user_id)
    * [`get_context()`](appbuilder.core.md#appbuilder.core.context.get_context)
    * [`init_context()`](appbuilder.core.md#appbuilder.core.context.init_context)
  * [appbuilder.core.functional module](appbuilder.core.md#module-appbuilder.core.functional)
  * [appbuilder.core.message module](appbuilder.core.md#module-appbuilder.core.message)
    * [`Message`](appbuilder.core.md#appbuilder.core.message.Message)
      * [`Message.content`](appbuilder.core.md#appbuilder.core.message.Message.content)
      * [`Message.id`](appbuilder.core.md#appbuilder.core.message.Message.id)
      * [`Message.model_computed_fields`](appbuilder.core.md#appbuilder.core.message.Message.model_computed_fields)
      * [`Message.model_config`](appbuilder.core.md#appbuilder.core.message.Message.model_config)
      * [`Message.model_fields`](appbuilder.core.md#appbuilder.core.message.Message.model_fields)
      * [`Message.mtype`](appbuilder.core.md#appbuilder.core.message.Message.mtype)
      * [`Message.name`](appbuilder.core.md#appbuilder.core.message.Message.name)
  * [appbuilder.core.session_message module](appbuilder.core.md#appbuilder-core-session-message-module)
  * [appbuilder.core.user_session module](appbuilder.core.md#module-appbuilder.core.user_session)
    * [`UserSession`](appbuilder.core.md#appbuilder.core.user_session.UserSession)
      * [`UserSession.append()`](appbuilder.core.md#appbuilder.core.user_session.UserSession.append)
      * [`UserSession.get_history()`](appbuilder.core.md#appbuilder.core.user_session.UserSession.get_history)
    * [`lazy_import_sqlalchemy()`](appbuilder.core.md#appbuilder.core.user_session.lazy_import_sqlalchemy)
  * [Module contents](appbuilder.core.md#module-appbuilder.core)

## Module contents

### *class* appbuilder.ASR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

ASR组件，即对于输入的语音文件，输出语音识别结果

Examples:

```python
import appbuilder
asr = appbuilder.ASR()
os.environ["APPBUILDER_TOKEN"] = '...'

with open("xxxx.pcm", "rb") as f:
    audio_data = f.read()
content_data = {"audio_format": "pcm", "raw_audio": audio_data, "rate": 16000}
msg = appbuilder.Message(content_data)
out = asr.run(msg)
print(out.content) # eg: {"result": ["北京科技馆。"]}
```

#### manifests *= [{'description': '对于输入的语音文件进行识别，输出语音识别结果。', 'name': 'asr', 'parameters': {'anyOf': [{'required': ['file_url']}, {'required': ['file_name']}], 'properties': {'file_name': {'description': '待识别语音文件名,用于生成获取语音的url', 'type': 'string'}, 'file_type': {'description': '语音文件类型,支持pcm/wav/amr/m4a', 'enum': ['pcm', 'wav', 'amr', 'm4a'], 'type': 'string'}, 'file_url': {'description': '输入语音文件的url,根据url获取到语音文件', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'asr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), audio_format: str = 'pcm', rate: int = 16000, timeout: float = None, retry: int = 0, \*\*kwargs) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行语音识别操作，并返回识别结果。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息对象，包含待识别的音频数据。该参数为必需项，格式如：Message(content={“raw_audio”: b”…”})。
  * **audio_format** (*str* *,* *optional*) – 音频文件格式，支持pcm/wav/amr/m4a，不区分大小写，推荐使用pcm格式。默认为”pcm”。
  * **rate** (*int* *,* *optional*) – 音频采样率，固定为16000。默认为16000。
  * **timeout** (*float* *,* *optional*) – HTTP请求超时时间。默认为None。
  * **retry** (*int* *,* *optional*) – HTTP请求重试次数。默认为0。
* **返回:**
  语音识别结果，格式如：Message(content={“result”: [“识别结果”]})。
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

评估给定文件名或文件URL的语音识别结果。

* **参数:**
  * **name** (*str*) – 函数调用名称。
  * **streaming** (*bool*) – 是否以流的方式返回结果。
  * **\*\*kwargs** – 关键字参数，用于指定文件名、文件URL等参数。
* **返回:**
  如果streaming为True，则通过生成器逐个返回包含识别结果的消息对象；
  如果streaming为False，则返回包含识别结果的JSON字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 如果未设置文件名或文件URL不存在，则抛出此异常。

#### version *= 'v1'*

### *class* appbuilder.AgentBuilder(app_id: str)

基类：[`AppBuilderClient`](appbuilder.core.console.appbuilder_client.md#appbuilder.core.console.appbuilder_client.appbuilder_client.AppBuilderClient)

### *class* appbuilder.AnimalRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出动物识别结果。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

animal_recognition = appbuilder.AnimalRecognition()
with open("./animal_recognition_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### manifests *= [{'description': '用于识别图片中动物类别，可识别近八千种动物', 'name': 'animal_rec', 'parameters': {'anyOf': [{'required': ['img_name']}, {'required': ['img_url']}], 'properties': {'img_name': {'description': '待识别图片的文件名', 'type': 'string'}, 'img_url': {'description': '待识别图片的url', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'animal_rec'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行动物识别

* **参数:**
  * **(****obj** (*message*) – Message): 用于执行识别操作的输入图片或图片url下载地址。
    例如：Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间
  * **retry** (*int* *,*  *可选*) – HTTP重试次数
* **返回:**
  Message): 识别结果。
  : 例如：Message(name=msg, content={‘result’: [{‘name’: ‘国宝大熊猫’, ‘score’: ‘0.945917’}, {‘name’: ‘秦岭四宝’, ‘score’: ‘0.0417291’},
    {‘name’: ‘团团圆圆’, ‘score’: ‘0.00584368’}, {‘name’: ‘圆仔’, ‘score’: ‘0.000846628’}, {‘name’: ‘棕色大熊猫’, ‘score’: ‘0.000538988’},
    {‘name’: ‘金丝猴’, ‘score’: ‘0.000279618’}]}, mtype=dict)
* **返回类型:**
  message (obj

#### tool_eval(name: str, streaming: bool, origin_query: str, \*\*kwargs) → Generator[str, None, None] | str

用于工具的执行，通过调用底层接口进行动物识别。

* **参数:**
  * **name** (*str*) – 工具名。
  * **streaming** (*bool*) – 是否流式返回。
  * **origin_query** (*str*) – 用户原始query。
  * **\*\*kwargs** – 工具调用的额外关键字参数。
* **返回:**
  动物识别结果，包括识别出的动物类别和相应的置信度信息。
* **返回类型:**
  Union[Generator[str, None, None], str]

#### version *= 'v1'*

### *class* appbuilder.AppBuilderClient(app_id: str, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

AppBuilderClient 组件支持调用在[百度智能云千帆AppBuilder]([https://cloud.baidu.com/product/AppBuilder](https://cloud.baidu.com/product/AppBuilder))平台上
构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。

### 示例

#### create_conversation() → str

创建会话并返回会话ID，会话ID在服务端用于上下文管理、绑定会话文档等，
如需开始新的会话，请创建并使用新的会话ID

* **参数:**
  **无**
* **返回:**
  唯一会话ID
* **返回类型:**
  response (str)

#### run(conversation_id: str, query: str = '', file_ids: list = [], stream: bool = False, tools: list[Tool] = None, tool_outputs: list[ToolOutput] = None, tool_choice: ToolChoice = None, end_user_id: str = None, \*\*kwargs) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

运行一次对话，返回对话结果

* **参数:**
  * **query** (*str*) – query内容
  * **conversation_id** (*str*) – 唯一会话ID，如需开始新的会话，请使用self.create_conversation创建新的会话
  * **file_ids** (*list* *[**str* *]* *,* *optional*) – 上传文件ID列表
  * **stream** (*bool* *,* *optional*) – 为True时，流式返回，需要将message.content.answer拼接起来才是完整的回答；为False时，对应非流式返回
  * **tools** (*list* *[**data_class.Tool* *]* *,* *optional*) – 一个Tool组成的列表，其中每个Tool对应一个工具的配置, 默认为None
  * **tool_outputs** (*list* *[**data_class.ToolOutput* *]* *,* *optional*) – 工具输出列表，格式为list[ToolOutput], ToolOutput内容为本地的工具执行结果，以自然语言/json dump str描述，默认为None
  * **tool_choice** (*data_class.ToolChoice* *,* *optional*) – 控制大模型使用组件的方式，默认为None
  * **end_user_id** (*str* *,* *optional*) – 用户ID，用于区分不同用户
* **返回:**
  Message): 对话结果
* **返回类型:**
  message (obj

#### run_with_handler(conversation_id: str, query: str = '', file_ids: list = [], tools: list[Tool] = None, stream: bool = False, event_handler=None, \*\*kwargs)

#### upload_local_file(conversation_id, local_file_path: str) → str

上传文件并将文件与会话ID进行绑定，后续可使用该文件ID进行对话，目前仅支持上传xlsx、jsonl、pdf、png等文件格式

* **参数:**
  * **conversation_id** (*str*) – 会话ID
  * **local_file_path** (*str*) – 本地文件路径
* **返回:**
  唯一文件ID
* **返回类型:**
  str
* **抛出:**
  * **ValueError** – 如果conversation_id为空，将抛出ValueError异常
  * **FileNotFoundError** – 如果本地文件路径不存在，将抛出FileNotFoundError异常

该接口用于在对话中上传文件供大模型处理，文件的有效期为7天并且不超过对话的有效期。一次只能上传一个文件。

### *exception* appbuilder.AppBuilderServerException(request_id='', code='', message='', service_err_code='', service_err_message='')

基类：`BaseRPCException`

AppBuilderServerException represent backend server failed response.

#### code *: int* *= 500*

#### description *: str* *= 'Interal Server Error'*

### *class* appbuilder.AppBuilderTracer(\*args, \*\*kwargs)

基类：`object`

#### add_custom_processor(processor)

#### end_trace()

#### *property* instrumentor

#### start_trace()

#### *property* tracer_provider

### *class* appbuilder.AppbuilderInstrumentor(\*args, \*\*kwargs)

基类：`BaseInstrumentor`

Instrumentor for appbuilder and appbuilder-sdk-ext.

#### instrumentation_dependencies()

Return a list of python packages with versions that the will be instrumented.

The format should be the same as used in requirements.txt or pyproject.toml.

For example, if an instrumentation instruments requests 1.x, this method should look
like:

> def instrumentation_dependencies(self) -> Collection[str]:
> : return [‘requests ~= 1.0’]

This will ensure that the instrumentation will only be used when the specified library
is present in the environment.

### *class* appbuilder.AppbuilderTestToolEval(appbuilder_components: <module 'appbuilder.core.components' from '/Users/yinjiaqi/miniconda3/envs/docs-test-for-sdk/lib/python3.12/site-packages/appbuilder/core/components/_\_init_\_.py'>, tool_eval_input: dict, response: ~requests.models.Response)

基类：`object`

功能:Components组件模拟post本地运行。

使用方法：

```
``
```

```
`
```

python
# 实例化一个
image_understand = appbuilder.ImageUnderstand()

# 设计一个符合规范的tool_eval input(dict数据类型)
tool_eval_input = {

> > ‘streaming’: True,
> > ‘traceid’: ‘traceid’,
> > ‘name’:”image_understand”,
> > ‘img_url’:’img_url_str’,
> > ‘origin_query’:””

> }

# 设计一个组件API接口预期的response
mock_response_data = {

> > ‘result’: {‘task_id’: ‘1821485837570181996’},
> > ‘log_id’: 1821485837570181996,

> }

mock_response = Mock()
mock_response.status_code = 200
mock_response.headers = {‘Content-Type’: ‘application/json’}
def mock_json():

> return mock_response_data

mock_response.json = mock_json

# 实例化一个AppbuilderTestToolEval对象,实现组件本地的自动化测试
appbuilder.AppbuilderTestToolEval(appbuilder_components=image_understand,

> tool_eval_input=tool_eval_input,
> response=mock_response)

```
``
```

```
`
```

#### test_manifests()

校验组件成员变量manifests是否符合规范。

* **参数:**
  **无参数。**
* **返回:**
  无返回值。
* **抛出:**
  **AppbuilderBuildexException** – 校验不通过时抛出异常。

#### test_tool_eval_generator()

测试组件tool_eval方法返回是否为生成器

* **参数:**
  **无**
* **返回:**
  无
* **抛出:**
  **AppbuilderBuildexException** – 如果组件tool_eval的返回值不为生成器时抛出异常

#### test_tool_eval_input()

校验tool_eval的传入参数是否合法。

* **参数:**
  **无参数。**
* **返回:**
  无返回值。
* **抛出:**
  **AppbuilderBuildexException** – 校验不通过时抛出异常。

#### test_tool_eval_reponse_raise()

* **参数:**
  **无参数**
* **返回:**
  无返回值
* **抛出:**
  **AppbuilderBuildexException** – 如果响应头状态码对应的异常类型与捕获到的异常类型不一致，则抛出此异常。

功能：测试tool_eval方法在不同响应头状态码下的异常抛出情况。

首先，设置响应头状态码为bad_request，并模拟InnerSession.post方法的返回值。
然后，定义一个状态码与异常类型的映射字典test_status_code_dict，用于测试不同状态码下抛出的异常类型是否正确。
接着，遍历test_status_code_dict字典，将状态码和异常类型分别赋值给self.response.status_code和error变量，并重新模拟InnerSession.post方法的返回值。
在每次循环中，调用self.component.tool_eval方法，并捕获可能抛出的异常。
如果捕获到的异常类型与test_status_code_dict字典中对应状态码的异常类型一致，则继续下一次循环；
否则，抛出AppbuilderBuildexException异常，提示用户检查self.component组件tool_eval方法的response返回值是否添加了check_response_header检测。

#### test_tool_eval_text_str()

测试tool_eval方法返回值的文本是否为字符串类型

* **参数:**
  **无**
* **返回:**
  无返回值，该函数主要进行断言测试
* **抛出:**
  **AppbuilderBuildexException** – 当tool_eval方法返回的文本不是字符串类型时抛出异常

### *class* appbuilder.AssistantEventHandler

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

### *class* appbuilder.AssistantStreamManager(response, event_handler: [AssistantEventHandler](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler))

基类：[`AssistantEventHandler`](appbuilder.core.assistant.threads.runs.md#appbuilder.core.assistant.threads.runs.stream_helper.AssistantEventHandler)

### *class* appbuilder.AutomaticTestToolEval(appbuilder_components: <module 'appbuilder.core.components' from '/Users/yinjiaqi/miniconda3/envs/docs-test-for-sdk/lib/python3.12/site-packages/appbuilder/core/components/_\_init_\_.py'>)

基类：`object`

#### test_input()

### *class* appbuilder.BESRetriever(embedding, index_name, bes_client, index_type='hnsw')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

向量检索组件，用于检索和query相匹配的内容

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
vector_index = appbuilder.BESVectorStoreIndex.from_segments(segments, self.cluster_id, self.username,
                                                            self.password)
query = appbuilder.Message("文心一言")
time.sleep(5)
retriever = vector_index.as_retriever()
res = retriever(query)
```

#### base_es_url *: str* *= '/v1/bce/bes/cluster/'*

#### name *: str* *= 'BaiduElasticSearchRetriever'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message), top_k: int = 1)

根据query进行查询

* **参数:**
  * **query** ([*Message*](#appbuilder.Message) *[**str* *]*) – 需要查询的内容，以Message对象的形式传递。
  * **top_k** (*int* *,* *optional*) – 查询结果中匹配度最高的top_k个结果。默认为1。
* **返回:**
  查询到的结果，包含文本、元数据以及匹配得分，以Message对象的形式返回。
* **返回类型:**
  obj ([Message](#appbuilder.Message)[Dict])

#### tool_desc *: Dict[str, Any]* *= {'description': 'a retriever based on Baidu ElasticSearch'}*

### *class* appbuilder.BESVectorStoreIndex(cluster_id, user_name, password, embedding=None, index_name=None, index_type='hnsw', prefix='/rpc/2.0/cloud_hub')

基类：`object`

BES向量存储检索工具

#### add_segments(segments: [Message](appbuilder.core.md#appbuilder.core.message.Message), metadata='')

向BES中插入数据

* **参数:**
  * **segments** ([*Message*](#appbuilder.Message) *[**str* *]*) – 需要插入的内容，包含多个文本段
  * **metadata** (*str* *,* *optional*) – 元数据，默认为空字符串。
* **返回:**
  无返回值

#### as_retriever()

将当前对象转化为retriever。

* **参数:**
  **无**
* **返回:**
  转化后的retriever对象
* **返回类型:**
  [BESRetriever](#appbuilder.BESRetriever)

#### base_es_url *: str* *= '/v1/bce/bes/cluster/'*

#### *static* create_index_mappings(index_type, vector_dims)

创建索引的mapping

* **参数:**
  * **index_type** (*str*) – 索引类型，如”hnsw”
  * **vector_dims** (*int*) – 向量的维度
* **返回:**
  索引的mapping配置
* **返回类型:**
  dict

#### delete_all_segments()

删除索引中的全部内容。

* **参数:**
  **无**
* **返回:**
  无

#### *property* es

#### *classmethod* from_segments(segments, cluster_id, user_name, password, embedding=None, \*\*kwargs)

根据段落创建一个bes向量索引。

* **参数:**
  * **segments** (*list*) – 切分的文本段落列表。
  * **cluster_id** (*str*) – bes集群ID。
  * **user_name** (*str*) – bes用户名。
  * **password** (*str*) – bes用户密码。
  * **embedding** ([*Embedding*](#appbuilder.Embedding) *,* *optional*) – 文本段落embedding工具，默认为None，使用默认的Embedding类。
  * **\*\*kwargs** – 其他初始化参数。
* **返回:**
  bes索引实例。
* **返回类型:**
  BesVectorIndex

#### *static* generate_id(length=16)

生成随机的ID。

* **参数:**
  **length** (*int* *,* *optional*) – 生成ID的长度，默认为16。
* **返回:**
  生成的随机ID。
* **返回类型:**
  str

#### get_all_segments()

获取索引中的全部内容

#### *property* helpers

### *exception* appbuilder.BadRequestException

基类：`BaseRPCException`

BadRequestException represent HTTP Code 400.

### *class* appbuilder.BaiduVDBRetriever(embedding, table)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

向量检索组件，用于检索和query相匹配的内容

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
vector_index = appbuilder.BaiduVDBVectorStoreIndex.from_params(
        self.instance_id,
        self.api_key,
)
vector_index.add_segments(segments)

query = appbuilder.Message("文心一言")
time.sleep(5)
retriever = vector_index.as_retriever()
res = retriever(query)
```

#### name *: str* *= 'BaiduVectorDBRetriever'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message), top_k: int = 1)

根据query进行查询

* **参数:**
  * **query** ([*Message*](#appbuilder.Message) *[**str* *]*) – 需要查询的内容，类型为Message，包含要查询的文本。
  * **top_k** (*int* *,* *optional*) – 查询结果中匹配度最高的top_k个结果，默认为1。
* **返回:**
  查询到的结果，包含文本和匹配得分。
* **返回类型:**
  [Message](#appbuilder.Message)[Dict]
* **抛出:**
  * **TypeError** – 如果query不是Message类型，或者top_k不是整数类型。
  * **ValueError** – 如果top_k不是正整数，或者query的内容为空字符串，或者长度超过512个字符。

#### tool_desc *: Dict[str, Any]* *= {'description': 'a retriever based on Baidu VectorDB'}*

### *class* appbuilder.BaiduVDBVectorStoreIndex(instance_id: str, api_key: str, account: str = 'root', database_name: str = 'AppBuilderDatabase', table_params: ~appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.TableParams = <appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever.TableParams object>, embedding=None)

基类：`object`

Baidu VDB向量存储检索工具

#### add_segments(segments: [Message](appbuilder.core.md#appbuilder.core.message.Message), metadata='')

向bes中插入数据段

* **参数:**
  * **segments** ([*Message*](#appbuilder.Message)) – 需要插入的数据段
  * **metadata** (*str* *,* *optional*) – 元数据，默认为空字符串。
* **返回:**
  无返回值
* **抛出:**
  **ValueError** – 如果segments为空，则抛出此异常。

#### as_retriever()

转化为retriever

#### *property* client *: Any*

Get client.

#### *classmethod* from_params(instance_id: str, api_key: str, account: str = 'root', database_name: str = 'AppBuilderDatabase', table_name: str = 'AppBuilderTable', drop_exists: bool = False, \*\*kwargs)

从参数中实例化类。

* **参数:**
  * **cls** – 类对象，即当前函数所属的类。
  * **instance_id** – str，实例ID。
  * **api_key** – str，API密钥。
  * **account** – str，账户名，默认为root。
  * **database_name** – str，数据库名，默认为AppBuilderDatabase。
  * **table_name** – str，表名，默认为AppBuilderTable。
  * **drop_exists** – bool，是否删除已存在的表，默认为False。
  * **\*\*kwargs** – 其他参数，可选的维度参数dimension默认为384。
* **返回:**
  类实例，包含实例ID、账户名、API密钥、数据库名、表参数等属性。

#### vdb_uri_prefix *= b'/api/v1/bce/vdb/instance/'*

### *class* appbuilder.CustomProcessRule(\*, separators: list[str], target_length: Annotated[int, Ge(ge=300), Le(le=1200)], overlap_rate: Annotated[float, Ge(ge=0), Le(le=0.3)])

基类：`BaseModel`

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'overlap_rate': FieldInfo(annotation=float, required=True, description='分段重叠最大字数占比，推荐值0.25', json_schema_extra={'example': 0.2}, metadata=[Ge(ge=0), Le(le=0.3)]), 'separators': FieldInfo(annotation=list[str], required=True, description='分段符号列表', json_schema_extra={'example': [',', '?']}), 'target_length': FieldInfo(annotation=int, required=True, description='分段最大长度', metadata=[Ge(ge=300), Le(le=1200)])}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### overlap_rate *: float*

#### separators *: list[str]*

#### target_length *: int*

### *class* appbuilder.DialogSummary(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

会话小结大模型组件， 基于生成式大模型对一段用户与坐席的对话生成总结，结果按{“诉求”: “”, “回应”: “”, “解决情况”: “”}格式输出。

Examples:

```python
import app
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

dialog_summary = appbuilder.DialogSummary("ERNIE Speed-AppBuilder")
text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
answer = dialog_summary(appbuilder.Message(text))
print(answer)
```

#### meta

[`DialogSummaryArgs`](appbuilder.core.components.llms.dialog_summary.md#appbuilder.core.components.llms.dialog_summary.component.DialogSummaryArgs) 的别名

#### name *: str* *= 'dialog_summary'*

#### run(message, stream=False, temperature=1e-10, top_p=0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.DishRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

菜品识别组件，适用于识别只含有单个菜品的图片，返回识别的菜品名称和卡路里信息

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

dish_recognition = appbuilder.DishRecognition()

with open("xxxx.jpg", "rb") as f:
    resp = dish_recognition(appbuilder.Message({"raw_image": f.read()}))
    # 输出示例 {'result': [{'name': '剁椒鱼头', 'calorie': '127'}]}
    print(resp.content)
```

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

根据输入图片进行菜品识别。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入待识别图片，支持传图片二进制流和图片URL。
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为 None。
  * **retry** (*int* *,* *optional*) – 重试次数，默认为 0。
* **返回:**
  包含菜品识别结果的输出消息。例如，Message(content={‘result’: [{‘name’: ‘剁椒鱼头’, ‘calorie’: ‘127’}]})
* **返回类型:**
  [Message](#appbuilder.Message)

### *class* appbuilder.DocCropEnhance(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

对图片中的文件、卡证、票据等内容进行四角点检测定位，提取主体内容并对其进行矫正，同时可选图片增强效果进一步提升图片清晰度，
达到主体检测矫正并增强的目的，提升图片整体质量

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

doc_crop_enhance = appbuilder.DocCropEnhance()
with open("./doc_enhance_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), enhance_type: int = 0, timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

文档矫正增强

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入图片或图片url下载地址用于执行操作。举例: Message(content={“raw_image”: b”…”,
  * **"enhance_type"** – 3})或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **enhance_type** (*int* *,*  *可选*) – 选择是否开启图像增强功能，如开启可选择增强效果，可选值如下：
    - 0：默认值，不开启增强功能
    - 1：去阴影
    - 2：增强并锐化
    - 3：黑白滤镜。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间
  * **retry** (*int* *,*  *可选*) – HTTP重试次数
* **返回:**
  识别结果。举例: Message(name=msg, content={‘image_processed’: ‘…’,
  ‘points’: [{‘x’: 220, ‘y’: 705}, {‘x’: 240, ‘y’: 0}, {‘x’: 885, ‘y’: 2}, {‘x’: 980, ‘y’: 759}]},
  mtype=dict)
* **返回类型:**
  [Message](#appbuilder.Message)

### *class* appbuilder.DocParser(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文档解析组件，用于对文档的内容进行解析。

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

file_path = "./test.pdf" # 待解析的文件路径
msg = Message(file_path)
parser = appbuilder.DocParser()
parse_result = parser(msg)
```

#### base_url *: str* *= '/v1/bce/xmind/parser'*

#### config *: [ParserConfig](#appbuilder.ParserConfig)* *= ParserConfig(convert_file_to_pdf=False, page_filter=None, return_para_node_tree=True, erase_watermark=False)*

#### make_parse_result(response: Dict)

将解析结果的内容转化成ParseResult的结构

#### name *: str* *= 'doc_parser'*

#### run(input_message: [Message](appbuilder.core.md#appbuilder.core.message.Message), return_raw=False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

对传入的文件进行解析

* **参数:**
  * **input_message** ([*Message*](#appbuilder.Message) *[**str* *]*) – 输入为文件的路径
  * **return_raw** (*bool* *,* *optional*) – 是否返回云端服务的原始结果。默认为False。
* **返回:**
  文件的解析结果。
* **返回类型:**
  [Message](#appbuilder.Message)[ParseResult]
* **抛出:**
  * **ValueError** – 如果传入的文件路径不是字符串类型。
  * [**AppBuilderServerException**](#appbuilder.AppBuilderServerException) – 如果文件解析过程中出现异常，将抛出该异常。

#### set_config(config: [ParserConfig](#appbuilder.ParserConfig))

设置解析配置

#### tool_desc *: Dict[str, Any]* *= {'description': 'parse document content'}*

### *class* appbuilder.DocSplitter(splitter_type, max_segment_length=800, overlap=200, separators=['。', '！', '？', '.', '!', '?', '……', '|\\n'], join_symbol='', \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

#### meta *: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments)* *= ComponentArguments(name='', tool_desc={'description': 'split data to segments in doc'})*

#### name *: str* *= 'doc_to_parapraphs'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

将输入的解析文档结果处理为多个段落结果。

* **参数:**
  **(****obj** (*message*) – Message): 上游docparser的文档解析结果。
* **返回:**
  Message: 文档分隔后的段落结果。
* **返回类型:**
  obj
* **抛出:**
  * **ValueError** – 如果 message.content 不是 ParseResult 类型。
  * **ValueError** – 如果 splitter_type 未设置值。
  * **ValueError** – 如果 ParseResult 对象不包含原始值（raw）。
  * **ValueError** – 如果 splitter_type 不是 ‘split_by_chunk’ 或 ‘split_by_title’。

### *class* appbuilder.DocumentChoices(\*, choices: list[str])

基类：`BaseModel`

#### choices *: list[str]*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'choices': FieldInfo(annotation=list[str], required=True, description='选择项')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

### *class* appbuilder.DocumentChunker(\*, choices: list[str], prependInfo: list[str], separator: [DocumentSeparator](#appbuilder.DocumentSeparator) | None, pattern: [DocumentPattern](#appbuilder.DocumentPattern) | None = None)

基类：`BaseModel`

#### choices *: list[str]*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'choices': FieldInfo(annotation=list[str], required=True, description='使用哪些chunker方法 (separator | pattern | onePage)，separator：自定义切片—标识符，pattern：自定义切片—标识符中选择正则表达式，onePage：整文件切片'), 'pattern': FieldInfo(annotation=Union[DocumentPattern, NoneType], required=False, description='正则表达式'), 'prependInfo': FieldInfo(annotation=list[str], required=True, description='chunker关联元数据，可选值为title (增加标题), filename(增加文件名)'), 'separator': FieldInfo(annotation=Union[DocumentSeparator, NoneType], required=True, description='分段符号')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### pattern *: [DocumentPattern](#appbuilder.DocumentPattern) | None*

#### prependInfo *: list[str]*

#### separator *: [DocumentSeparator](#appbuilder.DocumentSeparator) | None*

### *class* appbuilder.DocumentPattern(\*, markPosition: str, regex: str, targetLength: int, overlapRate: float)

基类：`BaseModel`

#### markPosition *: str*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'markPosition': FieldInfo(annotation=str, required=True, description='命中内容放置策略, head：前序切片, tail：后序切片, drop：匹配后丢弃', json_schema_extra={'enum': ['head', 'tail', 'drop']}), 'overlapRate': FieldInfo(annotation=float, required=True, description='分段重叠最大字数占比，推荐值0.25'), 'regex': FieldInfo(annotation=str, required=True, description='正则表达式'), 'targetLength': FieldInfo(annotation=int, required=True, description='分段最大长度')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### overlapRate *: float*

#### regex *: str*

#### targetLength *: int*

### *class* appbuilder.DocumentProcessOption(\*, template: str, parser: [DocumentChoices](#appbuilder.DocumentChoices) | None = None, knowledgeAugmentation: [DocumentChoices](#appbuilder.DocumentChoices) | None = None, chunker: [DocumentChunker](#appbuilder.DocumentChunker) | None = None)

基类：`BaseModel`

#### chunker *: [DocumentChunker](#appbuilder.DocumentChunker) | None*

#### knowledgeAugmentation *: [DocumentChoices](#appbuilder.DocumentChoices) | None*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'chunker': FieldInfo(annotation=Union[DocumentChunker, NoneType], required=False, description='分段器类型'), 'knowledgeAugmentation': FieldInfo(annotation=Union[DocumentChoices, NoneType], required=False, description='知识增强，faq、spokenQuery、spo、shortSummary按需增加。问题生成:faq、spokenQuery，段落摘要:shortSummary，三元组知识抽取:spo'), 'parser': FieldInfo(annotation=Union[DocumentChoices, NoneType], required=False, description='解析方法(文字提取默认启动，参数不体现，layoutAnalysis版面分析，ocr按需增加)'), 'template': FieldInfo(annotation=str, required=True, description='模板类型，ppt: 模版配置—ppt幻灯片, resume：模版配置—简历文档, paper：模版配置—论文文档, custom：自定义配置—自定义切片, default：自定义配置—默认切分', json_schema_extra={'enum': ['ppt', 'paper', 'qaPair', 'resume', ' custom', 'default']})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### parser *: [DocumentChoices](#appbuilder.DocumentChoices) | None*

#### template *: str*

### *class* appbuilder.DocumentSeparator(\*, separators: list[str], targetLength: int, overlapRate: float)

基类：`BaseModel`

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'overlapRate': FieldInfo(annotation=float, required=True, description='分段重叠最大字数占比，推荐值0.25'), 'separators': FieldInfo(annotation=list[str], required=True, description='分段符号'), 'targetLength': FieldInfo(annotation=int, required=True, description='分段最大长度')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### overlapRate *: float*

#### separators *: list[str]*

#### targetLength *: int*

### *class* appbuilder.DocumentSource(\*, type: str, urls: list[str] = None, urlDepth: int = None)

基类：`BaseModel`

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'type': FieldInfo(annotation=str, required=True, description='数据来源类型', json_schema_extra={'enum': ['bos', 'web']}), 'urlDepth': FieldInfo(annotation=int, required=False, description='url下钻深度，1时不下钻'), 'urls': FieldInfo(annotation=list[str], required=False, description='文档URL')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### type *: str*

#### urlDepth *: int*

#### urls *: list[str]*

### *class* appbuilder.Embedding(model='Embedding-V1')

基类：`EmbeddingBaseComponent`

Embedding-V1是基于百度文心大模型技术的文本表示模型，将文本转化为用数值表示的向量形式，用于文本检索、信息推荐、知识挖掘等场景。

### 示例

```python
import appbuilder
from appbuilder import Message

os.environ["APPBUILDER_TOKEN"] = '...'

embedding = appbuilder.Embedding()

embedding_single = embedding(Message("hello world!"))

embedding_batch = embedding.batch(Message(["hello", "world"]))
```

#### accepted_models *= ['Embedding-V1']*

#### base_urls *= {'Embedding-V1': '/v1/bce/wenxinworkshop/ai_custom/v1/embeddings/embedding-v1'}*

#### batch(texts: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]] | List[str]) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[List[float]]]

batch run

#### meta

[`EmbeddingArgs`](appbuilder.core.components.embeddings.md#appbuilder.core.components.embeddings.component.EmbeddingArgs) 的别名

#### name *: str* *= 'embedding'*

#### run(text: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]]

处理给定的文本或消息对象，并返回包含处理结果的消息对象。

* **参数:**
  **text** (*Union* *[*[*Message*](#appbuilder.Message) *[**str* *]* *,* *str* *]*) – 待处理的文本或消息对象。
* **返回:**
  处理后的结果，封装在消息对象中。结果是一个浮点数列表。
* **返回类型:**
  [Message](#appbuilder.Message)[List[float]]

#### version *: str* *= 'v1'*

### *class* appbuilder.ExtractTableFromDoc(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文档表格抽取

### 示例

```python
import os
import json

from appbuilder.utils.logger_util import logger
from appbuilder import Message, ExtractTableFromDoc, DocParser

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

# 测试文档解析器使用默认配置，xxx为待解析的文档路径。
msg = Message("xxx")
parser = DocParser()
# ExtractTableFromDoc输入为文档原始解析结果，此处需要带上原始结果，return_raw=True.
doc = parser(msg, return_raw=True).content.raw

# 抽取文档中的表格
parser = ExtractTableFromDoc()
result = parser.run(Message(doc))

logger.info("Tables: {}".format(
    json.dumps(result.content, ensure_ascii=False)))
```

#### base_url *= '/rpc/2.0/cloud_hub/v1/ai_engine/copilot_engine/v1/api/doc_search_tools/doc_table_to_markdown_parser'*

#### meta *: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments)* *= ComponentArguments(name='', tool_desc={'description': 'Extract table from doc, table format is markdown'})*

#### name *: str* *= 'extract_table_from_doc'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), table_max_size: int = 800, doc_node_num_before_table: int = 1)

将文档原始解析结果，请求云端进行表格抽取，返回表格列表。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 文档原始解析结果。
  * **table_max_size** (*int*) – 单个表格的长度的最大值(包含上文)，按字符数即len(table_str)统计，默认为800。如果表格超长，则会被拆            分成多个子表格，拆分的最小粒度为表格的行。若单行就超长，则会强制按table_max_size截断。截断时会优先截断上文，尽量保留表格内容。
  * **doc_node_num_before_table** (*int*) – 表格前附加的上文DocParser Node的数量，默认为1。范围：1~10。
* **返回:**
  返回解析后的消息实体对象
  : Message.content (list): 解析出来的文档表格，list(二维)。解析出来的文档表格，如果元素长度为1，则对应原文档中格式化后的                长度不超过\`table_max_size\`的表格；如果元素长度>1，则是对应原文档中一个大表格，该表格被拆分成的多个子表格，以满足设置                大小。输出结果数据结构样例：[[{table1}], [{table2-part1}, {table2-part2}]]
* **返回类型:**
  [Message](#appbuilder.Message)
* **抛出:**
  **ValueError** – 当输入参数不为文档原始解析结果时，或值不合法时，抛出异常。

### *exception* appbuilder.ForbiddenException

基类：`BaseRPCException`

BadRequestException represent HTTP Code 403.

### *class* appbuilder.GeneralOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

提供通用文字识别能力，在通用文字识别的基础上，提供更高精度的识别服务，支持更多语种识别（丹麦语、荷兰语、马来语、
瑞典语、印尼语、波兰语、罗马尼亚语、土耳其语、希腊语、匈牙利语、泰语、越语、阿拉伯语、印地语及部分中国少数民族语言），
并将字库从1w+扩展到2w+，能识别所有常用字和大部分生僻字。

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

general_ocr = appbuilder.GeneralOCR()
with open("./general_ocr_test.png", "rb") as f:
    out = general_ocr.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### manifests *= [{'description': '提供更高精度的通用文字识别能力，能够识别图片中的文字，不支持html后缀文件的输入', 'name': 'general_ocr', 'parameters': {'anyOf': [{'required': ['img_url']}, {'required': ['img_name']}], 'properties': {'img_name': {'description': '待识别图片的文件名,用于生成图片url', 'type': 'string'}, 'img_url': {'description': '待识别图片的url,根据该url能够获取图片', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'general_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行图片中的文字识别

* **参数:**
  * **(****obj** (*message*) – Message): 输入图片或图片url下载地址用于执行识别操作.x举例: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”}).
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间
  * **retry** (*int* *,*  *可选*) – HTTP重试次数
* **返回:**
  Message): 模型识别结果.
  : 举例: Message(content={“words_result”:[{“words”:”100”}, {“words”:”G8”}]})
* **返回类型:**
  message (obj

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

根据给定的参数执行OCR识别功能。

* **参数:**
  * **name** (*str*) – 函数名称，此处未使用，但为保持一致性保留。
  * **streaming** (*bool*) – 是否以流式方式返回结果。如果为True，则逐个返回结果，否则返回全部结果。
  * **kwargs** – 关键字参数，支持以下参数：
    traceid (str): 请求的唯一标识符，用于追踪请求和响应。
    img_url (str): 待识别图片的URL。
    file_urls (dict): 包含文件名和对应URL的字典。如果提供了img_url，则忽略此参数。
    img_name (str): 待识别图片的文件名，与file_urls配合使用。
* **返回:**
  如果streaming为False，则返回包含识别结果的JSON字符串。
  如果streaming为True，则逐个返回包含识别结果的字典。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误（例如未设置文件名或指定文件名对应的URL不存在），则抛出此异常。

#### version *= 'v1'*

### *exception* appbuilder.HTTPConnectionException

基类：`BaseRPCException`

HTTPConnectionException represent HTTP Connection error.

### *class* appbuilder.HallucinationDetection(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

幻觉检测。输入<query, context, answer>，判断answer中是否存在幻觉。
 *注：该组件推荐使用ERNIE Speed-AppBuilder模型。*

Examples:

```python
import os
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ['APPBUILDER_TOKEN'] = '...'

hallucination_detection = appbuilder.HallucinationDetection()

query = ''
context =         '''澳门美食： 澳门新麻蒲韩国烤肉店
在澳门一年四季之中除了火锅，烤肉也相当受欢迎。提到韩烧，有一间令我印象最深刻，就是号称韩国第一的烤肉店－新麻蒲韩国烤肉店，光是韩国的分店便多达四百多间，海外分店更是遍布世界各地，2016年便落户澳门筷子基区，在原本已经食肆林立的地方一起百花齐放！店内的装修跟韩国分店还完度几乎没差，让食客彷如置身于韩国的感觉，还要大赞其抽风系统不俗，离开时身上都不会沾上烤肉味耶！
时间：周一至周日 下午5:00 - 上午3:00
电话：＋853 2823 4012
地址：澳门筷子基船澳街海擎天第三座地下O号铺96号
必食推介:
护心肉二人套餐
来新麻蒲必试的有两样东西，现在差不多每间烤肉店都有炉边烤蛋，但大家知道吗？原来新麻蒲就是炉边烤蛋的开创者，既然是始祖，这已经是个非吃不可的理由！还有一款必试的就是护心肉，即是猪的横隔膜与肝中间的部分，每头猪也只有200克这种肉，非常珍贵，其味道吃起来有种独特的肉香味，跟牛护心肉一样精彩！
秘制猪皮
很多怕胖的女生看到猪皮就怕怕，但其实猪皮含有大量胶原蛋白，营养价值很高呢！这里红通通的猪皮还经过韩国秘制酱汁处理过，会有一点点辣味。烤猪皮的时候也需特别注意火侯，这样吃起来才会有外脆内Q的口感！'''
answer = '澳门新麻蒲烤肉店并不是每天开门。'

inputs = {'query': query, 'context': context, 'answer': answer}
msg = appbuilder.Message(inputs)
result = hallucination_detection.run(msg)

print(result)
```

#### completion(version, base_url, request, timeout: float = None, retry: int = 0)

Send a byte array of an audio file to obtain the result of speech recognition.

#### manifests *= [{'description': '输入用户查询query、检索结果context以及根据检索结果context生成的用户查询query的回答answer，判断answer中是否存在幻觉。', 'name': 'hallucination_detection', 'parameters': {'properties': {'answer': {'description': '根据检索结果context生成的用户查询query的回答answer。', 'text': 'string'}, 'context': {'description': '检索结果。', 'text': 'string'}, 'query': {'description': '用户查询。', 'text': 'string'}}, 'required': ['query', 'context', 'answer'], 'type': 'object'}}]*

#### meta

[`HallucinationDetectionArgs`](appbuilder.core.components.llms.hallucination_detection.md#appbuilder.core.components.llms.hallucination_detection.component.HallucinationDetectionArgs) 的别名

#### name *: str* *= 'hallucination_detection'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息，包含 query、context 和 answer。是必需的参数。
  * **stream** (*bool* *,*  *可选*) – 是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](#appbuilder.Message))
* **抛出:**
  * **AssertionError** – 如果输入的 message 中缺少 query、context 或 answer。
  * [**AppBuilderServerException**](#appbuilder.AppBuilderServerException) – 如果请求执行失败，将抛出异常，包含服务错误码和错误信息。

#### tool_eval(name: str, stream: bool = False, \*\*kwargs)

tool_eval for function call

#### version *: str* *= 'v1'*

### *class* appbuilder.HandwriteOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

手写文字识别组件

Examples:

```python
import os
import appbuilder
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
# 从BOS存储读取样例文件
image_url="https://bj.bcebos.com/v1/appbuilder/test_handwrite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b"
# 输入参数为一张图片
inp = appbuilder.Message(content={"url": image_url})
# 进行植物识别
handwrite_ocr = HandwriteOCR()
out = handwrite_ocr.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '需要对图片中手写体文字进行识别时，使用该工具，不支持PDF文件，如果用户没有提供图片文件，应引导用户提供图片，而不是尝试使用该工具', 'name': 'handwriting_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别文件的文件名', 'items': {'type': 'string'}, 'type': 'array'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'handwriting_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

输入图片并识别其中的文字

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入图片或图片url下载地址用于执行识别操作.例如: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”}).
  * **timeout** (*float* *,* *optional*) – HTTP超时时间. 默认为None.
  * **retry** (*int* *,* *optional*) – HTTP重试次数. 默认为0.
* **返回:**
  手写体模型识别结果.
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

对指定文件或URL进行手写识别。

* **参数:**
  * **name** (*str*) – 任务名称。
  * **streaming** (*bool*) – 是否以流式形式返回结果。
  * **kwargs** – 其他参数，包括：
    traceid (str, optional): 请求的traceid，用于标识请求的唯一性。默认为None。
    file_names (List[str], optional): 待识别的文件名列表。默认为None，此时会从kwargs中获取’files’参数。
    file_urls (Dict[str, str], optional): 文件名与URL的映射字典。默认为空字典。
* **返回:**
  如果streaming为True，则以生成器形式返回识别结果，否则直接返回结果字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误，例如指定的文件名对应的URL不存在。

#### version *= 'v1'*

### *class* appbuilder.ImageUnderstand(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

图像内容理解组件，即对于输入的一张图片（可正常解码，且长宽比适宜）与问题，输出对图片的描述

Examples:

```python
import os
import appbuilder
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
# 从BOS存储读取样例文件
image_url = "https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bfe25c372b7e56e6"
# 输入参数为一张图片
inp = Message(content={"url": image_url, "question": "图片里内容是什么?"})
# 进行图像内容理解
image_understand = ImageUnderstand()
out = image_understand.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '可对输入图片进行理解，可输出图片描述、OCR 及图像识别结果', 'name': 'image_understanding', 'parameters': {'anyOf': [{'required': ['img_name']}, {'required': ['img_url']}], 'properties': {'img_name': {'description': '待识别图片的文件名', 'type': 'string'}, 'img_url': {'description': '待识别图片的url', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'image_understanding'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行图像内容理解

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={“raw_image”: b”…”, “question”: “图片主要内容是什么？”})
    或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”, “question”: “图片主要内容是什么？”}).
  * **timeout** (*float* *,* *optional*) – HTTP超时时间. 默认为 None.
  * **retry** (*int* *,* *optional*) – HTTP重试次数. 默认为 0.
* **返回:**
  模型识别结果.
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(name: str, streaming: bool, origin_query: str, \*\*kwargs) → Generator[str, None, None] | str

用于工具的执行，调用底层接口进行图像内容理解

* **参数:**
  * **name** (*str*) – 工具名
  * **streaming** (*bool*) – 是否流式返回
  * **origin_query** (*str*) – 用户原始query
  * **\*\*kwargs** – 工具调用的额外关键字参数
* **返回:**
  图片内容理解结果
* **返回类型:**
  Union[Generator[str, None, None], str]

#### version *= 'v1'*

### *exception* appbuilder.InternalServerErrorException

基类：`BaseRPCException`

InternalServerErrorException represent HTTP Code 500.

### *class* appbuilder.IsComplexQuery(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

基于输入的问题, 对问题进行初步的分类，方便下游使用不同类型的流程来处理当前的简单问题/复杂问题。广泛用于知识问答场景。

> Examples:

{}”.format(answer.content))

#### meta

[`IsComplexQueryMeta`](appbuilder.core.components.llms.is_complex_query.md#appbuilder.core.components.llms.is_complex_query.component.IsComplexQueryMeta) 的别名

#### name *: str* *= 'is_complex_query'*

#### run(message, stream=False, temperature=1e-10, top_p=0)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.KnowledgeBase(knowledge_id: str | None = None, knowledge_name: str | None = None, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

#### add_document(content_type: str, file_ids: list[str] = [], is_enhanced: bool = False, custom_process_rule: [CustomProcessRule](#appbuilder.CustomProcessRule) | None = None, knowledge_base_id: str | None = None, client_token: str = None) → KnowledgeBaseAddDocumentResponse

向知识库中添加文档。

* **参数:**
  * **content_type** (*str*) – 文档的类型，例如 ‘TEXT’ 或 ‘PDF’。
  * **file_ids** (*list* *[**str* *]* *,* *optional*) – 文档ID列表，默认为空列表。文档ID通常由文件上传接口返回。
  * **is_enhanced** (*bool* *,* *optional*) – 是否启用增强模式，默认为False。启用后会对文档进行语义理解和结构化处理。
  * **custom_process_rule** (*Optional* *[*[*data_class.CustomProcessRule*](#appbuilder.CustomProcessRule) *]* *,* *optional*) – 自定义处理规则，默认为None。
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，默认为None。如果未指定，则使用当前实例的知识库ID。
  * **client_token** (*str* *,* *optional*) – 客户端请求的唯一标识，默认为None。如果不指定，则自动生成。
* **返回:**
  添加文档后的响应对象。
* **返回类型:**
  data_class.KnowledgeBaseAddDocumentResponse
* **抛出:**
  **ValueError** – 如果知识库ID为空且未先调用\`create\`方法或未指定现有知识库ID，则抛出ValueError异常。

#### create_chunk(documentId: str, content: str, client_token: str = None) → CreateChunkResponse

创建一个知识块。

* **参数:**
  * **documentId** (*str*) – 文档ID。
  * **content** (*str*) – 知识块内容。
  * **client_token** (*str* *,* *optional*) – 用于支持幂等性，默认为None。如果为None，则使用uuid4生成一个唯一的client_token。
* **返回:**
  创建知识块响应。
* **返回类型:**
  data_class.CreateChunkResponse
* **抛出:**
  **HTTPError** – 如果请求失败，将抛出HTTPError异常。

#### create_documents(id: str | None = None, contentFormat: str = '', source: [DocumentSource](#appbuilder.DocumentSource) = None, processOption: [DocumentProcessOption](#appbuilder.DocumentProcessOption) = None, client_token: str = None)

创建文档。

* **参数:**
  * **id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，默认为None。如果为None，则使用当前知识库ID。默认为None。
  * **contentFormat** (*str*) – 文档内容格式，默认为空字符串。
  * **source** ([*data_class.DocumentSource*](#appbuilder.DocumentSource) *,* *optional*) – 文档来源信息，默认为None。
  * **processOption** ([*data_class.DocumentProcessOption*](#appbuilder.DocumentProcessOption) *,* *optional*) – 文档处理选项，默认为None。
  * **client_token** (*str* *,* *optional*) – 用于标识请求的客户端令牌，默认为None。如果不提供，将自动生成一个UUID。
* **返回:**
  API响应结果。
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果当前知识库ID为空且未提供id参数，则抛出ValueError异常。

#### *classmethod* create_knowledge(knowledge_name: str) → [KnowledgeBase](appbuilder.core.console.knowledge_base.md#appbuilder.core.console.knowledge_base.knowledge_base.KnowledgeBase)

创建一个新的知识库。

* **参数:**
  * **cls** (*type*) – 类对象，用于调用此方法时不需要显式传递。
  * **knowledge_name** (*str*) – 要创建的知识库名称。
* **返回:**
  创建的知识库对象。
* **返回类型:**
  [KnowledgeBase](#appbuilder.KnowledgeBase)
* **抛出:**
  * **HTTPError** – 如果HTTP请求失败或响应状态码不为200。
  * **JSONDecodeError** – 如果响应数据不是有效的JSON格式。

#### NOTE
此方法已被弃用，请使用 create_knowledge_base 方法代替。

#### create_knowledge_base(name: str, description: str, type: str = 'public', esUrl: str = None, esUserName: str = None, esPassword: str = None, client_token: str = None) → KnowledgeBaseDetailResponse

创建一个知识库

* **参数:**
  * **name** (*str*) – 知识库名称
  * **description** (*str*) – 知识库描述
  * **type** (*str* *,* *optional*) – 知识库类型，默认为’public’。默认为 “public”。
  * **esUrl** (*str* *,* *optional*) – Elasticsearch 服务地址。默认为 None。
  * **esUserName** (*str* *,* *optional*) – Elasticsearch 用户名。默认为 None。
  * **esPassword** (*str* *,* *optional*) – Elasticsearch 密码。默认为 None。
  * **client_token** (*str* *,* *optional*) – 客户端token，用于区分请求来源。默认为 None。
* **返回:**
  创建知识库后的响应对象
* **返回类型:**
  data_class.KnowledgeBaseDetailResponse
* **抛出:**
  **requests.exceptions.HTTPError** – 请求失败时抛出

#### delete_chunk(chunkId: str, client_token: str = None)

删除知识库中的一个块

* **参数:**
  * **chunkId** (*str*) – 要删除的块的ID
  * **client_token** (*str* *,* *optional*) – 客户端令牌，用于请求的唯一标识，默认为None。
* **返回:**
  包含删除操作结果的字典。
* **返回类型:**
  dict

#### delete_document(document_id: str, knowledge_base_id: str | None = None, client_token: str = None) → KnowledgeBaseDeleteDocumentResponse

删除知识库中的文档

* **参数:**
  * **document_id** (*str*) – 要删除的文档ID
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果为None，则使用类的知识库ID。默认为None。
  * **client_token** (*str* *,* *optional*) – 请求的唯一标识，用于服务器追踪问题。默认为None，如果不传则自动生成。
* **返回:**
  删除文档响应对象
* **返回类型:**
  data_class.KnowledgeBaseDeleteDocumentResponse
* **抛出:**
  **ValueError** – 如果未设置类的知识库ID且未提供知识库ID，则抛出ValueError异常。

#### delete_knowledge_base(knowledge_base_id: str | None = None, client_token: str = None)

删除知识库

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID. 如果未提供，则使用当前实例的knowledge_id. Defaults to None.
  * **client_token** (*str* *,* *optional*) – 请求的唯一标识，用于服务端去重. 如果未提供，则自动生成一个UUID. Defaults to None.
* **返回:**
  API响应数据
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果既没有提供knowledge_base_id，且当前实例的knowledge_id也为None，则抛出异常

#### describe_chunk(chunkId: str) → DescribeChunkResponse

获取知识库片段信息

* **参数:**
  **chunkId** (*str*) – 知识库片段的ID
* **返回:**
  知识库片段信息响应对象
* **返回类型:**
  DescribeChunkResponse

#### describe_chunks(documentId: str, marker: str = None, maxKeys: int = None, type: str = None) → DescribeChunksResponse

查询文档分块信息

* **参数:**
  * **documentId** (*str*) – 文档ID
  * **marker** (*str* *,* *optional*) – 分页标记，默认为None。用于分页查询，如果第一页调用此API后，还有更多数据，API会返回一个Marker值，使用此Marker值调用API可以查询下一页数据，直到没有更多数据，API将不再返回Marker值。
  * **maxKeys** (*int* *,* *optional*) – 最大返回记录数，默认为None。指定本次调用最多可以返回的文档分块信息条数，最大值为100。
  * **type** (*str* *,* *optional*) – 文档分块类型，默认为None。指定要查询的文档分块类型。
* **返回:**
  包含文档分块信息的响应对象
* **返回类型:**
  DescribeChunksResponse

#### get_all_documents(knowledge_base_id: str | None = None) → dict

获取知识库中所有文档。

* **参数:**
  **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库的ID。如果为None，则使用当前实例的knowledge_id。默认为None。
* **返回:**
  包含所有文档的列表。
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果knowledge_base_id为空，且当前实例没有已创建的knowledge_id时抛出。

#### get_documents_list(limit: int = 10, after: str | None = '', before: str | None = '', knowledge_base_id: str | None = None) → KnowledgeBaseGetDocumentsListResponse

获取文档列表。

* **参数:**
  * **limit** (*int* *,* *optional*) – 返回的文档数量上限，默认为10。
  * **after** (*Optional* *[**str* *]* *,* *optional*) – 返回时间戳大于指定值的文档。默认为空字符串。
  * **before** (*Optional* *[**str* *]* *,* *optional*) – 返回时间戳小于指定值的文档。默认为空字符串。
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果未指定，则使用当前实例的知识库ID。默认为None。
* **返回:**
  包含文档列表的响应对象。
* **返回类型:**
  data_class.KnowledgeBaseGetDocumentsListResponse
* **抛出:**
  **ValueError** – 如果知识库ID为空，且未通过调用create方法创建知识库，则抛出此异常。

#### get_knowledge_base_detail(knowledge_base_id: str | None = None) → KnowledgeBaseDetailResponse

获取知识库详情。

* **参数:**
  **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID. 如果为None，则使用实例中的knowledge_id.
  默认为None.
* **返回:**
  知识库详情响应对象.
* **返回类型:**
  data_class.KnowledgeBaseDetailResponse
* **抛出:**
  **ValueError** – 如果knowledge_base_id为空且实例中的knowledge_id也为空，则抛出异常.

#### get_knowledge_base_list(knowledge_base_id: str | None = None, maxKeys: int = 10, keyword: str | None = None) → KnowledgeBaseGetListResponse

获取知识库列表

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID. 如果为None，则使用self.knowledge_id. 默认为None.
  * **maxKeys** (*int* *,* *optional*) – 最大返回数量. 默认为10.
  * **keyword** (*Optional* *[**str* *]* *,* *optional*) – 搜索关键字. 默认为None.
* **返回:**
  知识库列表响应对象.
* **返回类型:**
  data_class.KnowledgeBaseGetListResponse
* **抛出:**
  **ValueError** – 如果self.knowledge_id和knowledge_base_id都为None，则抛出异常，提示需要先调用create方法或使用已存在的知识库ID.

#### modify_chunk(chunkId: str, content: str, enable: bool, client_token: str = None)

修改知识库片段

* **参数:**
  * **chunkId** (*str*) – 知识库片段ID
  * **content** (*str*) – 修改后的内容
  * **enable** (*bool*) – 是否启用该知识库片段
  * **client_token** (*str* *,* *optional*) – 请求的唯一标识，默认为 None. 如果不指定，则自动生成.
* **返回:**
  修改后的知识库片段信息
* **返回类型:**
  dict
* **抛出:**
  * **HttpClientError** – 如果请求失败，则抛出 HttpClientError 异常
  * **ConsoleResponseError** – 如果控制台响应错误，则抛出 ConsoleResponseError 异常

#### modify_knowledge_base(knowledge_base_id: str | None = None, name: str | None = None, description: str | None = None, client_token: str = None)

修改知识库信息

* **参数:**
  * **knowledge_base_id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，如果为None，则使用当前实例的知识库ID. 默认为 None.
  * **name** (*Optional* *[**str* *]* *,* *optional*) – 知识库名称. 默认为 None.
  * **description** (*Optional* *[**str* *]* *,* *optional*) – 知识库描述. 默认为 None.
  * **client_token** (*str* *,* *optional*) – 客户端唯一标识符，用于保证幂等性. 默认为 None.
* **返回:**
  修改后的知识库信息
* **返回类型:**
  dict
* **抛出:**
  **ValueError** – 如果既没有提供knowledge_base_id，且当前实例没有设置knowledge_id，则抛出此异常.

#### upload_documents(file_path: str, content_format: str = 'rawText', id: str | None = None, processOption: [DocumentProcessOption](#appbuilder.DocumentProcessOption) = None, client_token: str = None)

上传文档到知识库

* **参数:**
  * **file_path** (*str*) – 文件路径
  * **content_format** (*str* *,* *optional*) – 内容格式，默认为 ‘rawText’。可选项包括 ‘rawText’, ‘markdown’, ‘html’ 等
  * **id** (*Optional* *[**str* *]* *,* *optional*) – 知识库ID，默认为None，此时将使用当前实例的知识库ID
  * **processOption** ([*data_class.DocumentProcessOption*](#appbuilder.DocumentProcessOption) *,* *optional*) – 文档处理选项，默认为None
  * **client_token** (*str* *,* *optional*) – 客户端token，默认为None，将自动生成一个UUID
* **返回:**
  上传文档后的响应数据
* **返回类型:**
  dict
* **抛出:**
  **FileNotFoundError** – 如果指定的文件路径不存在，将抛出 FileNotFoundError 异常

#### upload_file(file_path: str, client_token: str = None) → KnowledgeBaseUploadFileResponse

上传文件到知识库服务器。

* **参数:**
  * **file_path** (*str*) – 要上传的文件的路径。
  * **client_token** (*str* *,* *optional*) – 客户端令牌，用于标识请求的唯一性。如果未提供，则自动生成。
* **返回:**
  上传文件的响应。
* **返回类型:**
  data_class.KnowledgeBaseUploadFileResponse
* **抛出:**
  **FileNotFoundError** – 如果指定的文件路径不存在，则抛出 FileNotFoundError 异常。

### *class* appbuilder.LandmarkRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

识别地标组件，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的地标识别结果

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
landmark_recognize = appbuilder.LandmarkRecognition()
with open("xxxx.jpg", "rb") as f:
    inp = appbuilder.Message(content={"raw_image": f.read()})
    out = landmark_recognize.run(inp)
    # 打印识别结果
    print(out.content) # eg: {"landmark": "狮身人面相"}
```

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行地标识别任务

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息对象，包含待识别的图片或图片URL。
    例如：Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,* *optional*) – HTTP请求的超时时间。默认为None。
  * **retry** (*int* *,* *optional*) – HTTP请求的重试次数。默认为0。
* **返回:**
  地标识别结果的消息对象。
  : 例如：Message(content={“landmark”: b”狮身人面像”})
* **返回类型:**
  [Message](#appbuilder.Message)

### *class* appbuilder.MRC(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

阅读理解问答组件，基于大模型进行阅读理解问答，支持拒答、澄清、重点强调、友好性提升、溯源等多种功能，可用于回答用户提出的问题。

Examples:

```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建MRC对象
mrc_component = appbuilder.MRC()

#初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)
context_list = appbuilder.Message(["如何办理残疾人通行证一、残疾人通行证办理条件：
1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；2、持有准驾车型为C1（听力残疾）、
C2（左下肢残疾、听力残疾", "3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，
并有有效交强险凭证，C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
北京市无障碍环境建设促进中心"])

# 模拟运行MRC组件，开启拒答、澄清追问、重点强调、友好性提升和溯源能力五个功能
result = mrc_component.run(msg, context_list, reject=True,
                            clarify=True, highlight=True, friendly=True, cite=True)

# 输出运行结果
print(result)
```

#### meta *: [MrcArgs](appbuilder.core.components.llms.mrc.md#appbuilder.core.components.llms.mrc.component.MrcArgs)*

#### name *: str* *= 'mrc'*

#### run(message, context_list, reject=False, clarify=False, highlight=False, friendly=False, cite=False, stream=False, temperature=1e-10, top_p=0)

运行阅读理解问答模型并返回结果。

* **参数:**
  * **(****obj** (*context_list*) – Message): 输入消息，包含用户提出的问题。这是一个必需的参数。
  * **(****obj** – Message): 用户输入的问题对应的段落文本列表。这是一个必需的参数。
  * **reject** (*bool* *,*  *可选*) – 拒答开关，如果为 True，则启用拒答能力。默认为 False。
  * **clarify** (*bool* *,*  *可选*) – 澄清开关，如果为 True，则启用澄清能力。默认为 False。
  * **highlight** (*bool* *,*  *可选*) – 重点强调开关，如果为 True，则启用重点强调能力。默认为 False。
  * **friendly** (*bool* *,*  *可选*) – 友好性提升开关，如果为 True，则启用友好性提升能力。默认为 False。
  * **cite** (*bool* *,*  *可选*) – 溯源开关，如果为 True，则启用溯源能力。默认为 False。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.Matching(embedding_component: EmbeddingBaseComponent)

基类：`MatchingBaseComponent`

基于Embedding类型的文本表示模型，输入query和文本列表，对其进行排序或者相似度计算

### 示例

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

# 初始化所需要的组件
embedding = appbuilder.Embedding()
matching = appbuilder.Matching(embedding)

# 定义输入query和文本列表
query = appbuilder.Message("你好")
contexts = appbuilder.Message(["世界", "你好"])

# 根据query，对文本列表做相似度排序
contexts_matched = matching(query, contexts)
print(contexts_matched.content)
# ['你好', '世界']
```

#### meta

`MatchingArgs` 的别名

#### name *: str* *= 'Matching'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str, contexts: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]] | List[str], return_score: bool = False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]]

根据给定的查询和上下文，返回匹配的上下文列表。

* **参数:**
  * **query** (*Union* *[*[*Message*](#appbuilder.Message) *[**str* *]* *,* *str* *]*) – 查询字符串或Message对象，包含查询字符串。
  * **contexts** (*Union* *[*[*Message*](#appbuilder.Message) *[**List* *[**str* *]* *]* *,* *List* *[**str* *]* *]*) – 上下文字符串列表或Message对象，包含上下文字符串列表。
  * **return_score** (*bool* *,* *optional*) – 是否返回匹配得分。默认为False。
* **返回:**
  匹配的上下文列表。如果return_score为True，则返回包含得分和上下文的元组列表；否则仅返回上下文列表。
* **返回类型:**
  [Message](#appbuilder.Message)[List[str]]

#### semantics(query_embedding: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]] | List[float], context_embeddings: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[List[float]]] | List[List[float]]) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[float]]

计算query和context的相似度

* **参数:**
  * **query_embedding** (*Union* *[*[*Message*](#appbuilder.Message) *[**List* *[**float* *]* *]* *,* *List* *[**float* *]* *]*) – query的embedding，长度为n的数组
  * **context_embeddings** (*Union* *[*[*Message*](#appbuilder.Message) *[**List* *[**List* *[**float* *]* *]* *]* *,* *List* *[**List* *[**float* *]* *]* *]*) – context的embedding，长度为m x n的矩阵，其中m表示候选context的数量
* **返回:**
  query和所有候选context的相似度列表
* **返回类型:**
  [Message](#appbuilder.Message)[List[float]]

#### version *: str* *= 'v1'*

### *class* appbuilder.Message(content: \_T | None = None, \*, name: str | None = 'msg', mtype: str | None = 'dict', id: str | None = 'fb5d0e80-64cd-4a7e-a5a8-82b268cc0f68', \*\*data)

基类：`BaseModel`, `Generic`[`_T`]

#### content *: \_T | None*

#### id *: str | None*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'allow'}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'content': FieldInfo(annotation=Union[TypeVar, NoneType], required=False, default={}), 'id': FieldInfo(annotation=Union[str, NoneType], required=False, default='fb5d0e80-64cd-4a7e-a5a8-82b268cc0f68'), 'mtype': FieldInfo(annotation=Union[str, NoneType], required=False, default='dict'), 'name': FieldInfo(annotation=Union[str, NoneType], required=False, default='msg')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### mtype *: str | None*

#### name *: str | None*

### *class* appbuilder.MixCardOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

身份证混贴识别组件

Examples:

```python
import os
import requests
import appbuilder

os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
# 从BOS存储读取样例文件
image_url="https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T06%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe1865e4393da5a3515e90d72d81ef18296bd29598"
raw_image = requests.get(image_url).content
# 输入参数为一张图片
inp = appbuilder.Message(content={"raw_image": raw_image})
# 进行识别
mix_card_ocr = MixCardOCR()
out = mix_card_ocr.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '当身份证正反面在同一张图片上，需要识别图片中身份证正反面所有字段时，使用该工具', 'name': 'mixcard_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别文件的文件名', 'items': {'type': 'string'}, 'type': 'array'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'mixcard_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行身份证识别操作

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 包含待识别图片或图片下载URL的Message对象.
    示例: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”}).
  * **timeout** (*float* *,*  *可选*) – HTTP请求的超时时间，默认为None.
  * **retry** (*int* *,*  *可选*) – HTTP请求的重试次数，默认为0.
* **返回:**
  包含身份证识别结果的Message对象.
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

对指定文件进行OCR识别。

* **参数:**
  * **name** (*str*) – API名称。
  * **streaming** (*bool*) – 是否流式输出。如果为True，则逐个返回识别结果；如果为False，则一次性返回所有识别结果。
  * **\*\*kwargs** – 其他参数。
* **返回:**
  如果streaming为False，则返回包含所有识别结果的JSON字符串。
  如果streaming为True，则逐个返回包含识别结果的字典，每个字典包含以下字段：
  > type (str): 消息类型，固定为”text”。
  > text (str): 识别结果的JSON字符串。
  > visible_scope (str): 消息可见范围，可以是”llm”或”user”。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误，即文件URL不存在时抛出。

#### version *= 'v1'*

### *exception* appbuilder.NotFoundException

基类：`BaseRPCException`

NotFoundException represent HTTP Code 404.

### *class* appbuilder.ObjectRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

提供通用物体及场景识别能力，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的多
个物体及场景标签。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

object_recognition = appbuilder.ObjectRecognition()
with open("./object_recognition_test.jepg", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### manifests *= [{'description': '提供通用物体及场景识别能力，即对于输入的一张图片，输出图片中的多个物体及场景标签。', 'name': 'object_recognition', 'parameters': {'anyOf': [{'required': ['img_url']}, {'required': ['img_name']}], 'properties': {'img_name': {'description': '待识别图片的文件名,用于生成图片url', 'type': 'string'}, 'img_url': {'description': '待识别图片的url,根据该url能够获取图片', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'object_recognition'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

通用物体识别

* **参数:**
  * **(****obj** (*message*) – Message): 输入图片或图片url下载地址用于执行识别操作。
    例如: Message(content={“raw_image”: b”…”}) 或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间
  * **retry** (*int* *,*  *可选*) – HTTP重试次数
* **返回:**
  Message): 模型识别结果。
  : 例如: Message(content={“result”:[{“keyword”:”苹果”,
    : ”score”:0.94553,”root”:”植物-蔷薇科”},{“keyword”:”姬娜果”,”score”:0.730442,”root”:”植物-其它”},
      {“keyword”:”红富士”,”score”:0.505194,”root”:”植物-其它”}]})
* **返回类型:**
  message (obj

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

评估并识别传入图像中的物体或场景。

* **参数:**
  * **name** (*str*) – 调用此方法的对象名称。
  * **streaming** (*bool*) – 是否以流式方式返回结果。如果是True，则以生成器形式返回结果；如果是False，则直接返回字符串形式的识别结果。
  * **\*\*kwargs** – 任意关键字参数，支持以下参数：
    traceid (str, optional): 请求的追踪ID，用于追踪请求处理流程。默认为None。
    img_url (str, optional): 待识别图像的URL地址。默认为None，如果未指定，则尝试从file_urls和img_name参数中获取图像路径。
    file_urls (dict, optional): 包含文件名和对应URL的字典。默认为空字典。
    img_name (str, optional): 待识别图像的文件名。如果img_url未指定，则根据img_name从file_urls中获取图像的URL。默认为None。
    score_threshold (float, optional): 置信度阈值，低于此阈值的识别结果将被忽略。默认为0.5。
* **返回:**
  如果streaming为True，则返回一个生成器，生成器中的元素为包含识别结果的字典，字典包含以下键：
  : type (str): 结果类型，固定为”text”。
    text (str): 识别结果的JSON字符串表示。
    visible_scope (str): 结果的可见范围，’llm’表示仅对LLM可见，’user’表示对用户可见。

  如果streaming为False，则直接返回识别结果的JSON字符串表示。
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误（如未设置文件名或文件URL不存在），则抛出此异常。

#### version *= 'v1'*

### *class* appbuilder.OralQueryGeneration(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

口语化Query生成，可用于问答场景下对文档增强索引。
 *注：该组件推荐使用ERNIE Speed-AppBuilder模型。*

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
        '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
        '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
        '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
        '，实时视频分享您的生活。')
oral_query_generation = appbuilder.OralQueryGeneration(model='ERNIE Speed-AppBuilder')
answer = oral_query_generation(appbuilder.Message(text), query_type='全部', output_format='str')
print(answer.content)
```

#### completion(version, base_url, request, timeout: float = None, retry: int = 0)

Send a byte array of an audio file to obtain the result of speech recognition.

#### manifests *= [{'description': '输入文本、待生成的query类型和输出格式，生成query，并按照要求的格式进行输出。', 'name': 'query_generation', 'parameters': {'properties': {'output_format': {'description': '输出格式，可选json或str，str格式与老版本输出格式相同。', 'text': 'string'}, 'query_type': {'description': '待生成的query类型，可选问题、短语以及全部（问题 + 短语）。', 'text': 'string'}, 'text': {'description': '输入文本，组件会根据该输入文本生成query。', 'text': 'string'}}, 'required': ['text'], 'type': 'object'}}]*

#### meta

[`OralQueryGenerationArgs`](appbuilder.core.components.llms.oral_query_generation.md#appbuilder.core.components.llms.oral_query_generation.component.OralQueryGenerationArgs) 的别名

#### name *: str* *= 'query_generation'*

#### regenerate_output(model_output, output_format)

兼容老版本的输出格式

#### run(message, query_type='全部', output_format='str', stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息，包含query、context和answer等信息。这是一个必需的参数。
  * **query_type** (*str* *,*  *可选*) – 待生成的query类型，包括问题、短语和全部（问题+短语）。默认为全部。
  * **output_format** (*str* *,*  *可选*) – 输出格式，包括json和str，当stream为True时，只能以json形式输出。默认为str。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](#appbuilder.Message))

#### tool_eval(name: str, stream: bool = False, \*\*kwargs)

调用函数进行工具评估。

* **参数:**
  * **name** (*str*) – 评估工具的名称。
  * **stream** (*bool* *,* *optional*) – 是否以流的形式返回结果。默认为False。
  * **\*\*kwargs** – 关键字参数，可以包含以下参数：
    text (str): 需要评估的文本。
    query_type (str, optional): 查询类型，默认为’全部’。
    output_format (str, optional): 输出格式，默认为’str’。
    model_configs (dict, optional): 模型配置，默认为空字典。
* **返回:**
  如果stream为False，则返回评估结果列表；
  如果stream为True，则逐个返回评估结果。
* **抛出:**
  **ValueError** – 如果未提供text参数，则抛出ValueError异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.PPTGenerationFromFile(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文件生成PPT。

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

ppt_generator = appbuilder.PPTGenerationFromFile()
user_input = {
    'file_url': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx'
}
answer = ppt_generator(appbuilder.Message(user_input))
print(answer.content)
```

#### get_ppt_download_link(job_id: str, timeout: float = None)

获取PPT下载链接

* **参数:**
  * **job_id** (*str*) – 任务ID
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None。
* **返回:**
  PPT下载链接
* **返回类型:**
  str
* **抛出:**
  **Exception** – PPT生成请求错误

#### get_ppt_download_link_url *= '/ppt/text2ppt/apps/ppt-download'*

#### get_ppt_generation_status(job_id: str, request_times: int = 60, request_interval: int = 5, timeout: float = None)

轮询查看PPT生成状态

* **参数:**
  * **job_id** (*str*) – PPT生成任务的唯一标识符
  * **request_times** (*int* *,* *optional*) – 轮询请求次数，默认为60次。
  * **request_interval** (*int* *,* *optional*) – 每次轮询请求的间隔时间（秒），默认为5秒。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间（秒），默认为None，即无超时限制。
* **返回:**
  PPT生成状态码，1表示正在生成，2表示生成完成，3表示生成失败。
* **返回类型:**
  int
* **抛出:**
  **Exception** – 如果PPT生成状态码不为2（生成完成），则抛出异常。

#### get_ppt_generation_status_url *= '/ppt/text2ppt/apps/ppt-result'*

#### manifests *= [{'description': '根据上传的文件（非论文）生成PPT。', 'name': 'ppt_generation_from_file', 'parameters': {'properties': {'file_url': {'description': '用户上传的文件的链接。', 'text': 'string'}}, 'required': ['file_url'], 'type': 'object'}}]*

#### meta

`PPTGenerationFromFileArgs` 的别名

#### name *= 'ppt_generation_from_file'*

#### ppt_generation(post_data: dict, timeout: float = None)

创建PPT生成任务

* **参数:**
  * **post_data** (*dict*) – 包含PPT生成任务所需数据的字典
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None，表示不设置超时时间。
* **返回:**
  PPT生成任务的Job ID
* **返回类型:**
  str
* **抛出:**
  **Exception** – 如果PPT生成任务请求失败，抛出异常

#### ppt_generation_url *= '/ppt/text2ppt/apps/ppt-create-file'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), poll_request_times=60, poll_request_interval=5) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息，用于传入请求参数。
  * **poll_request_times** (*int*) – 轮询请求结果次数。
  * **poll_request_interval** (*int*) – 轮询请求的间隔时间（秒）。
* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](#appbuilder.Message))

#### tool_eval(stream: bool = False, \*\*kwargs)

用于执行function call的功能。

* **参数:**
  * **stream** (*bool* *,* *optional*) – 是否以生成器的方式返回结果，默认为False。
  * **\*\*kwargs** – 任意关键字参数，目前只支持’file_url’。
* **返回:**
  如果stream为False，则返回一个字符串，表示ppt下载链接。
  如果stream为True，则返回一个生成器，生成器产生一个字符串，表示ppt下载链接。
* **抛出:**
  **ValueError** – 如果’file_url’为空，则抛出异常。

#### uniform_prefix *= '/api/v1/component/component'*

#### version *: str*

### *class* appbuilder.PPTGenerationFromInstruction(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

指令生成PPT，可通过传入对PPT的描述或者自定义参数进行生成。

### 示例

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

ppt_generator = appbuilder.PPTGenerationFromInstruction()
input_data = {
    'text': '生成一个介绍北京的PPT。',
    'custom_data': {},
    'complex': 3,
    'user_name': '百度千帆AppBuilder'
}
answer = ppt_generator(appbuilder.Message(input_data))
print(answer.content)
```

#### get_ppt_download_link(job_id: str, timeout: float = None)

获取PPT下载链接

* **参数:**
  * **job_id** (*str*) – 作业ID
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None。
* **返回:**
  PPT下载链接
* **返回类型:**
  str
* **抛出:**
  **Exception** – 当PPT生成请求失败时抛出异常

#### get_ppt_download_link_url *= '/ppt/text2ppt/apps/ppt-download'*

#### get_ppt_generation_status(job_id: str, request_times: int = 60, request_interval: int = 5, timeout: float = None)

轮询查看PPT生成状态

* **参数:**
  * **job_id** (*str*) – PPT生成任务的唯一标识符
  * **request_times** (*int* *,* *optional*) – 轮询请求的次数，默认为60次。
  * **request_interval** (*int* *,* *optional*) – 每次轮询请求之间的间隔时间（秒），默认为5秒。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间（秒）。如果未设置，则使用http_client的默认超时时间。
* **返回:**
  PPT生成状态码。
  : - 1：正在生成
    - 2：生成完成
    - 3：生成失败
* **返回类型:**
  int
* **抛出:**
  **Exception** – PPT生成过程中出现异常时抛出。

#### get_ppt_generation_status_url *= '/ppt/text2ppt/apps/ppt-result'*

#### manifests *= [{'description': '根据输入指令生成PPT。', 'name': 'ppt_generation_from_instruction', 'parameters': {'properties': {'text': {'description': '用户请求生成PPT的指令。', 'example': '生成一个介绍北京的PPT。', 'text': 'string'}}, 'required': ['text'], 'type': 'object'}}]*

#### meta

`PPTGenerationFromInstructionArgs` 的别名

#### name *= 'ppt_generation_from_instruction'*

#### ppt_generation(post_data: dict, timeout: float = None)

创建PPT生成任务

* **参数:**
  * **post_data** (*dict*) – 请求数据
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None.
* **返回:**
  任务ID
* **返回类型:**
  str
* **抛出:**
  **Exception** – PPT生成请求失败

#### ppt_generation_url *= '/ppt/text2ppt/apps/ppt-create'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), poll_request_times=60, poll_request_interval=5) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息，用于传入请求参数。
  * **poll_request_times** (*int* *,* *optional*) – 轮询请求结果次数，默认为60。
  * **poll_request_interval** (*int* *,* *optional*) – 轮询请求的间隔时间（秒），默认为5。
* **返回:**
  模型运行后的输出消息，包含PPT下载链接。
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(stream: bool = False, \*\*kwargs)

评估给定的文本内容。

* **参数:**
  * **stream** (*bool* *,* *optional*) – 是否以生成器形式返回结果，默认为False。如果为True，则逐个生成下载链接；如果为False，则直接返回下载链接。
  * **\*\*kwargs** – 关键字参数，可以传递其他参数，但当前只使用 ‘text’ 参数。
* **返回:**
  如果 stream 为 False，则返回一个包含下载链接的字符串；如果 stream 为 True，则逐个生成下载链接。
* **抛出:**
  **ValueError** – 如果 ‘text’ 参数为空，则抛出此异常。

#### uniform_prefix *= '/api/v1/component/component'*

#### version *: str*

### *class* appbuilder.PPTGenerationFromPaper(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

论文生成PPT。

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

ppt_generator = appbuilder.PPTGenerationFromPaper()
user_input = {
    'file_key': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx'
}
answer = ppt_generator(appbuilder.Message(user_input))
print(answer.content)
```

#### get_ppt_download_link(job_id: str, timeout: float = None)

获取PPT下载链接

* **参数:**
  * **job_id** (*str*) – 任务ID
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None.
* **返回:**
  PPT下载链接
* **返回类型:**
  str
* **抛出:**
  **Exception** – PPT生成请求失败

#### get_ppt_download_link_url *= '/ppt/text2ppt/apps/ppt-download'*

#### get_ppt_generation_status(job_id: str, request_times: int = 60, request_interval: int = 5, timeout: float = None)

轮询查看PPT生成状态

* **参数:**
  * **job_id** (*str*) – 任务ID
  * **request_times** (*int* *,* *optional*) – 请求次数，默认为60次。
  * **request_interval** (*int* *,* *optional*) – 请求间隔时间，默认为5秒。
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None，即不设置超时时间。
* **返回:**
  PPT生成状态码。
  : - 1: PPT正在生成中
    - 2: PPT生成完成
    - 3: PPT生成失败
* **返回类型:**
  int
* **抛出:**
  **Exception** – PPT生成失败或请求失败时抛出异常。

#### get_ppt_generation_status_url *= '/ppt/text2ppt/apps/ppt-result'*

#### manifests *= [{'description': '根据上传的论文生成PPT。', 'name': 'ppt_generation_from_paper', 'parameters': {'properties': {'file_key': {'description': '用户上传的论文的链接。', 'text': 'string'}}, 'required': ['file_key'], 'type': 'object'}}]*

#### meta

`PPTGenerationFromPaperArgs` 的别名

#### name *= 'ppt_generation_from_paper'*

#### ppt_generation(post_data: dict, timeout: float = None)

创建PPT生成任务

* **参数:**
  * **post_data** (*dict*) – 发送的POST请求体数据
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None。
* **返回:**
  返回的任务ID
* **返回类型:**
  str
* **抛出:**
  **Exception** – 如果PPT生成请求失败，抛出异常

#### ppt_generation_url *= '/ppt/text2ppt/apps/ppt-create-thesis'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), poll_request_times=60, poll_request_interval=5) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入消息，用于传入请求参数。
  * **poll_request_times** (*int*) – 轮询请求结果次数，默认为60次。
  * **poll_request_interval** (*int*) – 轮询请求的间隔时间（秒），默认为5秒。
* **返回:**
  模型运行后的输出消息，包含PPT下载链接。
* **返回类型:**
  [Message](#appbuilder.Message)
* **抛出:**
  **Exception** – 当输入参数中缺少必要的键时，抛出异常。

#### tool_eval(stream: bool = False, \*\*kwargs)

使用指定的file_key来评估并获取相应的结果。

* **参数:**
  * **stream** (*bool* *,* *optional*) – 是否以生成器的方式逐项返回结果，默认为False。
  * **\*\*kwargs** – 关键字参数，用于传递其他参数，目前仅支持file_key。
* **返回:**
  如果stream为False，则直接返回结果。
  如果stream为True，则逐个返回结果。
* **抛出:**
  **ValueError** – 如果参数file_key为空，则抛出异常。

#### uniform_prefix *= '/api/v1/component/component'*

#### version *: str*

### *class* appbuilder.ParserConfig(\*, need_pdffile_data: bool = False, page_filter: List[int] = None, return_para_nodes: bool = True, erase_watermark: bool = False)

基类：`BaseModel`

DocParser解析配置

#### convert_file_to_pdf *: bool*

#### erase_watermark *: bool*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'convert_file_to_pdf': FieldInfo(annotation=bool, required=False, default=False, alias='need_pdffile_data', alias_priority=2), 'erase_watermark': FieldInfo(annotation=bool, required=False, default=False, alias='erase_watermark', alias_priority=2), 'page_filter': FieldInfo(annotation=List[int], required=False, alias='page_filter', alias_priority=2), 'return_para_node_tree': FieldInfo(annotation=bool, required=False, default=True, alias='return_para_nodes', alias_priority=2)}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### page_filter *: List[int]*

#### return_para_node_tree *: bool*

### *class* appbuilder.PlantRecognition(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

植物识别组件，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的植物识别结果

Examples:

```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
image_url = "https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2188d971ca547c53d01742af4a2cbe"

# 从BOS存储读取样例文件
raw_image = requests.get(image_url).content
inp = appbuilder.Message(content={"raw_image": raw_image})
# inp = Message(content={"url": image_url})

# 运行植物识别
plant_recognize = appbuilder.PlantRecognition()
out = plant_recognize.run(inp)
# 打印识别结果
print(out.content)
```

#### manifests *= [{'description': '用于识别图片中植物类别', 'name': 'plant_rec', 'parameters': {'anyOf': [{'required': ['img_name']}, {'required': ['img_url']}], 'properties': {'img_name': {'description': '待识别图片的文件名', 'type': 'string'}, 'img_url': {'description': '待识别图片的url', 'type': 'string'}}, 'type': 'object'}}]*

#### name *= 'plant_rec'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

输入图片并识别其中的植物

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={“raw_image”: b”…”})
  * **Message****(****content={"url"** ( *或*) – “[https://image/download/uel](https://image/download/uel)”}).
  * **timeout** (*float* *,* *optional*) – HTTP超时时间，默认为None
  * **retry** (*int* *,* *optional*) – HTTP重试次数，默认为0
* **返回:**
  模型识别结果
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(name: str, streaming: bool, origin_query: str, \*\*kwargs) → Generator[str, None, None] | str

用于工具的执行，通过调用底层接口进行植物识别

* **参数:**
  * **name** (*str*) – 工具名
  * **streaming** (*bool*) – 是否流式返回
  * **origin_query** (*str*) – 用户原始query
  * **\*\*kwargs** – 工具调用的额外关键字参数
* **返回:**
  植物识别结果，包括识别出的植物类别和相应的置信度信息
* **返回类型:**
  Union[Generator[str, None, None], str]

#### version *= 'v1'*

### *class* appbuilder.Playground(prompt_template=None, model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

空模板， 支持用户自定义prompt模板，并进行执行

Examples:

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = "..."

play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model="ERNIE Speed-AppBuilder")
play(appbuilder.Message({"name": "小明", "bot_name": "小红", "bot_type": "聊天机器人", "bot_function": "聊天", "bot_question": "你好吗？"}), stream=False)
```

#### meta

[`PlaygroundArgs`](appbuilder.core.components.llms.playground.md#appbuilder.core.components.llms.playground.component.PlaygroundArgs) 的别名

#### name *: str* *= 'playground'*

#### prompt_template *= ''*

#### run(message, stream=False, temperature=1e-10, top_p=0.0, max_output_tokens=1024, disable_search=True, response_format='text', stop=[], \*\*kwargs)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
  * **max_output_tokens** (*int* *,*  *可选*) – 指定生成的文本的最大长度，默认最大输出token数为1024, 最小为2，
    最大输出token与选择的模型有关。
  * **disable_search** (*bool* *,*  *可选*) – 是否强制关闭实时搜索功能，默认为 True，表示关闭。
  * **response_format** (*str* *,*  *可选*) – 指定返回的消息格式，默认为 ‘text’，以文本模式返回。
    可选 ‘json_object’，以 json 格式返回，但可能存在不满足效果的情况。
  * **stop** (*list* *[**str* *]* *,*  *可选*) – 生成停止标识，当模型生成结果以 stop 中某个元素结尾时，停止文本生成。
    每个元素长度不超过 20 字符，最多 4 个元素。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### variable_names *= {}*

#### version *: str* *= 'v1'*

### *exception* appbuilder.PreconditionFailedException

基类：`BaseRPCException`

PreconditionFailedException represent HTTP Code 412.

### *class* appbuilder.QAPairMining(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

基于输入文本内容，快速生成多个问题及对应答案,极大提高信息提炼的效率和准确性.广泛用于在线客服、智能问答等领域。

Examples:

#### meta

[`QAPairMiningMeta`](appbuilder.core.components.llms.qa_pair_mining.md#appbuilder.core.components.llms.qa_pair_mining.component.QAPairMiningMeta) 的别名

#### name *: str* *= 'qa_pair_mining'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.QRcodeOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

qrcode_ocr = appbuilder.QRcodeOCR()
with open("./qrcode_ocr_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read(),"location": "true"}))
print(out.content)
```

#### manifests *= [{'description': '需要对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息，使用该工具', 'name': 'qrcode_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别文件的文件名', 'items': {'type': 'string'}, 'type': 'array'}, 'location': {'description': '是否输出二维码/条形码位置信息', 'type': 'string'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'qrcode_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), location: str = 'true', timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行二维码识别操作。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 输入的图片或图片URL下载地址，用于执行识别操作。例如：
    Message(content={“raw_image”: b”…”, “location”: “”}) 或
    Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **location** (*str* *,*  *可选*) – 是否需要返回二维码位置信息，默认为 “true”。
  * **timeout** (*float* *,*  *可选*) – HTTP请求的超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP请求的重试次数。
* **返回:**
  识别结果，包含识别到的二维码信息。例如：
  : Message(name=msg, content={‘codes_result’: [{‘type’: ‘QR_CODE’, ‘text’: [’[http://weixin.qq.com/r/cS7M1PHE5qyZrbW393tj](http://weixin.qq.com/r/cS7M1PHE5qyZrbW393tj)’],
    : ’location’: {‘top’: 63, ‘left’: 950, ‘width’: 220, ‘height’: 211}}, …]}, mtype=dict)
* **返回类型:**
  [Message](#appbuilder.Message)
* **抛出:**
  **InvalidRequestArgumentError** – 如果 location 参数非法，将抛出该异常。

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

评估工具函数

* **参数:**
  * **name** (*str*) – 工具名称
  * **streaming** (*bool*) – 是否流式输出
  * **\*\*kwargs** – 其他关键字参数
* **关键字参数:**
  * **traceid** (*str*) – 请求的traceid
  * **file_names** (*List* *[**str* *]*) – 文件名列表
  * **locations** (*str*) – 是否需要获取位置信息，可选值为’true’或’false’，默认为’false’
  * **file_urls** (*Dict* *[**str* *,* *str* *]*) – 文件名到文件URL的映射
* **返回:**
  如果streaming为True，则返回一个生成器，生成两个字典，分别代表LLM和用户可见的内容；
  : 如果streaming为False，则返回一个JSON字符串，包含评估结果
* **返回类型:**
  Union[str, Generator[Dict[str, Any], None, None]]
* **抛出:**
  **InvalidRequestArgumentError** – 如果请求格式错误，或者位置信息不合法，则抛出该异常

#### version *= 'v1'*

### *class* appbuilder.QueryDecomposition(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

尝试对已经判定为复杂问题的原始问题进行拆解，把复杂问题拆解为一个个简单问题。广泛用于知识问答场景。

> Examples:

{}”.format(answer.content))

#### meta

[`QueryDecompositionMeta`](appbuilder.core.components.llms.query_decomposition.md#appbuilder.core.components.llms.query_decomposition.component.QueryDecompositionMeta) 的别名

#### name *: str* *= 'query_decomposition'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.QueryRewrite(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

多轮改写大模型组件， 基于生成式大模型进行多轮对话query改写的组件。它主要用于理解和优化用户与机器人的交互过程，进行指代消解及省略补全。该组件支持不同的改写类型，可根据对话历史生成更准确的用户查询。

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

query_rewrite = appbuilder.QueryRewrite(model="ERNIE Speed-AppBuilder")
answer = query_rewrite(appbuilder.Message(['我应该怎么办理护照？',
                                            '您可以查询官网或人工咨询',
                                            '我需要准备哪些材料？',
                                            '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》',
                                            '在哪里办']),
                                            rewrite_type="带机器人回复")
```

#### meta

[`QueryRewriteArgs`](appbuilder.core.components.llms.query_rewrite.md#appbuilder.core.components.llms.query_rewrite.component.QueryRewriteArgs) 的别名

#### name *: str* *= 'query_rewrite'*

#### run(message, rewrite_type='带机器人回复', stream=False, temperature=1e-10, top_p=0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **rewrite_type** (*str* *,*  *可选*) – 改写类型选项，可选值为 ‘带机器人回复’(改写时参考user查询历史和assistant回复历史)，
    ‘仅用户查询’(改写时参考user查询历史)。默认为”带机器人回复”。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj
* **抛出:**
  **ValueError** – 如果输入消息为空或不符合要求，将抛出 ValueError 异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.Reranker(model='bce-reranker-base')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

Examples:

```python
import os
import appbuilder
from appbuilder import Message

os.environ["APPBUILDER_TOKEN"] = '...'

reranker = appbuilder.Reranker()
ranked_1 = reranker("你好", ["他也好", "hello?"])
print(ranked_1)
```

#### accepted_models *= ['bce-reranker-base']*

#### base_urls *= {'bce-reranker-base': '/api/v1/component/component/bce_reranker_base'}*

#### meta

[`RerankerArgs`](appbuilder.core.components.retriever.reranker.md#appbuilder.core.components.retriever.reranker.rerank.RerankerArgs) 的别名

#### name *: str* *= 'reranker'*

#### run(query: [Message](appbuilder.core.md#appbuilder.core.message.Message)[str] | str, texts: [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]] | List[str]) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[dict]]

运行查询，对给定的文本集合进行批量处理，并返回处理后的结果列表。

* **参数:**
  * **query** (*Union* *[*[*Message*](#appbuilder.Message) *[**str* *]* *,* *str* *]*) – 查询条件，可以是字符串或Message对象。
  * **texts** (*Union* *[*[*Message*](#appbuilder.Message) *[**List* *[**str* *]* *]* *,* *List* *[**str* *]* *]*) – 待处理的文本集合，可以是字符串列表或包含字符串列表的Message对象。
* **返回:**
  处理后的结果列表，每个元素是一个字典，包含处理后的文本信息。
* **返回类型:**
  [Message](#appbuilder.Message)[List[dict]]

#### version *: str* *= 'v1'*

### *class* appbuilder.SimilarQuestion(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

基于输入的问题, 挖掘出与该问题相关的类似问题。广泛用于客服、问答等场景。
: Examples:

{}”.format(answer.content))

#### manifests *= [{'description': '基于输入的问题，挖掘出与该问题相关的类似问题。', 'name': 'similar_question', 'parameters': {'properties': {'query': {'description': '输入的问题，用于大模型根据该问题输出相关的类似问题。', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

[`SimilarQuestionMeta`](appbuilder.core.components.llms.similar_question.md#appbuilder.core.components.llms.similar_question.component.SimilarQuestionMeta) 的别名

#### name *: str* *= 'similar_question'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0, request_id=None)

给定输入（message）到模型运行，同时指定运行参数，并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### tool_eval(name: str, streaming: bool = False, \*\*kwargs)

执行函数调用的评估工具。

* **参数:**
  * **name** (*str*) – 函数名。
  * **streaming** (*bool* *,* *optional*) – 是否以流式方式输出结果。默认为False。
  * **\*\*kwargs** – 

    其他关键字参数，包括：
    traceid (str, optional): 请求的追踪ID。
    query (str): 输入的查询字符串。
    model_configs (dict, optional): 模型配置字典，包括：
    > temperature (float, optional): 温度参数，用于控制输出结果的多样性。默认为1e-10。
    > top_p (float, optional): 截断概率，用于控制生成文本的质量。默认为0.0。
* **返回:**
  如果streaming为False，则返回评估结果的字符串表示。
  如果streaming为True，则生成评估结果的字符串表示的迭代器。
* **抛出:**
  **ValueError** – 如果未提供query参数，则抛出此异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.StreamRunContext

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

### *class* appbuilder.StyleRewrite(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

文本风格转写大模型组件， 基于生成式大模型对文本的风格进行改写，支持有营销、客服、直播、激励及教学五种话术。

Examples:

```python
import os
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'

style_rewrite = appbuilder.StyleRewrite(model="ERNIE Speed-AppBuilder")
answer = style_rewrite(appbuilder.Message("文心大模型发布新版本"), style="激励话术")
```

#### manifests *= [{'description': '能够将一段文本转换成不同的风格（营销、客服、直播、激励及教学话术），同时保持原文的基本意义不变。', 'name': 'style_rewrite', 'parameters': {'properties': {'query': {'description': '需要改写的文本。', 'type': 'string'}, 'style': {'description': '想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选. 默认是营销话术。', 'enum': ['营销话术', '客服话术', '直播话术', '激励话术', '教学话术'], 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

[`StyleRewriteArgs`](appbuilder.core.components.llms.style_rewrite.md#appbuilder.core.components.llms.style_rewrite.component.StyleRewriteArgs) 的别名

#### name *: str* *= 'style_rewrite'*

#### run(message, style='营销话术', stream=False, temperature=1e-10, top_p=0.0, request_id=None)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **style** (*str* *,* *optional*) – 想要转换的文本风格，目前有营销、客服、直播、激励及教学五种话术可选。默认为”营销话术”。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### tool_eval(name: str, streaming: bool = False, \*\*kwargs)

执行工具评估函数

* **参数:**
  * **name** (*str*) – 函数名称，本函数不使用该参数，但保留以符合某些框架的要求。
  * **streaming** (*bool* *,* *optional*) – 是否以流的形式返回结果。默认为 False，即一次性返回结果。如果设置为 True，则以生成器形式逐个返回结果。
  * **\*\*kwargs** – 

    其他参数，包含但不限于：
    traceid (str): 请求的跟踪ID，用于日志记录和跟踪。
    query (str): 待评估的文本。
    style (str, optional): 评估风格，可选值为 [‘营销话术’, ‘客服话术’, ‘直播话术’, ‘激励话术’, ‘教学话术’]。默认为 ‘营销话术’。
    model_configs (dict, optional): 模型配置参数，可选的键包括：
    > temperature (float, optional): 温度参数，用于控制生成文本的随机性。默认为 1e-10。
    > top_p (float, optional): top_p 采样参数，用于控制生成文本的多样性。默认为 0.0。
* **返回:**
  如果 streaming 为 False，则直接返回评估结果字符串。
  如果 streaming 为 True，则以生成器形式逐个返回评估结果字符串。
* **抛出:**
  **ValueError** – 如果缺少参数 ‘query’。

#### version *: str* *= 'v1'*

### *class* appbuilder.StyleWriting(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

风格写作大模型组件， 基于生成式大模型进行风格写作，支持B站、小红书等多种风格，可用于文案、广告等多种场景。

Examples:

```python
import os
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

style_writing = appbuilder.StyleWriting(model="ERNIE Speed-AppBuilder")
answer = style_writing(appbuilder.Message("帮我写一篇关于人体工学椅的文案"), style_query="小红书", length=100)
```

#### manifests *= [{'description': '根据用户输入的文案要求和文案风格，生成符合特定风格的产品介绍或宣传文案。目前支持生成小红书风格、B站风格或通用风格的文案。', 'name': 'style_writing', 'parameters': {'properties': {'length': {'description': '用于定义输出内容的长度。有效的选项包括 100（短）、300（中）、600（长），默认值为 100。', 'enum': [100, 300, 600], 'type': 'integer'}, 'query': {'description': '用于描述生成文案的主题和要求。', 'type': 'string'}, 'style': {'description': '用于定义文案生成的风格，包括通用、B站、小红书，默认为通用。', 'enum': ['通用', 'B站', '小红书'], 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### meta

[`StyleWritingArgs`](appbuilder.core.components.llms.style_writing.md#appbuilder.core.components.llms.style_writing.component.StyleWritingArgs) 的别名

#### name *: str* *= 'style_writing'*

#### run(message, style_query='通用', length=100, stream=False, temperature=1e-10, top_p=0, request_id=None)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
  * **style_query** (*str*) – 风格查询选项，用于指定写作风格。有效的选项包括 ‘B站’, ‘小红书’, ‘通用’。默认值为 ‘通用’。
  * **length** (*int*) – 输出内容的长度。有效的选项包括 100（短），300（中），600（长）。默认值为 100。
  * **stream** (*bool* *,* *optional*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,* *optional*) – 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,* *optional*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### tool_eval(name: str, streaming: bool = False, \*\*kwargs)

对指定的工具进行函数调用评估。

* **参数:**
  * **name** (*str*) – 工具名称。
  * **streaming** (*bool* *,* *optional*) – 是否以流的方式返回结果。默认为False。
  * **\*\*kwargs** – 其他参数。
* **返回:**
  如果 streaming 为 False，则返回评估结果字符串；如果 streaming 为 True，则返回一个生成器，每次迭代返回评估结果字符串的一部分。
* **返回类型:**
  str 或 generator
* **抛出:**
  **ValueError** – 如果未提供必要的参数 ‘query’。

#### version *: str* *= 'v1'*

### *class* appbuilder.TTS(\*args, \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文本转语音组件，即输入一段文本将其转为一段语音

Examples:

```python
import appbuilder
os.environ["APPBUILDER_TOKEN"] = '...'
tts = appbuilder.TTS()

# 默认使用baidu-tts模型, 默认返回MP3格式
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp)
with open("sample.mp3", "wb") as f:
    f.write(out.content["audio_binary"])

# 使用paddlespeech-tts模型，目前只支持返回WAV格式
inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
out = tts.run(inp, model="paddlespeech-tts", audio_type="wav")
with open("sample.wav", "wb") as f:
    f.write(out.content["audio_binary"])
```

#### Baidu_TTS *= 'baidu-tts'*

#### PaddleSpeech_TTS *= 'paddlespeech-tts'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), model: Literal['baidu-tts', 'paddlespeech-tts'] = 'baidu-tts', speed: int = 5, pitch: int = 5, volume: int = 5, person: int = 0, audio_type: Literal['mp3', 'wav', 'pcm'] = 'mp3', timeout: float = None, retry: int = 0, stream: bool = False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

执行文本转语音。

* **参数:**
  * **(****obj** (*message*) – Message): 待转为语音的文本。举例: Message(content={“text”: “欢迎使用百度语音”})如果选择\`baidu-tts\`模型，

    ```
    `
    ```

    text\`最大文本长度为1024 GBK编码长度,大约为512个中英文字符;如果选择\`paddlespeech-tts\`模型, 

    ```
    `
    ```

    text\`最大文本长度是510个字符。
  * **model** (*str* *,*  *可选*) – 默认是\`baidu-tts\`模型，可设置为\`paddlespeech-tts\`。
  * **speed** (*int* *,*  *可选*) – 语音语速，默认是5中等语速，取值范围在0~15之间，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **pitch** (*int* *,*  *可选*) – 语音音调，默认是5中等音调，取值范围在0~15之间，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **volume** (*int* *,*  *音量*) – 语音音量，默认是5中等音量，取值范围在0~15之间，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **person** (*int* *,*  *可选*) – 语音人物特征，默认是0,
    可选值包括度小宇=1 度小美=0 度逍遥（基础）=3 度丫丫=4 度逍遥（精品）=5003
    度小鹿=5118 度博文=106 度小童=110 度小萌=111 度米朵=103 度小娇=5，
    如果选择模型为paddlespeech-tts，参数自动失效。
  * **audio_type** (*str* *,*  *可选*) – 音频文件格式，默认是\`mp3\`，
    如果选择\`paddlespeech-tts\`模型，参数只能设为\`wav\`。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP重试次数。
  * **stream** (*bool* *,*  *可选*) – 是否以流的形式返回音频数据，默认为False。
* **返回:**
  Message): 文本转语音结果。举例: Message(content={“audio_binary”: b”xxx”, “audio_type”: “mp3”})
* **返回类型:**
  message (obj

### *class* appbuilder.TableOCR(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

支持识别图片中的表格内容，返回各表格的表头表尾内容、单元格文字内容及其行列位置信息，全面覆盖各类表格样式，包括常规有线表格、
无线表格、含合并单元格表格。同时，支持多表格内容识别。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

table_ocr = appbuilder.TableOCR()
with open("./table_ocr_test.png", "rb") as f:
    out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
print(out.content)
```

#### get_table_markdown(tables_result)

将表格识别结果转换为Markdown格式。

* **参数:**
  **tables_result** (*list*) – 表格识别结果列表，每个元素是一个包含表格数据的字典，其中包含表格体（body）等字段。
* **返回:**
  包含Markdown格式表格的字符串列表。
* **返回类型:**
  list

#### manifests *= [{'description': '需要识别图片中的表格内容，使用该工具, 但不支持html后缀文件的识别', 'name': 'table_ocr', 'parameters': {'properties': {'file_names': {'description': '待识别图片的文件名', 'items': {'type': 'string'}, 'type': 'array'}}, 'required': ['file_names'], 'type': 'object'}}]*

#### name *= 'table_ocr'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

表格文字识别

* **参数:**
  * **(****obj** (*message*) – Message): 输入图片或图片url下载地址用于执行识别操作。
    举例: Message(content={“raw_image”: b”…”})
    或 Message(content={“url”: “[https://image/download/url](https://image/download/url)”})。
  * **timeout** (*float* *,*  *可选*) – HTTP超时时间。
  * **retry** (*int* *,*  *可选*) – HTTP重试次数。
* **返回:**
  Message): 识别结果。
  : 举例: Message(name=msg, content={‘tables_result’: [{
    ‘table_location’: [{‘x’: 15, ‘y’: 15}, {‘x’: 371, ‘y’: 15}, {‘x’: 371, ‘y’: 98}, {‘x’: 15,
    ‘y’: 98}], ‘header’: [], ‘body’: [{‘cell_location’: [{‘x’: 15, ‘y’: 15}, {‘x’: 120, ‘y’: 15},
    {‘x’: 120, ‘y’: 58}, {‘x’: 15, ‘y’: 58}], ‘row_start’: 0, ‘row_end’: 1, ‘col_start’: 0,
    ‘col_end’: 1, ‘words’: ‘参数’}, {‘cell_location’: [{‘x’: 120, ‘y’: 15}, {‘x’: 371, ‘y’: 15},
    {‘x’: 371, ‘y’: 58}, {‘x’: 120, ‘y’: 58}], ‘row_start’: 0, ‘row_end’: 1, ‘col_start’: 1,
    ‘col_end’: 2, ‘words’: ‘值’}, {‘cell_location’: [{‘x’: 15, ‘y’: 58}, {‘x’: 120, ‘y’: 58},
    {‘x’: 120, ‘y’: 98}, {‘x’: 15, ‘y’: 98}], ‘row_start’: 1, ‘row_end’: 2, ‘col_start’: 0,
    ‘col_end’: 1, ‘words’: ‘Content-Type’}, {‘cell_location’: [{‘x’: 120, ‘y’: 58}, {‘x’: 371,
    ‘y’: 58}, {‘x’: 371, ‘y’: 98}, {‘x’: 120, ‘y’: 98}], ‘row_start’: 1, ‘row_end’: 2, ‘col_start’:
    1, ‘col_end’: 2, ‘words’: ‘application/x-www-form-urlencoded’}], ‘footer’: []}]}, mtype=dict)
* **返回类型:**
  message (obj

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

对传入文件进行处理，并返回处理结果。

* **参数:**
  * **name** (*str*) – 工具的名称。
  * **streaming** (*bool*) – 是否为流式处理。若为True，则以生成器形式返回结果；若为False，则直接返回结果。
  * **\*\*kwargs** – 关键字参数，包含以下参数：
    traceid (str): 请求的唯一标识符。
    file_names (List[str]): 文件名列表，表示需要处理的文件名。
    files (List[str]): 同file_names，用于兼容老版本接口。
    file_urls (Dict[str, str]): 文件名和对应URL的映射字典。
* **返回:**
  若streaming为True，则以生成器形式返回处理结果，每个元素为包含type和text的字典，type固定为”text”，text为处理结果的JSON字符串。
  若streaming为False，则直接返回处理结果的JSON字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 若传入文件名在file_urls中未找到对应的URL，则抛出此异常。

#### version *= 'v1'*

### *class* appbuilder.TableParams(dimension: int, table_name: str = 'AppBuilderTable', replication: int = 3, partition: int = 1, index_type: str = 'HNSW', metric_type: str = 'L2', drop_exists: bool = False, vector_params: Dict = None)

基类：`object`

Baidu VectorDB table params.
See the following documentation for details:
[https://cloud.baidu.com/doc/VDB/s/mlrsob0p6](https://cloud.baidu.com/doc/VDB/s/mlrsob0p6)
:param dimension int: The dimension of vector.
:param replication int: The number of replicas in the table.
:param partition int: The number of partitions in the table.
:param index_type: HNSW, FLAT… Default value is “HNSW”
:type index_type: Optional[str]
:param metric_type: L2, COSINE, IP. Default value is “L2”
:type metric_type: Optional[str]
:param drop_exists: Delete the existing Table. Default value is False.
:type drop_exists: Optional[bool]
:param vector_params: if HNSW set parameters: M and efConstruction, for example {‘M’: 16, efConstruction: 200}

> default is HNSW

### *class* appbuilder.TagExtraction(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

标签抽取组件，基于生成式大模型进行关键标签的抽取。

Examples:

```python
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

tag_extraction = appbuilder.TagExtraction(model="ERNIE Speed-AppBuilder")
answer = tag_extraction(appbuilder.Message("从这段文本中抽取关键标签"))
```

#### meta

[`TagExtractionArgs`](appbuilder.core.components.llms.tag_extraction.md#appbuilder.core.components.llms.tag_extraction.component.TagExtractionArgs) 的别名

#### name *: str* *= 'tag_extraction'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **(****obj** (*message*) – Message, 必选): 输入消息，用于模型的主要输入内容。
  * **stream** (*bool* *,*  *可选*) – 指定是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。
    默认值为 0。
* **返回:**
  Message: 模型运行后的输出消息。
* **返回类型:**
  obj

#### version *: str* *= 'v1'*

### *class* appbuilder.Text2Image(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文生图组件，即对于输入的文本，输出生成的图片url。

Examples:

```python
import appbuilder
text_to_image = appbuilder.Text2Image()
os.environ["APPBUILDER_TOKEN"] = '...'
content_data = {"prompt": "上海的经典风景", "width": 1024, "height": 1024, "image_num": 1}
msg = appbuilder.Message(content_data)
out = text_to_image.run(inp)
# 打印生成结果
print(out.content) # eg: {"img_urls": ["xxx"]}
```

#### *static* check_service_error(request_id: str, data: dict)

个性化服务response参数检查

参数:
: request (dict) : 文生图生成结果body返回

返回：
: 无

#### extract_img_urls(response: Text2ImageQueryResponse)

提取图片的url。

参数:
: response (obj:Text2ImageQueryResponse): A作画生成的返回结果。

返回:
: List[str]:img_urls: 从返回体中提取的图片url列表。

#### manifests *= [{'description': '文生图，该组件只用于图片创作。当用户需要进行场景、人物、海报等内容的绘制时，使用该画图组件。如果用户需要生成图表（柱状图、折线图、雷达图等），则必须使用代码解释器。', 'name': 'text_to_image', 'parameters': {'properties': {'query': {'description': '文生图用的query。特别注意，这个字段只能由中文字符组成，不能含有任何英语描述。', 'type': 'string'}}, 'required': ['query'], 'type': 'object'}}]*

#### queryText2ImageData(request: Text2ImageQueryRequest, timeout: float = None, retry: int = 0, request_id: str = None) → Text2ImageQueryResponse

使用给定的输入并返回文生图的结果。

参数:
: request (obj:Text2ImageQueryRequest): 输入请求，这是一个必需的参数。
  timeout (float, 可选): 请求的超时时间。
  retry (int, 可选): 请求的重试次数。

返回:
: obj:Text2ImageQueryResponse: 接口返回的输出消息。

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), width: int = 1024, height: int = 1024, image_num: int = 1, image: str | None = None, url: str | None = None, pdf_file: str | None = None, pdf_file_num: str | None = None, change_degree: int | None = None, text_content: str | None = None, task_time_out: int | None = None, text_check: int | None = 1, request_id: str | None = None)

执行文本到图像的生成任务。

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 包含任务相关信息的消息对象。
  * **width** (*int* *,* *optional*) – 生成的图像的宽度，默认为1024。
  * **height** (*int* *,* *optional*) – 生成的图像的高度，默认为1024。
  * **image_num** (*int* *,* *optional*) – 生成图像的数量，默认为1。
  * **image** (*Optional* *[**str* *]* *,* *optional*) – 参考图像的路径或URL，默认为None。
  * **url** (*Optional* *[**str* *]* *,* *optional*) – 参考图像的URL，默认为None。
  * **pdf_file** (*Optional* *[**str* *]* *,* *optional*) – 参考PDF文件的路径，默认为None。
  * **pdf_file_num** (*Optional* *[**str* *]* *,* *optional*) – 参考PDF文件中的页码范围，默认为None。
  * **change_degree** (*Optional* *[**int* *]* *,* *optional*) – 图像变换的程度，默认为None。
  * **text_content** (*Optional* *[**str* *]* *,* *optional*) – 需要转换的文本内容，默认为None。
  * **task_time_out** (*Optional* *[**int* *]* *,* *optional*) – 任务超时时间，默认为None。
  * **text_check** (*Optional* *[**int* *]* *,* *optional*) – 是否进行文本内容检查，默认为1。
  * **request_id** (*Optional* *[**str* *]* *,* *optional*) – 请求的唯一标识，默认为None。
* **返回:**
  包含生成图像URL的消息对象。
* **返回类型:**
  [Message](#appbuilder.Message)
* **抛出:**
  **HTTPError** – 请求失败时抛出异常。

#### submitText2ImageTask(request: Text2ImageSubmitRequest, timeout: float = None, retry: int = 0, request_id: str = None) → Text2ImageSubmitResponse

使用给定的输入并返回文生图的任务信息。

* **参数:**
  * **(****obj** (*request*) – Text2ImageSubmitRequest): 输入请求，这是一个必需的参数。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间。默认为None。
  * **retry** (*int* *,* *optional*) – 请求的重试次数。默认为0。
  * **request_id** (*str* *,* *optional*) – 请求的唯一标识符。默认为None。
* **返回:**
  Text2ImageSubmitResponse: 接口返回的输出消息。
* **返回类型:**
  obj

### *class* appbuilder.Translation(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文本翻译组件,可支持中、英、日、韩等200+语言互译，100+语种自动检测。
支持语种列表可参照 [https://ai.baidu.com/ai-doc/MT/4kqryjku9#%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8](https://ai.baidu.com/ai-doc/MT/4kqryjku9#%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8)

Examples:

```python
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = '...'

translate = appbuilder.Translation()
resp = translate(appbuilder.Message("你好\n中国"), to_lang="en")
# 输出 {'from_lang':'zh', 'to_lang':'en', 'trans_result':[{'src':'你好','dst':'hello'},{'src':'中国','dst':'China'}]}
print(resp.content)
```

#### manifests *= [{'description': '文本翻译通用版工具，会根据指定的目标语言对文本进行翻译，并返回翻译后的文本。', 'name': 'translation', 'parameters': {'properties': {'q': {'description': '需要翻译的源文本，文本翻译工具会将该文本翻译成对应的目标语言', 'type': 'string'}, 'to_lang': {'description': "翻译的目标语言类型，'en'表示翻译成英语, 'zh'表示翻译成中文，'yue'表示翻译成粤语，'wyw'表示翻译成文言文，'jp'表示翻译成日语，'kor'表示翻译成韩语，'fra'表示翻译成法语，'spa'表示翻译成西班牙语，'th'表示翻译成泰语,'ara'表示翻译成阿拉伯语，'ru'表示翻译成俄语，'pt'表示翻译成葡萄牙语，'de'表示翻译成德语，'it'表示翻译成意大利语，'el'表示翻译成希腊语，'nl'表示翻译成荷兰语,'pl'表示翻译成波兰语,'bul'表示翻译成保加利亚语，'est'表示翻译成爱沙尼亚语，'dan'表示翻译成丹麦语, 'fin'表示翻译成芬兰语，'cs'表示翻译成捷克语，'rom'表示翻译成罗马尼亚语，'slo'表示翻译成斯洛文尼亚语，'swe'表示翻译成瑞典语，'hu'表示翻译成匈牙利语，'cht'表示翻译成繁体中文，'vie'表示翻译成越南语，默认为'en'", 'enum': ['en', 'zh', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it', 'el', 'nl', 'pl', 'bul', 'est', 'dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie'], 'type': 'string'}}, 'required': ['q'], 'type': 'object'}}]*

#### name *= 'translate'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), from_lang: str = 'auto', to_lang: str = 'en', timeout: float = None, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

根据提供的文本以及语种参数执行文本翻译

* **参数:**
  * **message** ([*Message*](#appbuilder.Message)) – 翻译文本。
  * **from_lang** (*str*) – 翻译的源语言。默认为 “auto”。
  * **to_lang** (*str*) – 翻译的目标语言。默认为 “en”。
  * **timeout** (*float* *,* *optional*) – 翻译请求的超时时间。
  * **retry** (*int* *,* *optional*) – 重试次数。
* **返回:**
  返回的文本翻译结果。
  例如，Message(content={‘from_lang’: ‘zh’, ‘to_lang’: ‘en’, ‘trans_result’: [{‘src’: ‘你好’, ‘dst’: ‘hello’}]})
* **返回类型:**
  [Message](#appbuilder.Message)

#### tool_eval(name: str, streaming: bool, \*\*kwargs)

工具函数，用于翻译指定的文本。

* **参数:**
  * **name** (*str*) – 函数名称，此参数在本函数中未使用。
  * **streaming** (*bool*) – 是否流式输出翻译结果。
  * **\*\*kwargs** – 关键字参数，可以包含以下参数：
    - traceid (str, optional): 请求的唯一标识符，默认为None。
    - q (str): 待翻译的文本。
    - to_lang (str, optional): 目标语言代码，默认为”en”。
* **返回:**
  如果streaming为True，则返回生成器，生成包含翻译结果的字典；
  如果streaming为False，则返回包含翻译结果的JSON字符串。
* **抛出:**
  **InvalidRequestArgumentError** – 如果未设置参数”q”，则抛出此异常。

#### version *= 'v1'*

### appbuilder.get_all_apps()

获取所有应用列表。

* **参数:**
  **无参数。**
* **返回:**
  包含所有应用信息的列表，每个元素为一个App对象，
  其中App对象的结构取决于get_app_list函数的返回结果。
* **返回类型:**
  List[App]

### appbuilder.get_app_list(limit: int = 10, after: str = '', before: str = '', secret_key: str | None = None, gateway_v2: str | None = None) → list[AppOverview]

该接口查询用户下状态为已发布的应用列表

* **参数:**
  * **limit** (*int* *,* *optional*) – 返回结果的最大数量，默认值为10。
  * **after** (*str* *,* *optional*) – 返回结果中第一个应用的游标值，用于分页查询。默认值为空字符串。
  * **before** (*str* *,* *optional*) – 返回结果中最后一个应用的游标值，用于分页查询。默认值为空字符串。
  * **secret_key** (*Optional* *[**str* *]* *,* *optional*) – 认证密钥。如果未指定，则使用默认的密钥。默认值为None。
  * **gateway_v2** (*Optional* *[**str* *]* *,* *optional*) – 网关地址。如果未指定，则使用默认的地址。默认值为None。
* **返回:**
  应用列表。
* **返回类型:**
  list[data_class.AppOverview]

### appbuilder.get_model_list(secret_key: str = '', api_type_filter: List[str] = [], is_available: bool = False) → list

返回用户的模型列表。

参数:
: secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv(“APPBUILDER_TOKEN”, “”)。
  api_type_filter(List[str], 可选): 根据apiType过滤，[“chat”, “completions”, “embeddings”, “text2image”]，不填包括所有的。
  is_available(bool, 可选): 是否返回可用模型列表, 默认返回所有模型。

返回:
: list: 模型列表。
