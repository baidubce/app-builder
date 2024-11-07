# appbuilder.core.components.doc_splitter package

## Submodules

## appbuilder.core.components.doc_splitter.doc_splitter module

对文档进行段落切分

### *class* appbuilder.core.components.doc_splitter.doc_splitter.ChunkSplitter(max_segment_length=800, overlap=200, separators=['。', '！', '？', '.', '!', '?', '……', '|\\n'], join_symbol='', \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文档按照块大小切分段落

Examples:

原始文档：
: 贷款资金不得用于从事股本权益性投资，不得用于购买股票、有价证券、期货、理财产品等金融产品。
  不得用于从事房地产经营，不得用于借贷牟取非法收入。不得用于个人或其控制的企业生产经营。
  不得套取现金。不得用于其他违反国家法律、政策规定的领域，不得用于监管机构禁止银行贷款进入的领域。

切分结果：
: [“贷款资金不得用于从事股本权益性投资，不得用于购买股票、有价证券、期货、理财产品等金融产品。不得用于从事房地产经营，
  不得用于借贷牟取非法收入。不得用于个”,
  “不得用于个人或其控制的企业生产经营。不得套取现金。不得用于其他违反国家法律、政策规定的领域，
  不得用于监管机构禁止银行贷款进入的领域。”]

#### meta *: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments)* *= ComponentArguments(name='', tool_desc={'description': 'split data to chunks with max size in doc'})*

#### name *: str* *= 'doc_to_chunk'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

对输入的解析文档结果，按照最大段落块大小、结尾分隔符等，处理为多个段落结果

* **参数:**
  **(****obj** (*message*) – Message): 上游docparser的文档解析结果
* **返回:**
  Message: 文档分隔后的段落结果
* **返回类型:**
  obj
* **抛出:**
  **ValueError** – 如果 message.content 的类型不是 ParseResult，则抛出 ValueError 异常

Examples:

```python
import os
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter, ChunkSplitter
from appbuilder.core.message import Message

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

# 先解析
msg = Message("./test.pdf")
parser = DocParser()
parse_result = parser(msg, return_raw=True)

# 基于parser的结果切分段落
splitter = ChunkSplitter()
res_paras = splitter(parse_result)

# 打印结果
print(res_paras.content)
```

### *class* appbuilder.core.components.doc_splitter.doc_splitter.DocSplitter(splitter_type, max_segment_length=800, overlap=200, separators=['。', '！', '？', '.', '!', '?', '……', '|\\n'], join_symbol='', \*\*kwargs)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文档段落切分组件

#### name

组件名称。

* **Type:**
  str

#### meta

组件元数据。

* **Type:**
  [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

#### meta *: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments)* *= ComponentArguments(name='', tool_desc={'description': 'split data to segments in doc'})*

#### name *: str* *= 'doc_to_parapraphs'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message))

运行函数，根据splitter_type将文档分割成多个部分

* **参数:**
  **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 包含文档内容的消息对象
* **返回:**
  分割后的文档列表
* **返回类型:**
  list
* **抛出:**
  * **ValueError** – 如果message.content不是ParseResult类型，抛出异常
  * **ValueError** – 如果splitter_type为空，抛出异常
  * **ValueError** – 如果ParseResult不包含原始值，抛出异常
  * **ValueError** – 如果splitter_type不是split_by_chunk或split_by_title，抛出异常

### *class* appbuilder.core.components.doc_splitter.doc_splitter.TitleSplitter(meta: [ComponentArguments](appbuilder.core.md#appbuilder.core.component.ComponentArguments) | None = ComponentArguments(name='', tool_desc={}), secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文档按照标题层级切分段落

### 示例

原始文档：
: 一、简介
  叠贷业务是指借款人家庭为满足购房、购车、装修、教育、医疗、旅游、日常消费等符合国家法律法规规定的消费用途。
  二、申请条件
  （一）基本条件
  1、年满18周岁的自然人，具有完全民事行为能力，能提供有效身份证明或居留证明；
  2、有稳定职业和收入，有偿还贷款本息的能力；
  （二）抵押房产所有人的要求
  1、抵押房产的所有人应为借款人本人
  2、抵押房产如有共同所有人，借款人必须为之一，且其他共同所有人必须同意以该房产办理最高额抵押登记，并提供同意抵押的合法有效的书面文件。

切分结果：
: [“一、简介  叠贷业务是指借款人家庭为满足购房、购车、装修、教育、医疗、旅游、日常消费等符合国家法律法规规定的消费用途。”,
  “二、申请条件 （一）基本条件  1、年满18周岁的自然人，具有完全民事行为能力，能提供有效身份证明或居留证明； 2、有稳定职业和收入，
  有偿还贷款本息的能力；”，
  “二、申请条件 （二）抵押房产所有人的要求  1、抵押房产的所有人应为借款人本人。 2、抵押房产如有共同所有人，借款人必须为之一，
  且其他共同所有人必须同意以该房产办理最高额抵押登记，并提供同意抵押的合法有效的书面文件。”】

#### name *: str* *= 'doc_to_title_level'*

#### run(input_message: [Message](appbuilder.core.md#appbuilder.core.message.Message)) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

对输入的解析文档结果，按照各标题层级，处理为多个段落结果

* **参数:**
  **(****obj** (*input_message*) – Message): 上游docparser的文档解析结果
* **返回:**
  Message: 文档分隔后的段落结果
* **返回类型:**
  obj
* **抛出:**
  **ValueError** – 如果message.content的类型不是ParseResult，则抛出异常

Examples:

```python
import os
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter, TitleSplitter
from appbuilder.core.message import Message

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

# 先解析
msg = Message("./title_splitter.docx")
parser = DocParser()
parse_result = parser(msg, return_raw=True)

# 基于parser的结果切分段落
splitter = TitleSplitter()
res_paras = splitter(parse_result)

# 打印结果
print(res_paras.content)
```

#### tool_desc *: Dict[str, Any]* *= {'description': 'split document content by titles'}*
