# appbuilder.core.components.rag_with_baidu_search_pro package

## Submodules

## appbuilder.core.components.rag_with_baidu_search_pro.component module

### *class* appbuilder.core.components.rag_with_baidu_search_pro.component.RagWithBaiduSearchPro(model: str, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False, instruction: [Message](appbuilder.core.md#appbuilder.core.message.Message) | None = None)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

RagWithBaiduSearchPro 组件

#### meta *: [RagWithBaiduSearchProArgs](#appbuilder.core.components.rag_with_baidu_search_pro.component.RagWithBaiduSearchProArgs)*

#### name *= 'rag_with_baidu_search_pro'*

#### run(message, stream=False, instruction=None, model=None, temperature=1e-10, top_p=1e-10, search_top_k=4, hide_corner_markers=True)

执行模型推理。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 待处理的信息对象。
  * **stream** (*bool* *,* *optional*) – 是否以流的形式接收响应数据。默认为False。
  * **instruction** (*Instruction* *,* *optional*) – 指令信息对象。默认为None。
  * **model** (*str* *,* *optional*) – 模型名称。默认为None，表示使用当前实例的模型。
  * **temperature** (*float* *,* *optional*) – 温度参数，控制生成文本的随机性。默认为1e-10。
  * **top_p** (*float* *,* *optional*) – 累积概率阈值，用于控制生成文本的多样性。默认为1e-10。
  * **search_top_k** (*int* *,* *optional*) – 搜索候选结果的数量。默认为4。
  * **hide_corner_markers** (*bool* *,* *optional*) – 是否隐藏响应中的边界标记。默认为True。
* **返回:**
  处理后的信息对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **AppBuilderServerException** – 如果输入信息或指令过长，将抛出此异常。

#### set_secret_key_and_gateway(\*\*kwargs)

#### version *= 'v1'*

### *class* appbuilder.core.components.rag_with_baidu_search_pro.component.RagWithBaiduSearchProArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, query: Annotated[str, MaxLen(max_length=300)])

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

RagWithBaiduSearchPro 的参数

* **参数:**
  **query** (*str*) – 用户的 query 输入

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'name': FieldInfo(annotation=str, required=False, default=''), 'query': FieldInfo(annotation=str, required=True, description='用户的 query 输入', metadata=[MaxLen(max_length=300)]), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### query *: str*

### *class* appbuilder.core.components.rag_with_baidu_search_pro.component.RagWithBaiduSearchProRequest(\*, message: object, stream: bool = False, instruction: str, model: str | None = None, temperature: Annotated[float, None, Interval(gt=None, ge=0, lt=None, le=1), None, None] = 1e-10, top_p: Annotated[float, None, Interval(gt=None, ge=0, lt=None, le=1), None, None] = 1e-10, search_top_k: Annotated[int, None, Interval(gt=None, ge=1, lt=None, le=None), None] = 4, hide_corner_markers: bool = True)

基类：`BaseModel`

RagWithBaiduSearchPro 的请求

#### message

用户的消息

* **Type:**
  object

#### stream

是否流式处理

* **Type:**
  bool

#### instruction

指令

* **Type:**
  str

#### model

模型名称

* **Type:**
  Optional[str]

#### temperature

温度，范围在0到1之间

* **Type:**
  confloat(ge=0, le=1)

#### top_p

top_p，范围在0到1之间

* **Type:**
  confloat(ge=0, le=1)

#### search_top_k

search_top_k，

* **Type:**
  conint(ge=1)

#### hide_corner_markers *: bool*

#### instruction *: str*

#### message *: object*

#### model *: str | None*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'hide_corner_markers': FieldInfo(annotation=bool, required=False, default=True), 'instruction': FieldInfo(annotation=str, required=True), 'message': FieldInfo(annotation=object, required=True), 'model': FieldInfo(annotation=Union[str, NoneType], required=False), 'search_top_k': FieldInfo(annotation=int, required=False, default=4, description='search_top_k必须是大于等于1的整数', metadata=[None, Interval(gt=None, ge=1, lt=None, le=None), None]), 'stream': FieldInfo(annotation=bool, required=False, default=False), 'temperature': FieldInfo(annotation=float, required=False, default=1e-10, description='temperature范围在0到1之间', metadata=[None, Interval(gt=None, ge=0, lt=None, le=1), None, None]), 'top_p': FieldInfo(annotation=float, required=False, default=1e-10, description='top_p范围在0到1之间', metadata=[None, Interval(gt=None, ge=0, lt=None, le=1), None, None])}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### search_top_k *: Annotated[int, None, Interval(gt=None, ge=1, lt=None, le=None), None]*

#### stream *: bool*

#### temperature *: Annotated[float, None, Interval(gt=None, ge=0, lt=None, le=1), None, None]*

#### top_p *: Annotated[float, None, Interval(gt=None, ge=0, lt=None, le=1), None, None]*

## appbuilder.core.components.rag_with_baidu_search_pro.parse_rag_pro_response module

### *class* appbuilder.core.components.rag_with_baidu_search_pro.parse_rag_pro_response.ParseRagProResponse(response, stream: bool = False)

基类：`CompletionResponse`

#### message_iterable_wrapper(message)

对模型输出的 Message 对象进行包装。
当 Message 是流式数据时，数据被迭代完后，将重新更新 content 为 blocking 的字符串。
