# appbuilder.core.components.gbi.nl2sql package

## Submodules

## appbuilder.core.components.gbi.nl2sql.component module

GBI nl2sql component.

### *class* appbuilder.core.components.gbi.nl2sql.component.NL2Sql(model_name: str, table_schemas: List[str], knowledge: Dict | None = None, prompt_template: str = '')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

gib nl2sql

#### meta

`NL2SqlArgs` 的别名

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: float = 60, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[NL2SqlResult]

执行自然语言转SQL操作。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) -- 

    包含用户问题和会话历史的消息对象。
    - message.content 是一个字典，包含以下关键字：
    > 1. query: 用户问题
    > 2. session: 会话历史列表，参考 SessionRecord
    > 3. column_constraint: 列选约束，参考 ColumnItem 具体定义
  * **timeout** (*float*) -- 超时时间，默认为60秒。
  * **retry** (*int*) -- 重试次数，默认为0次。
* **返回:**
  转换结果以Message对象形式返回，其中content属性包含NL2SqlResult对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[NL2SqlResult]
