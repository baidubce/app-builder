# appbuilder.core.components.doc_parser package

## Submodules

## appbuilder.core.components.doc_parser.doc_parser module

文档解析

### *class* appbuilder.core.components.doc_parser.doc_parser.DocParser(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

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

#### config *: [ParserConfig](appbuilder.md#appbuilder.ParserConfig)* *= ParserConfig(convert_file_to_pdf=False, page_filter=None, return_para_node_tree=True, erase_watermark=False)*

#### make_parse_result(response: Dict)

将解析结果的内容转化成ParseResult的结构

#### name *: str* *= 'doc_parser'*

#### run(input_message: [Message](appbuilder.core.md#appbuilder.core.message.Message), return_raw=False) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

对传入的文件进行解析

* **参数:**
  * **input_message** ([*Message*](appbuilder.md#appbuilder.Message) *[**str* *]*) – 输入为文件的路径
  * **return_raw** (*bool* *,* *optional*) – 是否返回云端服务的原始结果。默认为False。
* **返回:**
  文件的解析结果。
* **返回类型:**
  [Message](appbuilder.md#appbuilder.Message)[ParseResult]
* **抛出:**
  * **ValueError** – 如果传入的文件路径不是字符串类型。
  * [**AppBuilderServerException**](appbuilder.md#appbuilder.AppBuilderServerException) – 如果文件解析过程中出现异常，将抛出该异常。

#### set_config(config: [ParserConfig](appbuilder.md#appbuilder.ParserConfig))

设置解析配置

#### tool_desc *: Dict[str, Any]* *= {'description': 'parse document content'}*

## Module contents
