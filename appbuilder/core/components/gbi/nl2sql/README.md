# GBI 问表

## 简介
GBI 问表，根据提供的 mysql 表的 schema 信息，生成对应问题的 sql 语句。

### 功能介绍
GBI 问表，根据提供的 mysql 表的 schema 信息，生成对应问题的 sql 语句。

### 特色优势
直接生成 sql 语句，无需人工编写。

### 应用场景
1. 业务人员需要根据问题生成 sql 语句，但是不熟悉 sql 语法。
2. 业务人员需要根据问题生成 sql 语句，但是不熟悉表的名称。


## 基本用法
这里是一个示例，展示如何基于 mysql 表的 schema, 根据问题生成 sql 语句。


```python
import logging
import os
import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.components.gbi.basic import SessionRecord

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

SUPER_MARKET_SCHEMA = """
CREATE TABLE `supper_market_info` (
  `订单编号` varchar(32) DEFAULT NULL,
  `订单日期` date DEFAULT NULL,
  `邮寄方式` varchar(32) DEFAULT NULL,
  `地区` varchar(32) DEFAULT NULL,
  `省份` varchar(32) DEFAULT NULL,
  `客户类型` varchar(32) DEFAULT NULL,
  `客户名称` varchar(32) DEFAULT NULL,
  `商品类别` varchar(32) DEFAULT NULL,
  `制造商` varchar(32) DEFAULT NULL,
  `商品名称` varchar(32) DEFAULT NULL,
  `数量` int(11) DEFAULT NULL,
  `销售额` int(11) DEFAULT NULL,
  `利润` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""

table_schemas = [SUPER_MARKET_SCHEMA]
gbi_nl2sql = appbuilder.NL2Sql(model_name="ERNIE-Bot 4.0", table_schemas=table_schemas)
query = "列出超市中的所有数据"
nl2sql_result_message = gbi_nl2sql(Message({"query": query}))

print(f"sql: {nl2sql_result_message.content.sql}")
print(f"llm result: {nl2sql_result_message.content.llm_result}")
```


## 参数说明

### 初始化参数
- model_name:  支持的模型名字 ERNIE-Bot 4.0, ERNIE-Bot, ERNIE-Bot-turbo, ERNIE Speed-AppBuilder
- table_schemas: 表的 schema，例如:
  
```
CREATE TABLE `supper_market_info` (
  `订单编号` varchar(32) DEFAULT NULL,
  `订单日期` date DEFAULT NULL,
  `邮寄方式` varchar(32) DEFAULT NULL,
  `地区` varchar(32) DEFAULT NULL,
  `省份` varchar(32) DEFAULT NULL,
  `客户类型` varchar(32) DEFAULT NULL,
  `客户名称` varchar(32) DEFAULT NULL,
  `商品类别` varchar(32) DEFAULT NULL,
  `制造商` varchar(32) DEFAULT NULL,
  `商品名称` varchar(32) DEFAULT NULL,
  `数量` int(11) DEFAULT NULL,
  `销售额` int(11) DEFAULT NULL,
  `利润` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

- knowledge: 用于提供一些知识, 比如 {"毛利率": "(销售收入 - 销售成本) / 销售收入"}
- prompt_template: prompt 模版, 必须包含的格式如下:
                  ***你的描述
                  {schema}
                  ***你的描述
                  {column_instrument}
                  ***你的描述
                  {kg}
                  ***你的描述
                  当前时间：{date}
                  ***你的描述
                  {history_instrument}
                  ***你的描述
                  当前问题：{query}
                  回答：

### 调用参数
- message: message.content 是 字典，包含: query, session, column_constraint 三个key
  * query: 用户的问题
  * session: gbi session 的历史 列表, 参考 SessionRecord
  * column_constraint: 列选约束 参考 ColumnItem 具体定义

#### SessionRecord 初始化参数
- query: 用户的问题
- answer: gbi_nl2sql 返回的结果 NL2SqlResult

#### ColumnItem 初始化参数如下
- ori_value: query 中的 词语, 比如: "北京去年收入",  分词后: "北京, 去年, 收入", ori_value 是分词中某一个，比如: ori_value = "北京"
- column_name: 对应数据库中的列名称, city
- column_value: 对应数据库中的列值, 北京市
- table_name: 该列所属的表名称
- is_like: 与 ori_value 的匹配是包含 还是 等于，包含: True; 等于: False

### 返回值
- NL2SqlResult 的 message

#### NL2SqlResult 初始化参数如下
- llm_result: 大模型返回的结果
- sql: 从 llm_result 中抽取的 sql 语句

## 高级用法
### 设置 session


```python
session = list()
session.append(SessionRecord(query=query, answer=nl2sql_result_message.content))
```

再次问表


```python
nl2sql_result_message2 = gbi_nl2sql(Message({"query": "查看商品类别是水果的所有数据",
                                             "session": session}))
