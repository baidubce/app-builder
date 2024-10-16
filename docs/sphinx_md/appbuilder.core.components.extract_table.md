# appbuilder.core.components.extract_table package

## Submodules

## appbuilder.core.components.extract_table.component module

文档表格转换

### *class* appbuilder.core.components.extract_table.component.ExtractTableFromDoc(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

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
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 文档原始解析结果。
  * **table_max_size** (*int*) – 单个表格的长度的最大值(包含上文)，按字符数即len(table_str)统计，默认为800。如果表格超长，则会被拆            分成多个子表格，拆分的最小粒度为表格的行。若单行就超长，则会强制按table_max_size截断。截断时会优先截断上文，尽量保留表格内容。
  * **doc_node_num_before_table** (*int*) – 表格前附加的上文DocParser Node的数量，默认为1。范围：1~10。
* **返回:**
  返回解析后的消息实体对象
  : Message.content (list): 解析出来的文档表格，list(二维)。解析出来的文档表格，如果元素长度为1，则对应原文档中格式化后的                长度不超过\`table_max_size\`的表格；如果元素长度>1，则是对应原文档中一个大表格，该表格被拆分成的多个子表格，以满足设置                大小。输出结果数据结构样例：[[{table1}], [{table2-part1}, {table2-part2}]]
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **ValueError** – 当输入参数不为文档原始解析结果时，或值不合法时，抛出异常。
