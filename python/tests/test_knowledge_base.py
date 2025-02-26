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
import appbuilder
import os

from appbuilder.core._exception import BadRequestException
from appbuilder.core.console.knowledge_base import data_class


class TestKnowLedge(unittest.TestCase):
    def setUp(self):
        self.whether_create_knowledge_base = False

    def test_doc_knowledage(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        appbuilder.logger.setLoglevel('DEBUG')
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)

        upload_res = knowledge.upload_file(
            "./data/qa_appbuilder_client_demo.pdf")
        add_res = knowledge.add_document(
            content_type="raw_text",
            file_ids=[upload_res.id],
            custom_process_rule=appbuilder.CustomProcessRule(
                separators=["?"], target_length=400, overlap_rate=0.2
            ),
        )
        list_res = knowledge.get_documents_list()
        delete_res = knowledge.delete_document(
            document_id=add_res.document_ids[0])
        all_doc = knowledge.get_all_documents()
        self.assertIsInstance(all_doc, list)

    def test_get_documents_number_raise(self):
        knowledge = appbuilder.KnowledgeBase()
        with self.assertRaises(ValueError):
            knowledge.get_all_documents()

    def test_xlsx_knowledage(self):
        dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
        knowledge = appbuilder.KnowledgeBase(knowledge_id=dataset_id)

        upload_res = knowledge.upload_file("./data/qa_demo.xlsx")
        add_res = knowledge.add_document(
            content_type="qa", file_ids=[upload_res.id])
        list_res = knowledge.get_documents_list()
        delete_res = knowledge.delete_document(
            document_id=add_res.document_ids[0])

    def test_create_knowledge_base(self):
        knowledge = appbuilder.KnowledgeBase()
        appbuilder.logger.setLoglevel("DEBUG")
        try:
            resp = knowledge.create_knowledge_base(
                name="test",
                description="test",
                type="public",
                pathPrefix="/全部群组",
            )
            knowledge_base_id = resp.id
            knowledge.get_knowledge_base_detail(knowledge_base_id)
            knowledge.get_knowledge_base_list(knowledge_base_id, maxKeys=10)
            self.whether_create_knowledge_base = True
        except BadRequestException as e:
            print("create_knowledge_base函数运行失败{},将调用本地DATASET_ID".format(e))
            knowledge_base_id = os.getenv('DATASET_ID', 'UNKNOWN')

        create_documents_response = knowledge.create_documents(
            id=knowledge_base_id,
            contentFormat="rawText",
            source=appbuilder.DocumentSource(
                type="web",
                urls=["https://baijiahao.baidu.com/s?id=1802527379394162441"],
                urlDepth=1,
                urlConfigs=[appbuilder.DocumentSourceUrlConfig(frequency=1)]
            ),
            processOption=appbuilder.DocumentProcessOption(
                template="custom",
                parser=appbuilder.DocumentChoices(
                    choices=["layoutAnalysis", "ocr"]
                ),
                chunker=appbuilder.DocumentChunker(
                    choices=["separator"],
                    separator=appbuilder.DocumentSeparator(
                        separators=["。"],
                        targetLength=300,
                        overlapRate=0.25,
                    ),
                    prependInfo=["title", "filename"],
                ),
                knowledgeAugmentation=appbuilder.DocumentChoices(choices=[
                                                                 "faq"]),
            ),
        )
        self.assertIsInstance(create_documents_response.documentIds, list)

        upload_documents_response = knowledge.upload_documents(
            id=knowledge_base_id,
            content_format="rawText",
            file_path="./data/qa_appbuilder_client_demo.pdf",
            processOption=appbuilder.DocumentProcessOption(
                template="custom",
                parser=appbuilder.DocumentChoices(
                    choices=["layoutAnalysis", "ocr"]
                ),
                chunker=appbuilder.DocumentChunker(
                    choices=["separator"],
                    separator=appbuilder.DocumentSeparator(
                        separators=["。"],
                        targetLength=300,
                        overlapRate=0.25,
                    ),
                    prependInfo=["title", "filename"],
                ),
                knowledgeAugmentation=appbuilder.DocumentChoices(choices=[
                                                                 "faq"]),
            ),
        )
        self.assertIsInstance(upload_documents_response.documentId, str)

        knowledge.get_documents_list(
            knowledge_base_id=knowledge_base_id)
        list_res = knowledge.describe_documents(knowledge_base_id=knowledge_base_id)
        document_id = list_res.data[-1].id
        knowledge.describe_chunks(document_id, knowledgebase_id=knowledge_base_id, keyword="test")
        resp = knowledge.create_chunk(document_id, content="test", knowledgebase_id=knowledge_base_id)
        chunk_id = resp.id
        knowledge.modify_chunk(chunk_id, content="new test", enable=True, knowledgebase_id=knowledge_base_id)
        # 目前openapi有延迟，后续openapi完善后，删除注释
        knowledge.describe_chunk(chunk_id, knowledgebase_id=knowledge_base_id)
        knowledge.delete_chunk(chunk_id, knowledgebase_id=knowledge_base_id)

        knowledge.modify_knowledge_base(
            knowledge_base_id=knowledge_base_id,
            name="test",
            pathPrefix="/全部群组",
        )

        if self.whether_create_knowledge_base:
            knowledge.delete_knowledge_base(knowledge_base_id)

    def test_query_knowledge_base(self):
        knowledge = appbuilder.KnowledgeBase()
        appbuilder.logger.setLoglevel("DEBUG")
        client = appbuilder.KnowledgeBase()
        res = client.query_knowledge_base(
            query="民法典第三条",
            type="fulltext",
            knowledgebase_ids=["70c6375a-1595-41f2-9a3b-e81bc9060b7f"],
            top=5,
            skip=0,
            metadata_filters=data_class.MetadataFilters(filters=[], condition="or"),
            pipeline_config=data_class.QueryPipelineConfig(
                id="pipeline_001",
                pipeline=[
                    {
                        "name": "step1",
                        "type": "elastic_search",
                        "threshold": 0.1,
                        "top": 400,
                        "pre_ranking": {
                            "bm25_weight": 0.25,
                            "vec_weight": 0.75,
                            "bm25_b": 0.75,
                            "bm25_k1": 1.5,
                            "bm25_max_score": 50,
                        },
                    },
                    {
                        "name": "step2",
                        "type": "ranking",
                        "inputs": ["step1"],
                        "model_name": "ranker-v1",
                        "top": 20,
                    },
                ],
            ),
        )
        chunk_id = res.chunks[0].chunk_id
        self.assertIsNotNone(chunk_id)


if __name__ == "__main__":
    unittest.main()
