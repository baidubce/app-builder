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

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestKnowLedge(unittest.TestCase):
    def test_doc_knowledage(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)

        upload_res = knowledge.upload_file("./data/qa_appbuilder_client_demo.pdf")
        add_res = knowledge.add_document(content_type='raw_text',
                                         file_ids=[upload_res.id],
                                         custom_process_rule=appbuilder.CustomProcessRule(
                                            separators=["?"], target_length=400,overlap_rate=0.2
                                         ))
        list_res = knowledge.get_documents_list()
        delete_res = knowledge.delete_document(document_id=add_res.document_ids[0])
    
    def test_xlsx_knowledage(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)

        upload_res = knowledge.upload_file("./data/qa_demo.xlsx")
        add_res = knowledge.add_document(content_type='qa', file_ids=[upload_res.id])
        list_res = knowledge.get_documents_list()
        delete_res = knowledge.delete_document(document_id=add_res.document_ids[0])


if __name__ == '__main__':
    unittest.main()
