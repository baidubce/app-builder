# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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
import unittest
import os 

from appbuilder.core.components.rag_with_baidu_search.component import RAGWithBaiduSearch
from appbuilder.core.message import Message 
from appbuilder.core._exception import *

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestRagWithBaiduSearchComponent(unittest.TestCase):
    def test_rag_with_baidu_search_component_RAGWithBaiduSearch(self):
        rwbs=RAGWithBaiduSearch(model='ERNIE-Bot 4.0')
        
        # test_get_search_input
        text='text'
        res_text=rwbs._get_search_input(text)
        self.assertEqual(res_text, 'text')
        text='UTF-8是一种变长字节表示的Unicode字符集编码方式，它可以使用1到4个字节来表示一个字符。'
        res_text=rwbs._get_search_input(text)
        self.assertEqual(res_text, 'UTF-8是一种变长字节表示的Unicode字符集编码方式，它可')
        
        # test run
        message=Message()
        message.content='message'
        res_response=rwbs.run(message=message)
        assert message.content.startswith('message')
        
        message.content="""
        appbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilder
        appbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilder
        """
        with self.assertRaises(AppBuilderServerException):
            rwbs.run(message=message)
            
if __name__ == '__main__':
    unittest.main()