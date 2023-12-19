# 文档切分（DocSplitter）

## 简介
文档切分组件（DocSplitter）可以用于对文档进行段落切分。支持将文档划分为多个段落，便于后续处理和分析。
目前支持的文档切分类型splitter_type如下：
*  split_by_chunk：按照最大段落大小，对文档进行切分
*  split_by_title：按照文档的title标识层级进行段落切分

基本用法
---
参考tests目录下的[test_doc_splitter.py](../../../tests/test_doc_splitter.py)，可快速搭建自己的文档切分用例。

以下是DocSplitter快速开始的一个示例。

#### DocSplitter示例:

```python
import os
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter
from appbuilder.core.message import Message


os.environ["APPBUILDER_TOKEN"] = "..."

# 先解析
msg = Message("./test.pdf")
parser = DocParser()
parse_result = parser(msg, return_raw=True)

# 基于parser的结果切分段落
splitter = DocSplitter(splitter_type="split_by_chunk")
res_paras = splitter(parse_result)

# 打印结果
print(res_paras.content)
```
### 参数说明
#### 初始化参数
`splitter_type`(str): 切分器的类型，支持`split_by_chunk`和`split_by_title`两种方式，必选参数

#### 调用参数
* `message`(Message): 上游`docparser`的文档解析结果
* 备注: 文档解析时，`parser(msg, return_raw=True)`函数的参数`return_raw`必须为`True`
#### 返回值
* `Message`: 文档分隔后的段落结果

### DocSplitter高级用法

#### 示例:

```python
import os
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter
from appbuilder.core.message import Message

os.environ["APPBUILDER_TOKEN"] = "..."

# 先解析
msg = Message("./test.pdf")
parser = DocParser()
parse_result = parser(msg, return_raw=True)

# 基于parser的结果切分段落
doc_splitter = DocSplitter(splitter_type="split_by_chunk",
                           separators=["。", "！", "？", ".", "!", "?", "……", "|\n"],
                           max_segment_length=800,
                           overlap=0)
res_paras = doc_splitter(parse_result)

# 打印结果
print(res_paras.content)
```
#### 参数说明:
*  `splitter_type`：文本提取器类型, 目前支持`split_by_chunk`, `split_by_title`，必选参数
*  `max_segment_length`：切分时段落的最大长度，默认为800，可选参数
*  `separators`：固定字数时，段落最后截断的分隔符，默认为["。", "！", "？", ".", "!", "?", "……", "|\n"]，可选参数
*  `overlap`：分隔的段落间重叠的内容字数，默认为200，可选参数
*  `join_symbol`：组成固定字数段落时，文本块段落间的链接符，默认为空字符，可选参数
*  备注: `splitter_type`为`split_by_title`时，`max_segment_length`, `separators`, `overlap`, `join_symbol`参数不起作用

#### 调用参数
* `message`(Message): 上游`docparser`的文档解析结果
* 备注: 文档解析时，`parser(msg, return_raw=True)`函数的参数`return_raw`必须为`True`
#### 返回值
* `Message`: 文档分隔后的段落结果

## 示例和案例研究

目前暂无具体的实际应用案例。

## API文档

暂无

## 更新记录和贡献

- 初始版本发布。
- 如您希望为会话小结组件贡献代码或反馈，请参考 [贡献指南](#)。