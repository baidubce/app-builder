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
import appbuilder
import os

from appbuilder.core.console.rag.rag import RAG


@unittest.skip("暂时跳过")
class TestRag(unittest.TestCase):

    def setUp(self):
        self.app_id = "06e3f5c9-885d-4f85-af57-97dc85ee4606"

    def test_rag(self):
        rag_app = RAG(self.app_id)
        query = "写一个200字作文，主题关于百度AI"
        answer = rag_app.run(appbuilder.Message(query))
        self.assertIsNotNone(answer.content)
        
        # test debug
        rag_app.debug(appbuilder.Message(query))


if __name__ == '__main__':
    unittest.main()
