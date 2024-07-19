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


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestKnowLedge(unittest.TestCase):
    def test_doc_knowledage(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)

        upload_res = knowledge.upload_file("./data/qa_appbuilder_client_demo.pdf")
        add_res = knowledge.add_document(
            content_type="raw_text",
            file_ids=[upload_res.id],
            custom_process_rule=appbuilder.CustomProcessRule(
                separators=["?"], target_length=400, overlap_rate=0.2
            ),
        )
        list_res = knowledge.get_documents_list()
        delete_res = knowledge.delete_document(document_id=add_res.document_ids[0])

    def test_xlsx_knowledage(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)

        upload_res = knowledge.upload_file("./data/qa_demo.xlsx")
        add_res = knowledge.add_document(content_type="qa", file_ids=[upload_res.id])
        list_res = knowledge.get_documents_list()
        delete_res = knowledge.delete_document(document_id=add_res.document_ids[0])

    def test_create_knowledge_base(self):
        knowledge = appbuilder.KnowledgeBase()
        resp = knowledge.create_knowledge_base(
            name="test",
            description="test",
            type="public",
            esUrl="http://localhost:9200",
            esUserName="elastic",
            esPassword="changeme",
        )

        knowledge_base_id = resp.id
        knowledge.get_knowledge_base_detail(knowledge_base_id)
        knowledge.get_knowledge_base_list(knowledge_base_id, maxKeys=10)
        knowledge.create_documents(
            id=knowledge_base_id,
            contentFormat="rawText",
            source=appbuilder.DocumentSource(
                type="web",
                urls=["https://baijiahao.baidu.com/s?id=1802527379394162441"],
                urlDepth=1,
            ),
            processOption=appbuilder.DocumentProcessOption(
                template="custom",
                parser=appbuilder.DocumentChoices(choices=["layoutAnalysis", "ocr"]),
                chunker=appbuilder.DocumentChunker(
                    choices=["separator"],
                    separator=appbuilder.DocumentSeparator(
                        separators=["。"],
                        targetLength=300,
                        overlapRate=0.25,
                    ),
                    prependInfo=["title", "filename"],
                ),
                knowledgeAugmentation=appbuilder.DocumentChoices(choices=["faq"]),
            ),
        )

        knowledge.upload_documents(
            id=knowledge_base_id,
            content_format="rawText",
            file_path="./appbuilder/tests/data/qa_appbuilder_client_demo.pdf",
            processOption=appbuilder.DocumentProcessOption(
                template="custom",
                parser=appbuilder.DocumentChoices(choices=["layoutAnalysis", "ocr"]),
                chunker=appbuilder.DocumentChunker(
                    choices=["separator"],
                    separator=appbuilder.DocumentSeparator(
                        separators=["。"],
                        targetLength=300,
                        overlapRate=0.25,
                    ),
                    prependInfo=["title", "filename"],
                ),
                knowledgeAugmentation=appbuilder.DocumentChoices(choices=["faq"]),
            ),
        )

        knowledge.modify_knowledge_base(
            knowledge_base_id=knowledge_base_id, name="test"
        )
        knowledge.delete_knowledge_base(knowledge_base_id)
        self.assertIsNotNone(knowledge_base_id)

    def test_create_chunk(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)
        list_res = knowledge.get_documents_list()
        document_id = list_res.data[0].id
        resp = self.knowledge.create_chunk(document_id, content="test")
        chunk_id = resp.id
        knowledge.modify_chunk(chunk_id, content="new test", enable=True)
        knowledge.describe_chunk(chunk_id)
        knowledge.describe_chunks(document_id)
        knowledge.delete_chunk(chunk_id)


if __name__ == "__main__":
    unittest.main()
