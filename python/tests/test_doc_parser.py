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

import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestDocParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        设置测试类所需的全局变量，包括当前文件所在目录路径和测试PDF文件路径。
        
        Args:
            无
        
        Returns:
            无
        
        """
        # 获取当前文件所在的目录路径
        cls.current_dir = os.path.dirname(__file__)
        cls.test_pdf_path = os.path.join(cls.current_dir, 'test.pdf')

    def test_set_config(self):
        self.doc_parser = appbuilder.DocParser()
        config = appbuilder.ParserConfig()
        config.convert_file_to_pdf = True
        config.return_para_node_tree = False
        config.convert_file_to_pdf = True
        self.doc_parser.set_config(config)
        self.assertEqual(self.doc_parser.config.return_para_node_tree, False)
        self.assertEqual(self.doc_parser.config.convert_file_to_pdf, True)

    def test_make_parse_result(self):
        self.doc_parser = appbuilder.DocParser()
        data = {'para_nodes': {}, 'catalog': {}, 'pdf_data': '', 'file_content': []}
        result = self.doc_parser.make_parse_result(data)
        self.assertEqual(result['para_node_tree'], {})
        self.assertEqual(result['page_contents'], [])
        self.assertEqual(result['pdf_data'], '')

    def test_doc_parser_with_default_config(self):
        # 测试文档解析器使用默认配置
        msg = appbuilder.Message(self.test_pdf_path)
        parser = appbuilder.DocParser()
        result = parser(msg)
        # 断言解析结果的 para_node_tree 不为空（根据实际情况调整断言）
        self.assertIsNotNone(result.content.para_node_tree)

    def test_doc_parser_with_modified_config(self):
        # 测试文档解析器使用修改后的配置
        msg = appbuilder.Message(self.test_pdf_path)
        parser = appbuilder.DocParser()
        # 修改配置参数
        config = parser.config
        config.return_para_node_tree = False
        result = parser(msg)
        self.assertIs(len(result.content.para_node_tree), 0)
        config.convert_file_to_pdf = True
        result = parser(msg)
        # 断言解析结果的 para_node_tree 根据配置更改（根据实际情况调整断言）
        self.assertIsNotNone(result.content.pdf_data)


if __name__ == '__main__':
    unittest.main()
