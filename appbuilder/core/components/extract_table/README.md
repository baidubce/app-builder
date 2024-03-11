# 表格抽取组件（ExtractTableFromDoc）

## 简介
表格抽取组件（ExtractTableFromDoc）是用于文档表格处理的组件，从文档中抽取表格。支持对文档表格大小进行限制，限制后自动进行拆分、跨页合并等处理；支持合并表格上文，提取的表格为Markdown格式。

### 功能介绍
从文档中抽取表格。支持对文档表格大小进行限制，限制后自动进行拆分、跨页合并等处理；支持合并表格上文，设置表格上文数量，提取的表格为Markdown格式。

### 特色优势
组件抽取表格，准确高效，代码简单可快速上手；且不依赖本地计算资源。

### 适用场景
文档表格解析与处理，用于后续任务的输入。

## 基本用法
下面是一个基本用法的样例

```python
import os
import json
import requests

from appbuilder.utils.logger_util import logger
from appbuilder import Message, ExtractTableFromDoc, DocParser


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."


# 进行文档内容解析
file_url = "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/test.pdf?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-01-25T12%3A56%3A15Z/-1/host/b54178fea9be115eafa2a8589aeadfcfaeba20d726f434f871741d4a6cb0c70d"
file_data = requests.get(file_url).content
file_path = "./test.pdf"  # 待解析的文件路径
with open(file_path, "wb") as f:
    f.write(file_data)

msg = Message(file_path)

parser = DocParser()
# ExtractTableFromDoc输入为文档原始解析结果，此处需要带上原始结果，return_raw=True.
doc = parser(msg, return_raw=True).content.raw

# 抽取文档中的表格
parser = ExtractTableFromDoc()
result = parser.run(Message(doc))

logger.info("Tables: {}".format(
    json.dumps(result.content, ensure_ascii=False))
)
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[SDK使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
无

### 调用参数

|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
|message | Dict  |是 | 输入的消息，用于模型的主要输入内容，必须为Docparser解析后的结果raw，需要设置return_raw=True。这是一个必需的参数。| `Message(parser(msg, return_raw=True).content.raw)` |
|table_max_size |int  |否 |单个表格的长度的最大值(包含上文)，按字符数即len(table_str)统计，默认为800。如果表格超长，则会被拆分成多个子表格，拆分的最小粒度为表格的行。若单行就超长，则会强制按table_max_size截断。截断时会优先截断上文，尽量保留表格内容。 | 800 |
|doc_node_num_before_table |int  |否 |表格前附加的上文DocParser Node的数量，默认为1。范围：1~10。 | 1 |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
| - | List  | 解析出来的文档表格，如果元素长度为1，则对应原文档中格式化后的长度不超过`table_max_size`的表格；如果元素长度>1，则是对应原文档中一个大表格，该表格被拆分成的多个子表格，以满足设置大小。 | 见响应示例 |

### 错误码
|错误码|描述|
|------|---|


### 响应示例
```json
[[{"para": "table1"}], [{"para": "table2-part1"}, {"para": "table2-part2"}]]
```

## 更新记录和贡献
* 表格抽取能力 (2023-12)