# appbuilder.core.components.rag_with_baidu_search package

## Submodules

## appbuilder.core.components.rag_with_baidu_search.component module

### *class* appbuilder.core.components.rag_with_baidu_search.component.RAGWithBaiduSearch(model, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False, instruction: [Message](appbuilder.core.md#appbuilder.core.message.Message) | None = None, reject: bool | None = False, clarify: bool | None = False, highlight: bool | None = False, friendly: bool | None = False, cite: bool | None = False)

基类：`CompletionBaseComponent`

#### meta *: [RAGWithBaiduSearchArgs](#appbuilder.core.components.rag_with_baidu_search.component.RAGWithBaiduSearchArgs)*

#### name *: str* *= 'rag_with_baidu_search'*

#### run(message, instruction=None, reject=None, clarify=None, highlight=None, friendly=None, cite=None, stream=False, temperature=1e-10, top_p=1e-10)

执行模型推理

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 用户输入的消息对象
  * **instruction** (*Instruction* *,* *optional*) – 用户提供的指令信息，默认为None。如果未提供，则使用默认的指令信息。
  * **reject** (*bool* *,* *optional*) – 是否拒绝执行，默认为None。如果未提供，则使用默认设置。
  * **clarify** (*bool* *,* *optional*) – 是否需要澄清，默认为None。如果未提供，则使用默认设置。
  * **highlight** (*bool* *,* *optional*) – 是否高亮显示，默认为None。如果未提供，则使用默认设置。
  * **friendly** (*bool* *,* *optional*) – 是否以友好的方式回答，默认为None。如果未提供，则使用默认设置。
  * **cite** (*bool* *,* *optional*) – 是否引用原始信息，默认为None。如果未提供，则使用默认设置。
  * **stream** (*bool* *,* *optional*) – 是否以流式方式返回结果，默认为False。
  * **temperature** (*float* *,* *optional*) – 温度参数，用于控制生成文本的多样性，默认为1e-10。
  * **top_p** (*float* *,* *optional*) – 截断概率阈值，用于控制生成文本的多样性，默认为1e-10。
* **返回:**
  推理结果消息对象
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **AppBuilderServerException** – 如果输入消息内容过长（超过72个字符）或推理结果中存在错误，则抛出异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.rag_with_baidu_search.component.RAGWithBaiduSearchArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message), reject: bool, clarify: bool, highlight: bool, friendly: bool, cite: bool, instruction: [Message](appbuilder.core.md#appbuilder.core.message.Message))

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

RAG with Baidusearch提示词配置

#### cite *: bool*

#### clarify *: bool*

#### friendly *: bool*

#### highlight *: bool*

#### instruction *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### message *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'cite': FieldInfo(annotation=bool, required=True, description='控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能', json_schema_extra={'variable_name': 'cite'}), 'clarify': FieldInfo(annotation=bool, required=True, description='控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能', json_schema_extra={'variable_name': 'clarify'}), 'friendly': FieldInfo(annotation=bool, required=True, description='控制大模型友好对提升难过能力的开关，为true即为开启友好度提升功能，为false即为关闭友好度提升功能', json_schema_extra={'variable_name': 'friendly'}), 'highlight': FieldInfo(annotation=bool, required=True, description='控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能', json_schema_extra={'variable_name': 'highlight'}), 'instruction': FieldInfo(annotation=Message, required=True, description='系统人设', json_schema_extra={'variable_name': 'instruction'}), 'message': FieldInfo(annotation=Message, required=True, description="输入用户query，例如'千帆平台都有哪些大模型？'", json_schema_extra={'variable_name': 'message'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'reject': FieldInfo(annotation=bool, required=True, description='控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能', json_schema_extra={'variable_name': 'reject'}), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### reject *: bool*
