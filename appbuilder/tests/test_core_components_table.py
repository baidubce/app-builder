# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import unittest

from appbuilder.core.components.table_ocr.component import TableOCR
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.extract_table.component import ExtractTableFromDoc
from appbuilder.core.message import Message

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreCmpsTable(unittest.TestCase):
    def test_table_ocr_component_get_table_markdown(self):
        # test_get_table_markdown
        to=TableOCR()
        table={
            "body":[
                {'row_end': 1, 'col_end': 2,'row_start': 0, 'col_start': 0,'words':'words'},
            ]
        }
        tables=[table]
        md=to.get_table_markdown(tables)
            
    def test_table_ocr_component_tool_eval(self):
        # test_tool_eval 未测试完全
        to=TableOCR()
        url='https://www.baidu.com/'
        res=to.tool_eval(name="test_name", streaming=True, file_names=["test"],file_urls={'test':url})
        with self.assertRaises(AppBuilderServerException):
            next(res)
        res=to.tool_eval(name="test_name", streaming=True, files=["test"],file_urls={'test':url})
        with self.assertRaises(AppBuilderServerException):
            next(res)
            
    def test_extract_table_component_ExtractTableFromDoc(self):
        # test_input_check
        etf=ExtractTableFromDoc()
        message=Message()
        with self.assertRaises(ValueError):
            etf._input_check(message=message,table_max_size=29,doc_node_num_before_table=5)
        with self.assertRaises(ValueError):
            etf._input_check(message=message,table_max_size=31,doc_node_num_before_table=11)
        with self.assertRaises(ValueError):
            etf._input_check(message=message,table_max_size=31,doc_node_num_before_table=5)

        #test_post_process
        resp={
            'result':{
                'mdtables':[[
                    {'para': 'test'},
                    {'para':'描述一表：\n|数据A|数据B表|数据A|数据B表|数据A|数据B表'}
                ]]
            }
        }
        etf.table_max_size=10
        etf._post_process(resp=resp)
        
if __name__ == '__main__':
    unittest.main()