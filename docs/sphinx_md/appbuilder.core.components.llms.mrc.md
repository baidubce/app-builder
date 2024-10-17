# appbuilder.core.components.llms.mrc package

## Submodules

## appbuilder.core.components.llms.mrc.component module

### *class* appbuilder.core.components.llms.mrc.component.MRC(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

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

#### meta *: [MrcArgs](#appbuilder.core.components.llms.mrc.component.MrcArgs)*

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

### *class* appbuilder.core.components.llms.mrc.component.MrcArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, message: [Message](appbuilder.core.md#appbuilder.core.message.Message), context_list: list, reject: bool, clarify: bool, highlight: bool, friendly: bool, cite: bool)

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

阅读理解问答配置

#### message

Message
用户输入的查询内容，例如’千帆平台都有哪些大模型？’

* **Type:**
  [appbuilder.core.message.Message](appbuilder.core.md#appbuilder.core.message.Message)

#### context_list

list
用户输入的检索片段列表，例如[‘content1’, ‘content2’, ‘content3’,…]，也可以为空，即[]

* **Type:**
  list

#### reject

bool
控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能

* **Type:**
  bool

#### clarify

bool
控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能

* **Type:**
  bool

#### highlight

bool
控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能

* **Type:**
  bool

#### friendly

bool
控制大模型友好对提升难过能力的开关，为true即为开启友好度提升功能，为false即为关闭重点强调功能

* **Type:**
  bool

#### cite

bool
控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能

* **Type:**
  bool

#### cite *: bool*

#### clarify *: bool*

#### context_list *: list*

#### friendly *: bool*

#### highlight *: bool*

#### message *: [Message](appbuilder.core.md#appbuilder.core.message.Message)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'cite': FieldInfo(annotation=bool, required=True, description='控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能', json_schema_extra={'variable_name': 'cite'}), 'clarify': FieldInfo(annotation=bool, required=True, description='控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能', json_schema_extra={'variable_name': 'clarify'}), 'context_list': FieldInfo(annotation=list, required=True, description='用户输入检索片段list，例如[content1, content2, content3,...]，也可以为空, 即[]', json_schema_extra={'variable_name': 'context_list'}), 'friendly': FieldInfo(annotation=bool, required=True, description='控制大模型友好对提升难过能力的开关，为true即为开启友好度提升功能，为false即为关闭友好度提升功能', json_schema_extra={'variable_name': 'friendly'}), 'highlight': FieldInfo(annotation=bool, required=True, description='控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能', json_schema_extra={'variable_name': 'highlight'}), 'message': FieldInfo(annotation=Message, required=True, description="输入用户query，例如'千帆平台都有哪些大模型？'", json_schema_extra={'variable_name': 'query'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'reject': FieldInfo(annotation=bool, required=True, description='控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能', json_schema_extra={'variable_name': 'reject'}), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### reject *: bool*
