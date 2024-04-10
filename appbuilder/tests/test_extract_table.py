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

"""test"""
import json
import unittest
import os

from appbuilder.utils.logger_util import logger
from appbuilder import Message, ExtractTableFromDoc, DocParser

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestExtractTableFromDoc(unittest.TestCase):
    """ pass
    """
    @classmethod
    def setUpClass(cls):
        # 获取当前文件所在的目录路径
        current_dir = os.path.dirname(__file__)
        cls.test_pdf_path = os.path.join(current_dir, 'test.pdf')

        # 1.解析文档，并返回原始解析结果
        msg = Message(cls.test_pdf_path)
        parser = DocParser()
        cls.doc = parser(msg, return_raw=True).content.raw


    def test_doc_table_to_markdown_with_default_config(self):
        """ pass
        """
        # 2.文档原始的解析结果，作为输入，解析表格。表格默认最大字符长度：800
        parser = ExtractTableFromDoc()
        result = parser(Message(self.doc), table_max_size=800)
        logger.info("default config Tables: {}".format(
            json.dumps(result.content, ensure_ascii=False))
        )

        self.assertIsNotNone(result.content[0][0]["para"])
    
    def test_doc_table_to_markdown(self):
        """ pass
        """
        # 2.文档原始的解析结果，作为输入，解析表格。表格默认字符长度：800
        table_max_size = 200
        parser = ExtractTableFromDoc()
        result = parser(Message(self.doc), table_max_size=table_max_size, doc_node_num_before_table=10)
        logger.info("Tables: {}".format(
            json.dumps(result.content, ensure_ascii=False))
        )
        for table in result.content:
            for sub in table:
                self.assertLessEqual(len(sub["para"]), table_max_size)

if __name__ == '__main__':
    unittest.main()
    