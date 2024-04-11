# GBI 选表

## 简介
GBI 选表：根据提供的多个 MySql 表名 以及 表名对应的描述信息，通过 query 选择一个或多个最合适的表来回答该 query。
一般的适用场景是，当有数据库有多个表的时候，但是实际只有1个表能回答该 query，那么，通过该能力将该表选择出来，用于后面的 问表 环节。


### 功能介绍
GBI 选表，根据提供的多个 MySql 表名 以及 表名对应的描述信息，通过 query 选择一个或多个最合适的表来回答该 query。
一般的适用场景是，当有数据库有多个表的时候，但是实际只有1个表能回答该 query，那么，通过该能力将该表选择出来，用于后面的 问表 环节。

### 特色优势
可直接通过上传Excel进行数据问答

### 应用场景
1. 营销数据分析
2. 表格问答


## 基本用法
下面是根据提供的表的描述信息以及 query 选择对应的表的示例。


```python
import logging
import os
import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.components.gbi.basic import SessionRecord


# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

# 表的描述信息, key: 表名; value: 是表的描述
table_descriptions = {
    "supper_market_info": "超市营收明细表，包含超市各种信息等",
    "product_sales_info": "产品销售表"
}


# 生成问表对象
select_table = appbuilder.SelectTable(model_name="ERNIE-Bot 4.0", table_descriptions=table_descriptions)
select_table_result_message = select_table(Message({"query": "列出超市中的所有数据"}))

print(f"选的表是: {select_table_result_message.content}")
```

    选的表是: ['supper_market_info']


## 参数说明
### 初始化参数
- model_name: 支持的模型名字 ERNIE-Bot 4.0, ERNIE-Bot, ERNIE-Bot-turbo, ERNIE Speed-AppBuilder
- table_descriptions: 表的描述是个字典，key: 是表的名字, value: 是表的描述，例如:

```
{
    "supper_market_info": "超市营收明细表，包含超市各种信息等",
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
- message: message.content 是用户的问题，包含的key: query, session
  * query: 用户提出的问题
  * session: SessionRecord 列表

#### SessionRecord 初始化参数
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
select_table4 = appbuilder.SelectTable(model_name="ERNIE-Bot 4.0", 
                                          table_descriptions=table_descriptions,
                                          prompt_template=SELECT_TABLE_PROMPT_TEMPLATE)

select_table_result_message4 = select_table4(Message({"query": "列出超市中的所有数据"}))

print(f"选的表是: {select_table_result_message4.content}")
```

    选的表是: ['supper_market_info']

