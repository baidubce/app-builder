# appbuilder.core.components.gbi.select_table package

## Submodules

## appbuilder.core.components.gbi.select_table.component module

GBI nl2sql component.

### *class* appbuilder.core.components.gbi.select_table.component.SelectTable(model_name: str, table_descriptions: Dict[str, str], prompt_template: str = '')

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

gbi 选表

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), timeout: int = 60, retry: int = 0) → [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]]

执行查询操作，返回识别的表名列表。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 

    包含查询信息的消息对象。
    - message.content 字典包含以下 key:
    > 1. query (str): 用户的问题输入。
    > 2. session (list, optional): 对话历史，默认为空列表。
  * **timeout** (*int* *,* *optional*) – 超时时间，默认为 60 秒。
  * **retry** (*int* *,* *optional*) – 重试次数，默认为 0。
* **返回:**
  包含识别出的表名列表的 Message 对象。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)[List[str]]
* **抛出:**
  **ValueError** – 如果输入的 message.content 不符合期望的格式，将抛出 ValueError 异常。
