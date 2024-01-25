# 文档切分（DocSplitter）

## 简介
文档切分组件（DocSplitter）可以用于对文档进行段落切分。

### 功能介绍
对解析后的文档，支持将文档划分为多个段落，便于后续处理和分析。
目前支持的文档切分类型splitter_type如下：
*  split_by_chunk：按照最大段落大小，对文档进行切分
*  split_by_title：按照文档的title标识层级进行段落切分

### 特色优势
组件对文档分隔段落，准确高效，且有多种可选策略，代码简单可快速上手，是后续大模型使用文档信息的基础。


### 应用场景
对解析后的各类型文档进行分段，用于后续任务的输入。


## 基本用法
---
参考tests目录下的[test_doc_splitter.py](https://github.com/baidubce/app-builder/blob/master/appbuilder/tests/test_doc_splitter.py)，可快速搭建自己的文档切分用例。

以下是DocSplitter快速开始的一个示例。

#### DocSplitter示例:

```python
import os
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter
from appbuilder.core.message import Message

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
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
## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
`splitter_type`(str): 切分器的类型，支持`split_by_chunk`和`split_by_title`两种方式，必选参数

### 调用参数
* `message`(Message): 上游`docparser`的文档解析结果
* 备注: 文档解析时，`parser(msg, return_raw=True)`函数的参数`return_raw`必须为`True`

|参数名称 |参数类型 |是否必须 |描述 | 示例值    |
|--------|--------|--------|----|--------|
|splitter_type |String  |是 |文本提取器类型, 目前支持`split_by_chunk`, `split_by_title`| DocSplitter(splitter_type="split_by_chunk") |


### 响应参数
|参数名称 | 参数类型 |描述 | 示例值            |
|--------|------|----|----------------|
|res_paras  |Message    |返回结果| [{段落1}， {段落2}] |

### 响应示例
```
Message(name=msg, content={'paragraphs': [{'text': '第十节其他重要事项'}]})
```

### 错误码
无


## DocSplitter高级用法

#### 示例:

```python
import os
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter
from appbuilder.core.message import Message

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
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
## 参数说明:

### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 调用参数
* `message`(Message): 上游`docparser`的文档解析结果
* 备注: 文档解析时，`parser(msg, return_raw=True)`函数的参数`return_raw`必须为`True`
*  备注: `splitter_type`为`split_by_title`时，`max_segment_length`, `separators`, `overlap`, `join_symbol`参数不起作用

|参数名称 | 参数类型    | 是否必须 |描述 | 示例值   |
|--------|---------|------|----|-------|
|splitter_type | String  | 是    |文本提取器类型, 目前支持`split_by_chunk`, `split_by_title`| DocSplitter(splitter_type="split_by_chunk") |
|max_segment_length| Integer    | 否    |切分时段落的最大长度|  800   |
|separators| List  | 否    |固定字数时，段落最后截断的分隔符| ["。", "！", "？", ".", "!", "?", "……", "|\n"] |
|overlap| Integer | 否    |分隔的段落间重叠的内容字数| 200     |
|join_symbol| String | 否    |组成固定字数段落时，文本块段落间的链接符| 空字符     |

### 响应参数
|参数名称 | 参数类型 |描述 | 示例值            |
|--------|------|----|----------------|
|res_paras  |Message    |返回结果| [{段落1}， {段落2}] |

### 响应示例
```
Message(name=msg, content={'paragraphs': [{'text': '第十节其他重要事项'}]})
```

## 更新记录和贡献
* 文档分隔 (2023-12)


