"""
Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
import os
import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.components.gbi.basic import NL2SqlResult, SessionRecord
from appbuilder.core.components.gbi.basic import ColumnItem
from appbuilder.core._exception import BaseRPCException

SUPER_MARKET_SCHEMA = """
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
"""

PRODUCT_SALES_INFO = """
现有 mysql 表 product_sales_info, 
该表的用途是: 产品收入表
```
CREATE TABLE `product_sales_info` (
  `年` int,
  `月` int,
  `产品名称` varchar,
  `收入` decimal,
  `非交付成本` decimal,
  `含交付毛利` decimal
)
```
"""

PROMPT_TEMPLATE = """
  MySql 表 Schema 如下:
  {schema}
  请根据用户当前问题，联系历史信息，仅编写1个sql，其中 sql 语句需要使用```sql ```这种 markdown 形式给出。
  请参考列选信息：
  {instrument}
  请参考知识:
  {kg}
  当前时间：{date}
  历史信息如下:{history_prompt}
  当前问题："{query}"
  回答：
"""
class TestGBINL2Sql(unittest.TestCase):

    def setUp(self):
        """
        设置环境变量及必要数据。
        """
        model_name = "ERNIE-Bot 4.0"
        table_schemas = [SUPER_MARKET_SCHEMA]
        self.nl2sql_node = appbuilder.NL2Sql(model_name=model_name,
                                             table_schemas=table_schemas)


    def test_run_with_column_constraint(self):
        session = list()
        query = "列出商品类别是水果的的利润率"
        column_constraint = [ColumnItem(ori_value="水果",
                                        column_value="新鲜水果",
                                        column_name="商品类别",
                                        table_name="超市营收明细",
                                        is_like=False)]

        msg = Message({"query": query, "column_constraint": column_constraint,"session": session})
        
        try:
            result_message = self.nl2sql_node(msg)

            self.assertIsNotNone(result_message)
            self.assertTrue(result_message.content.sql != "")
            self.assertTrue(result_message.content.llm_result != "")
            self.assertIn("水果", result_message.content.sql)
            self.nl2sql_node.knowledge = dict()
            self.nl2sql_node.prompt_template = ""
        except BaseRPCException:
            pass
        except: 
            raise Exception('单测失败')
        
    def test_nl2sql_raise(self):
        with self.assertRaises(ValueError):
            node = appbuilder.NL2Sql(model_name='test',table_schemas=['test'])  
        

if __name__ == '__main__':
    unittest.main()
