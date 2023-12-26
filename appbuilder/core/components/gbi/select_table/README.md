# GBI 选表

## 简介
GBI 选表，根据提供的表的描述信息以及 query 选择对应的表.

## 基本用法

### 快速开启



```python
import logging
import os
import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.components.gbi.basic import GBISessionRecord

#  设置环境变量
os.environ["APPBUILDER_TOKEN"] = "***"

# 表的描述信息
table_descriptions = {
    "超市营收明细表": "超市营收明细表，包含超市各种信息等",
    "product_sales_info": "产品销售表"
}


# 生成问表对象
select_table = appbuilder.GBISelectTable(model_name="ERNIE-Bot 4.0", table_descriptions=table_descriptions)
query = "列出超市中的所有数据"
msg = Message(query)
session = list()
select_table_result_message = select_table(message=msg, session=session)
print(f"选的表是: {select_table_result_message.content}")
```

      选的表是: ['超市营收明细表']


## 参数说明
### 初始化参数
- model_name: 支持的模型名字 ERNIE-Bot 4.0, ERNIE-Bot-8K, ERNIE-Bot, ERNIE-Bot-turbo, EB-turbo-AppBuilder
- table_descriptions: 表的描述是个字典，key: 是表的名字, value: 是表的描述，例如:

```
{
    "超市营收明细表": "超市营收明细表，包含超市各种信息等",
    "product_sales_info": "产品销售表"
}
```
- prompt_template: prompt 模版, 必须包含如下:
  1. {num} - 表的数量， 注意 {num} 有两个地方出现
  2. {table_desc} - 表的描述
  3. {query} - query
  参考下面的示例:

```
你是一个专业的业务人员，下面有{num}张表，具体表名如下:
{table_desc}
请根据问题帮我选择上述1-{num}种的其中相关表并返回，可以为多表，也可以为单表,
返回多张表请用“,”隔开
返回格式请参考如下示例：
问题:有多少个审核通过的投运单？
回答: ```DWD_MAT_OPERATION```
请严格参考示例只不要返回无关内容，直接给出最终答案后面的内容，分析步骤不要输出
问题:{query}
回答:
```
     
### 调用参数
- message: message.content 是用户的问题，也就是 query
- session: GBISessionRecord 列表

#### GBISessionRecord 初始化参数
- query: 用户的问题
- answer: gbi_nl2sql 返回的结果 NL2SqlResult
  
### 返回值
识别的表名的列表例如:
`["table_name"]`

## 调整 prompt 模版
有时候，我们希望定义自己的prompt, 选表支持 prompt 模版的定制化，但是必须遵循对应的 prompt 模版的格式。

### 选表 prompt 调整
选表的 prompt template, 必须包含 
1. {num} - 表的数量， 注意 {num} 有两个地方出现
2. {table_desc} - 表的描述
3. {query} - query, 参考下面的示例:


```python
SELECT_TABLE_PROMPT_TEMPLATE = """
你是一个专业的业务人员，下面有{num}张表，具体表名如下:
{table_desc}
请根据问题帮我选择上述1-{num}种的其中相关表并返回，可以为多表，也可以为单表,
返回多张表请用“,”隔开
返回格式请参考如下示例：
问题:有多少个审核通过的投运单？
回答: ```DWD_MAT_OPERATION```
请严格参考示例只不要返回无关内容，直接给出最终答案后面的内容，分析步骤不要输出
问题:{query}
回答:
"""
```


```python
select_table4 = appbuilder.GBISelectTable(model_name="ERNIE-Bot 4.0", 
                                          table_descriptions=table_descriptions,
                                          prompt_template=SELECT_TABLE_PROMPT_TEMPLATE)
query4 = "列出超市中的所有数据"
msg4 = Message(query4)
select_table_result_message4 = select_table4(message=msg4, session=list())
print(f"选的表是: {select_table_result_message4.content}")
```

    选的表是: ['超市营收明细表']

