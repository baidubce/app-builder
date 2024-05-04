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
from appbuilder.core.component import Message

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestRag(unittest.TestCase):

    def test_init_and_http_client_and_debug(self):
        # test_init
        rag = RAG()
        
        # test_http_client
        http_client = rag.http_client
        
        # test_debug
        message=Message()
        rag.debug(query=message)
        
    def test_run(self):
        rag = RAG()
        message = Message()
        response_message=rag.run(query=message,stream=True)
        self.assertIsInstance(response_message,Message)
        
    
if __name__ == '__main__':
    unittest.main()
