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
from appbuilder.core.components.gbi.basic import SessionRecord
from appbuilder.core.components.gbi.basic import NL2SqlResult
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
class TestGBISelectTable(unittest.TestCase):

    def setUp(self):
        """
        设置环境变量及必要数据。
        """
        model_name = "ERNIE-Bot 4.0"

        self.select_table_node = \
            appbuilder.SelectTable(model_name=model_name,
                                   table_descriptions={"supper_market_info": "超市营收明细表，包含超市各种信息等",
                                                       "product_sales_info": "产品销售表"})

    def test_run_with_default_param(self):
        """测试 run 方法使用有效参数"""
        query = "列出超市中的所有数据"
        msg = Message({"query": query})
        try:
            result_message = self.select_table_node(message=msg)
            # print(result_message.content)
            self.assertIsNotNone(result_message)
            self.assertEqual(len(result_message.content), 1)
            self.assertEqual(result_message.content[0], "supper_market_info")
        except BaseRPCException:
            pass
        except: 
            raise Exception('单测失败')
            

    def test_run_with_prompt_template(self):
        """测试 run 方法中 prompt template 模版"""
        query = "列出超市中的所有数据"
        msg = Message({"query": query})
        self.select_table_node.prompt_template = PROMPT_TEMPLATE
        try:
            result_message = self.select_table_node(msg)

            self.assertIsNotNone(result_message)
            self.assertEqual(len(result_message.content), 1)
            self.assertTrue(result_message.content[0].startswith("supper_market_info"))
            self.select_table_node.prompt_template = ""
        except BaseRPCException:
            pass
        except: 
            raise Exception('单测失败')

    def test_run_with_session(self):
        """测试 run 方法中 prompt template 模版"""

        session = list()
        session_record = SessionRecord(query="列出商品类别是水果的的利润率",
                                       answer=NL2SqlResult(
                                           llm_result="根据问题分析得到 sql 如下: \n "
                                                      "```sql\nSELECT * FROM `超市营收明细` "
                                                      "WHERE `商品类别` = '水果'\n```",
                                           sql="SELECT * FROM `超市营收明细` WHERE `商品类别` = '水果'"))
        session.append(session_record)

        query = "列出超市中的所有数据"
        msg = Message({"query": query, "session": session})
        try:
            result_message = self.select_table_node(msg)

            self.assertIsNotNone(result_message)
            self.assertEqual(len(result_message.content), 1)
            self.assertEqual(result_message.content[0], "supper_market_info")
        except BaseRPCException:
            pass
        except: 
            raise Exception('单测失败')
        
    def test_st_raise(self):
        with self.assertRaises(ValueError):
            appbuilder.SelectTable(model_name='test',table_descriptions={})

if __name__ == '__main__':
    unittest.main()
