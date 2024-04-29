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

import unittest
import os
import appbuilder
import requests
from parameterized import parameterized, param
import appbuilder
from appbuilder.core.message import Message

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

png_path = "./data/qa_doc_parser_extract_table_from_doc.png"

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestDocParserExtractTableFromDoc(unittest.TestCase):
    @parameterized.expand([
        param(png_path, True),
    ])
    def test_normal_case(self, message, return_raw):
        """
        正常用例
        """
        builder = appbuilder.DocParser()
        # 测试文档解析器使用默认配置，xxx为待解析的文档路径。
        msg = Message(message)
        # ExtractTableFromDoc输入为文档原始解析结果，此处需要带上原始结果，return_raw=True.
        doc = builder(msg, return_raw=return_raw).content.raw
        # 抽取文档中的表格
        ExtractTableBuilder = appbuilder.ExtractTableFromDoc()
        res = ExtractTableBuilder.run(Message(doc), table_max_size=1000)
        assert len(res.content) > 0, "未抽取到表格"
        assert len(res.content[0]) > 0, "未抽取到表格"

    @parameterized.expand([
        # timeout为0
        param(123, True, None, png_path, "ValueError", "file_path", "file_path should be str type"),
    ])
    def test_abnormal_case(self, message, return_raw, single_table_size, file_name, err_type, err_param, err_msg):
        """
        异常用例
        """
        try:
            builder = appbuilder.DocParser()
            # 测试文档解析器使用默认配置，xxx为待解析的文档路径。
            msg = Message(message)
            # ExtractTableFromDoc输入为文档原始解析结果，此处需要带上原始结果，return_raw=True.
            doc = builder(msg, return_raw=return_raw).content.raw
            # 抽取文档中的表格
            ExtractTableBuilder = appbuilder.ExtractTableFromDoc(single_table_size=single_table_size,
                                                                 file_name=file_name)
            res = ExtractTableBuilder.run(Message(doc))
            log.info(res)
            assert False, "未捕获到错误信息"
        except Exception as e:
            self.assertIsInstance(e, eval(err_type), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, err_type))
            self.assertIn(err_param, str(e), "捕获的异常参数类型不正确, 实际:{}, 预期:{}".format(e, err_param))
            self.assertIn(err_msg, str(e), "捕获的异常消息不正确, 实际:{}, 预期:{}".format(e, err_msg))

    
if __name__ == '__main__':
    unittest.main()