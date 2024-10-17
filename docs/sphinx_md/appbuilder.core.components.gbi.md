# appbuilder.core.components.gbi package

## Subpackages

* [appbuilder.core.components.gbi.nl2sql package](appbuilder.core.components.gbi.nl2sql.md)
  * [Submodules](appbuilder.core.components.gbi.nl2sql.md#submodules)
  * [appbuilder.core.components.gbi.nl2sql.component module](appbuilder.core.components.gbi.nl2sql.md#module-appbuilder.core.components.gbi.nl2sql.component)
    * [`NL2Sql`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2Sql)
      * [`NL2Sql.meta`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2Sql.meta)
      * [`NL2Sql.run()`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2Sql.run)
    * [`NL2SqlArgs`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs)
      * [`NL2SqlArgs.query`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs.query)
      * [`NL2SqlArgs.session`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs.session)
      * [`NL2SqlArgs.column_constraint`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs.column_constraint)
      * [`NL2SqlArgs.column_constraint`](appbuilder.core.components.gbi.nl2sql.md#id0)
      * [`NL2SqlArgs.model_computed_fields`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs.model_computed_fields)
      * [`NL2SqlArgs.model_config`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs.model_config)
      * [`NL2SqlArgs.model_fields`](appbuilder.core.components.gbi.nl2sql.md#appbuilder.core.components.gbi.nl2sql.component.NL2SqlArgs.model_fields)
      * [`NL2SqlArgs.query`](appbuilder.core.components.gbi.nl2sql.md#id1)
      * [`NL2SqlArgs.session`](appbuilder.core.components.gbi.nl2sql.md#id2)
* [appbuilder.core.components.gbi.select_table package](appbuilder.core.components.gbi.select_table.md)
  * [Submodules](appbuilder.core.components.gbi.select_table.md#submodules)
  * [appbuilder.core.components.gbi.select_table.component module](appbuilder.core.components.gbi.select_table.md#module-appbuilder.core.components.gbi.select_table.component)
    * [`SelectTable`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTable)
      * [`SelectTable.run()`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTable.run)
    * [`SelectTableArgs`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTableArgs)
      * [`SelectTableArgs.model_computed_fields`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTableArgs.model_computed_fields)
      * [`SelectTableArgs.model_config`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTableArgs.model_config)
      * [`SelectTableArgs.model_fields`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTableArgs.model_fields)
      * [`SelectTableArgs.query`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTableArgs.query)
      * [`SelectTableArgs.session`](appbuilder.core.components.gbi.select_table.md#appbuilder.core.components.gbi.select_table.component.SelectTableArgs.session)

## Submodules

## appbuilder.core.components.gbi.basic module

GBI nl2sql component.

### *class* appbuilder.core.components.gbi.basic.ColumnItem(\*, ori_value: str, column_name: str, column_value: str, table_name: str, is_like: bool = False)

基类：`BaseModel`

列信息

#### column_name *: str*

#### column_value *: str*

#### is_like *: bool*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'column_name': FieldInfo(annotation=str, required=True, description='对应数据库中的列名称, 比如: city'), 'column_value': FieldInfo(annotation=str, required=True, description='对应数据库中的列值, 比如: 北京市'), 'is_like': FieldInfo(annotation=bool, required=False, default=False, description='与 ori_value 的匹配是包含 还是 等于，包含: True; 等于: False'), 'ori_value': FieldInfo(annotation=str, required=True, description='query 中的 词语, 比如: 北京去年收入,  分词后: 北京, 去年, 收入, ori_value 是分词中某一个，比如: ori_value = 北京'), 'table_name': FieldInfo(annotation=str, required=True, description='该列所在表的名字')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### ori_value *: str*

#### table_name *: str*

### *class* appbuilder.core.components.gbi.basic.NL2SqlResult(\*, llm_result: str, sql: str)

基类：`BaseModel`

gbi_nl2sql 返回的结果

#### llm_result *: str*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'llm_result': FieldInfo(annotation=str, required=True, description='大模型返回的结果'), 'sql': FieldInfo(annotation=str, required=True, description='从大模型中抽取的 sql 语句')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### sql *: str*

### *class* appbuilder.core.components.gbi.basic.SessionRecord(\*, query: str, answer: [NL2SqlResult](#appbuilder.core.components.gbi.basic.NL2SqlResult))

基类：`BaseModel`

gbi session record

#### answer *: [NL2SqlResult](#appbuilder.core.components.gbi.basic.NL2SqlResult)*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'answer': FieldInfo(annotation=NL2SqlResult, required=True, description='nl2sql 返回的结果'), 'query': FieldInfo(annotation=str, required=True, description='用户的问题')}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### query *: str*
