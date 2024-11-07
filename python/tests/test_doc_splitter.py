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


import json
import unittest
import os

import appbuilder


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestDocSplitter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_splitter_with_chunk_size(self):
        """
        测试文档分割: 指定最大chunk的大小\结尾分隔符\chunk块重叠的字数等参数,对文档进行分割
        """
        # 1. 文档解析
        current_dir = os.path.dirname(__file__)
        file_name = "test.pdf"
        test_pdf_path = os.path.join(current_dir, file_name)
        msg = appbuilder.Message(test_pdf_path)
        parser = appbuilder.DocParser()
        xmind_output = parser(msg, return_raw=True)

        # 2. 按照参数进行文档分段
        doc_splitter = appbuilder.DocSplitter(splitter_type="split_by_chunk",
                                   separators=["。", "！", "？", ".", "!", "?", "……", "|\n"],
                                   max_segment_length=800,
                                   overlap=200,
                                   join_symbol="")
        doc_splitter_result = doc_splitter(xmind_output)

        appbuilder.logger.info("paragraphs: {}".format(
            json.dumps(doc_splitter_result.content, ensure_ascii=False))
        )

        # 断言解析结果的不为空（根据实际情况调整断言）
        self.assertIsNotNone(doc_splitter_result.content["paragraphs"])

    def test_splitter_with_title_level(self):
        """
         测试文档分割: 按照标题级别进行分割
        """
        config = dict(title="title_splitter.docx")

        # 1. 文档解析
        current_dir = os.path.dirname(__file__)
        test_pdf_path = os.path.join(current_dir, config["title"])
        msg = appbuilder.Message(test_pdf_path)
        parser = appbuilder.DocParser()
        xmind_output = parser(msg, return_raw=True)

        # 2. 按照文档标题层级分段
        doc_splitter = appbuilder.DocSplitter(splitter_type="split_by_title")
        result = doc_splitter(xmind_output)

        appbuilder.logger.info("paragraphs: {}".format(
            json.dumps(result.content["paragraphs"], ensure_ascii=False))
        )

        # 在这里进行断言，确保你的代码达到预期的效果
        self.assertIsInstance(result, appbuilder.Message)
        self.assertTrue("paragraphs" in result.content)

    def test_run_chunk_splitter_with_invalid_input(self):
        # 模拟DocParser的输出结果
        invalid_result = "Invalid Result"
        message = appbuilder.Message(content=invalid_result)

        doc_splitter = appbuilder.DocSplitter(splitter_type="title_level")

        # 运行 DocSplitter，确保它能处理无效输入
        with self.assertRaises(ValueError):
            doc_splitter.run(message)


    def test_run_splitter_with_invalid_input(self):
        config = dict(title="title_splitter.docx")

        # 1. 文档解析
        current_dir = os.path.dirname(__file__)
        test_pdf_path = os.path.join(current_dir, config["title"])
        msg = appbuilder.Message(test_pdf_path)
        parser = appbuilder.DocParser()
        xmind_output = parser(msg, return_raw=False)

        # 2. 按照文档标题层级分段
        doc_splitter = appbuilder.DocSplitter(splitter_type="split_by_title")

        # 在这里进行断言，确保你的代码达到预期的效果
        with self.assertRaises(ValueError):
            doc_splitter.run(xmind_output)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDocSplitter)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main(verbosity=2)
