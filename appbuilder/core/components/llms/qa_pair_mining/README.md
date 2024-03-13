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

qa_mining = appbuilder.QAPairMining(model="ERNIE Speed-AppBuilder")
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
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
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
import requests

from appbuilder.utils.logger_util import logger
from appbuilder import Message, DocParser, DocSplitter, QAPairMining


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# os.environ["APPBUILDER_TOKEN"] = "..."

# 进行文档内容解析
file_url = "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/test.pdf?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-01-25T12%3A56%3A15Z/-1/host/b54178fea9be115eafa2a8589aeadfcfaeba20d726f434f871741d4a6cb0c70d"
file_data = requests.get(file_url).content
file_path = "./test.pdf"  # 待解析的文件路径
with open(file_path, "wb") as f:
    f.write(file_data)

# 解析文档
msg = Message(file_path)
parser = DocParser()
parse_result = parser.run(msg, return_raw=True)

# 对文档进行分段落，split_by_chunk需要return_raw=True
splitter = DocSplitter(
    splitter_type="split_by_chunk", overlap=0)
split_result = splitter(parse_result)

# 每个段落抽取问答对，并返回结果
for doc_segment in split_result.content["paragraphs"]:
    qa_mining = QAPairMining(model="ERNIE Speed-AppBuilder")
    text = doc_segment.get("text", "")
    if text == "":
        logger.error("Text is null. break")
        break
    logger.info("Input: \n{}".format(text))
    answer = qa_mining(Message(text))
    logger.info("Output: \n{}".format(answer.content))
    break # 样例代码只跑1个段落
```

## 更新记录和贡献
* 问答对挖掘能力 (2023-12)
