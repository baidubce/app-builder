# appbuilder.core.components.rag_with_baidu_search package

## Submodules

## appbuilder.core.components.rag_with_baidu_search.component module

### *class* appbuilder.core.components.rag_with_baidu_search.component.RAGWithBaiduSearch(model, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False, instruction: [Message](appbuilder.core.md#appbuilder.core.message.Message) | None = None, reject: bool | None = False, clarify: bool | None = False, highlight: bool | None = False, friendly: bool | None = False, cite: bool | None = False)

基类：`CompletionBaseComponent`

#### meta *: RAGWithBaiduSearchArgs*

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