print(f"sql: {nl2sql_result_message2.content.sql}")
print(f"llm result: {nl2sql_result_message2.content.llm_result}")
```

    sql: 
    SELECT * FROM supper_market_info WHERE 商品类别 = '水果';
    -----------------
    llm result: ```sql
    SELECT * FROM supper_market_info WHERE 商品类别 = '水果';
    ```


### 增加列选优化
实际上数据中 "商品类别" 存储的是 "新鲜水果", 那么就可以通过列选的限制来优化 sql.


```python
from appbuilder.core.components.gbi.basic import ColumnItem

column_constraint = [ColumnItem(ori_value="水果", 
                               column_name="商品类别", 
                               column_value="新鲜水果", 
                               table_name="超市营收明细表", 
                               is_like=False)]
nl2sql_result_message2 = gbi_nl2sql(Message({"query": "查看商品类别是水果的所有数据",
                                             "column_constraint": column_constraint}))

print(f"sql: {nl2sql_result_message2.content.sql}")
print(f"llm result: {nl2sql_result_message2.content.llm_result}")
```

    sql: 
    SELECT * FROM supper_market_info WHERE 商品类别='新鲜水果'
    -----------------
    llm result: ```sql
    SELECT * FROM supper_market_info WHERE 商品类别='新鲜水果'
    ```


从上面我们看到，商品类别不在是 "水果" 而是 修订为 "新鲜水果"

### 增加知识优化
当计算某些特殊知识的时候，大模型是不知道的，所以需要告诉大模型具体的知识，比如:
利润率的计算方式: 利润/销售额
可以将该知识注入。具体示例如下:


```python
# 注入知识
gbi_nl2sql.knowledge["利润率"] = "计算方式: 利润/销售额"
```


```python
query3 = "列出商品类别是日用品的利润率"
msg3 = Message(query3)

nl2sql_result_message3 = gbi_nl2sql(Message({"query": "列出商品类别是日用品的利润率"}))
print(f"sql: {nl2sql_result_message3.content.sql}")
print(f"llm result: {nl2sql_result_message3.content.llm_result}")
```

    sql: 
    SELECT 商品类别, SUM(利润)/SUM(销售额) AS 利润率
    FROM supper_market_info
    WHERE 商品类别 = '日用品'
    GROUP BY 商品类别
    -----------------
    llm result: ```sql
    SELECT 商品类别, SUM(利润)/SUM(销售额) AS 利润率
    FROM supper_market_info
    WHERE 商品类别 = '日用品'
    GROUP BY 商品类别
    ```


## 调整 prompt 模版
有时候，我们希望定义自己的prompt, 但是必须遵循对应的 prompt 模版的格式。


问表的 prompt template 必须包含:
1. {schema} - 表的 schema 信息
2. {instrument} - 列选限制的信息
3. {kg} - 知识
4. {date} - 时间
5. {history_prompt} - 历史
6. {query} - 当前问题

参考下面的示例


```python
NL2SQL_PROMPT_TEMPLATE = """
  MySql 表 Schema 如下:
  {schema}
  请根据用户当前问题，联系历史信息，仅编写1个sql，其中 sql 语句需要使用```sql ```这种 markdown 形式给出。
  请参考列选信息：
  {instrument}
  请参考知识:
  {kg}
  当前时间：{date}
  历史信息如下:
  {history_prompt}
  当前问题："{query}"
  回答：
"""
```


```python
gbi_nl2sql5 = appbuilder.NL2Sql(model_name="ERNIE-Bot 4.0", table_schemas=table_schemas, prompt_template=NL2SQL_PROMPT_TEMPLATE)
nl2sql_result_message5 = gbi_nl2sql5(Message({"query": "查看商品类别是水果的所有数据"}))

print(f"sql: {nl2sql_result_message5.content.sql}")
print(f"llm result: {nl2sql_result_message5.content.llm_result}")
```

    sql: 
    SELECT * FROM supper_market_info WHERE 商品类别 = '水果'
    -----------------
    llm result: ```sql
    SELECT * FROM supper_market_info WHERE 商品类别 = '水果'
    ```

