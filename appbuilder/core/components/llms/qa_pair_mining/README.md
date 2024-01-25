# 问答对挖掘（QAPairMining）

## 简介
问答对挖掘（QAPairMining）可以基于输入文本内容，快速生成多个问题及对应答案，极大提高信息提炼的效率和准确性。广泛用于在线客服、智能问答等领域。

### 功能介绍
基于输入文本内容，快速生成多个问题及对应答案；可与文档解析、分段联用，快速生成文档的问答对。

### 特色优势
问答对挖掘组件快速基于输入文本生成的问题和答案，准确率高；可快速依据文档生成FAQ，减少人工成本。

### 适用场景
适用于在线客服、智能问答等场景

## 基本用法

### 快速开始

```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

qa_mining = appbuilder.QAPairMining(model="eb-turbo-appbuilder")
# 输入文本（对此文本挖掘问答对）
msg = '2017年，工商银行根据外部宏观环境变化，及时调整业务策略，优化资产负债结构，' + \
    '保持存贷款业务协调发展，提升资产负债配置效率。' + \
    '2018年3月末，工商银行总资产264,937.81亿元，比上年末增加4,067.38亿元.'
msg = appbuilder.Message(msg)
answer = qa_mining(msg)

print(">>> Output: {}".format(answer.content))
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
无

### 调用参数

|参数名称 |参数类型 |是否必须 |描述 |示例值|
|--------|--------|--------|----|------|
| message | String |是 |输入消息，用于模型的主要输入内容。这是一个必需的参数。| `Message("2017年，工商银行根据...")` |
| stream |bool|否 |指定是否以流式形式返回响应。默认为 False。| False |
| temperature |float|否 |模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。 | 1e-10 |

### 响应参数
|参数名称 |参数类型 |描述 |示例值|
|--------|--------|----|------|
| result | String | 输出消息，包含模型运行后的输出内容。| 见响应示例 |

### 响应示例
```text
问题：2017年，工商银行是如何应对外部宏观环境变化的？
答案：工商银行根据外部宏观环境变化，及时调整业务策略，优化资产负债结构，保持存贷款业务协调发展，提升资产负债配置效率。

问题：2018年3月末，工商银行总资产是多少？
答案：264,937.81亿元。
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法

基于一篇文档，快速生成多个问题及对应答案，极大提高信息提炼的效率和准确性。
主要流程如下：

1. 读取本地文档，文档解析分段，获取段落；
2. 段落作为问答对挖掘的输入，挖掘问答对。 

### 代码样例
```python
import os

from appbuilder.utils.logger_util import logger
from appbuilder import Message, DocParser, DocSplitter, QAPairMining

# 准备一个文档，本地路径
file_path = "xxx.pdf"

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "...."

# 解析文档
msg = Message(file_path)
parser = DocParser()
parse_result = parser.run(msg)

# 对文档进行分段落
splitter = DocSplitter()
split_result = splitter(parse_result)

# 每个段落抽取问答对，并返回结果
for doc_segment in split_result.content:
    qa_mining = QAPairMining()
    logger.info("Input: {}".format(doc_segment.content))
    answer = qa_mining(doc_segment)
    logger.info("Output: {}".format(answer.content))
    break # debug，只跑1个段落
```

## 更新记录和贡献
* 问答对挖掘能力 (2023-12)
