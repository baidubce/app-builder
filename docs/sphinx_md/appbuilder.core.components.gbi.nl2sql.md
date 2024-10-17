# appbuilder.core.components.gbi.nl2sql package

## Submodules

## appbuilder.core.components.gbi.nl2sql.component module

GBI nl2sql component.

### *class* appbuilder.core.components.gbi.nl2sql.component.NL2Sql(model_name: str, table_schemas: List[str], knowledge: Dict | None = None, prompt_template: str = '')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

gib nl2sql

#### meta

[`NL2SqlArgs`](#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs) 的别名

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = 60, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[[NL2SqlResult](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.NL2SqlResult)]

执行自然语言转SQL操作。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 

    包含用户问题和会话历史的消息对象。
    - message.content 是一个字典，包含以下关键字：
    > 1. query: 用户问题
    > 2. session: 会话历史列表，参考 SessionRecord
    > 3. column_constraint: 列选约束，参考 ColumnItem 具体定义
  * **timeout** (*float*) – 超时时间，默认为60秒。
  * **retry** (*int*) – 重试次数，默认为0次。
* **返回:**
  转换结果以Message对象形式返回，其中content属性包含NL2SqlResult对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[[NL2SqlResult](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.NL2SqlResult)]

### *class* appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, query: str, session: List[[SessionRecord](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.SessionRecord)] = [], column_constraint: List[[ColumnItem](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.ColumnItem)] = [])

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

nl2sql 的参数

#### query

用户的 query 输入

* **Type:**
  str

#### session

gbi session 的历史 列表

* **Type:**
  List[[appbuilder.core.components.gbi.basic.SessionRecord](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.SessionRecord)]

#### column_constraint

列选的限制条件

* **Type:**
  List[[appbuilder.core.components.gbi.basic.ColumnItem](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.ColumnItem)]

#### column_constraint *: List[[ColumnItem](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.ColumnItem)]*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'column_constraint': FieldInfo(annotation=List[appbuilder.core.components.gbi.basic.ColumnItem], required=False, default=[], description='列选的限制条件'), 'name': FieldInfo(annotation=str, required=False, default=''), 'query': FieldInfo(annotation=str, required=True, description='用户的 query 输入'), 'session': FieldInfo(annotation=List[appbuilder.core.components.gbi.basic.SessionRecord], required=False, default=[], description='gbi session 的历史 列表'), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### query *: str*

#### session *: List[[SessionRecord](appbuilder.core.components.gbi.md#appbuilder.core.components.gbi.basic.SessionRecord)]*
