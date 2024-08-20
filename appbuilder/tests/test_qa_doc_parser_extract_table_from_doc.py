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
from appbuilder.core.message import Message

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestDocParserExtractTableFromDoc(unittest.TestCase):

    def test_run(self):
        test_dir = os.path.dirname(__file__)
        image_path = os.path.join(test_dir, "data/qa_doc_parser_extract_table_from_doc.png")
        return_raw = True

        builder = appbuilder.DocParser()
        msg = Message(image_path)
        doc = builder(msg, return_raw=return_raw).content.raw

        ExtractTableBuilder = appbuilder.ExtractTableFromDoc()
        out = ExtractTableBuilder.run(Message(doc), table_max_size=1000)

        self.assertIn("客户名称", str(out))
        self.assertIn("有限责任公司", str(out))


if __name__ == '__main__':
    unittest.main()
