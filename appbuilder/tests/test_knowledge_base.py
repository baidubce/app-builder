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
import requests
import appbuilder
import os
import time
import logging

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestKnowLedge(unittest.TestCase):
    def setUp(self) -> None:
        appbuilder.logger.setLoglevel("DEBUG")
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-V3xPTLgugTepGXYzJJAPQ/1c6eb19cb7df08b1e26b8fb7c2113ce555b3d62c"
        os.environ["GATEWAY_URL_V2"] = "https://qianfan.baidubce.com"
    
    def test_create_knowledage(self):
        knowledge_name = "test_knowledge_" + str(int(time.time()))
        knowledge = appbuilder.KnowledgeBase.create_knowledge(knowledge_name)
        # knowledge = appbuilder.KnowledgeBase(knowledge_id="290dbbe5-34c7-4fc5-918a-4a71397e9698")
        print(knowledge.knowledge_id)
        upload_res = knowledge.upload_file("./data/qa_appbuilder_client_demo.pdf")
        # print(upload_res)
        add_res = knowledge.add_document(
            content_type='raw_text',
            file_ids=[upload_res.id]
        )        
        print(add_res)

        list_res = knowledge.get_documents_list()
        print(list_res)

        delete_res = knowledge.delete_document(
            document_id=add_res.document_ids[0]
        )
        print(delete_res)



if __name__ == '__main__':
    unittest.main()
