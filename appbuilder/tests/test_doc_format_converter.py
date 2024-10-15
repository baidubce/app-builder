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
class TestDocFormatConverter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    @classmethod
    def test_doc_format_url(cls):
        image_url = "https://ai-cape-strategy-data.bj.bcebos.com/document-restructure/1EF33F9307451C9413D5D1160.jpg"
        doc_format_converter = appbuilder.DocFormatConverter()
        resp = doc_format_converter(appbuilder.Message({"file_path": image_url}))

        assert "word_url" in resp.content

if __name__ == '__main__':
    unittest.main()
