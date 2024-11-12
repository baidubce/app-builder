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
import os

import unittest
import time
import appbuilder

@unittest.skip("ConnectionError: NotFoundError")
class TestBESRetriever(unittest.TestCase):

    def setUp(self):

        # for es test
        self.cluster_id = "..."
        self.username = "..."
        self.password = "..."

        self.embedding = appbuilder.Embedding()
        self.index_type = "hnsw"
        self.vector_index = appbuilder.BESVectorStoreIndex(cluster_id=self.cluster_id,
                                                           user_name=self.username,
                                                           password=self.password,
                                                           embedding=self.embedding)

    def test_generate_id(self):
        id_length = 16
        index_id = appbuilder.BESVectorStoreIndex.generate_id(length=id_length)
        self.assertEqual(len(index_id), id_length)

    def test_create_index_mappings_linear(self):
        index_type = "linear"
        vector_dims = 100
        expected_mappings = {
            'properties': {
                'vector': {
                    'type': 'bpack_vector',
                    'dims': vector_dims,
                }
            }
        }
        actual_mappings = self.vector_index.create_index_mappings(index_type, vector_dims)
        self.assertEqual(actual_mappings, expected_mappings)

    def test_create_index_mappings_hnsw(self):
        index_type = "hnsw"
        vector_dims = 100
        expected_mappings = {
            'properties': {
                'vector': {
                    'type': 'bpack_vector',
                    'dims': vector_dims,
                    'index_type': 'hnsw',
                    'space_type': 'cosine',
                    'parameters': {"m": 4, "ef_construction": 200}
                }
            }
        }
        actual_mappings = self.vector_index.create_index_mappings(index_type, vector_dims)
        self.assertEqual(actual_mappings, expected_mappings)

    def test_add_segments(self):
        segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
        self.vector_index.add_segments(segments)
        time.sleep(5)
        self.assertEqual(self.vector_index.get_all_segments()["hits"]["total"]["value"], len(segments.content))

    def test_query(self):
        segments = appbuilder.Message(["文心一言大模型", "百度在线科技有限公司"])
        vector_index = appbuilder.BESVectorStoreIndex.from_segments(segments, self.cluster_id, self.username,
                                                                    self.password)
        query = appbuilder.Message("文心一言")
        time.sleep(5)
        retriever = vector_index.as_retriever()
        res = retriever(query)
        self.assertEqual(res.content[0]["text"], "文心一言大模型")

    def test_delete_all_segments(self):
        segments = appbuilder.Message(["文心一言大模型"])
        vector_index = appbuilder.BESVectorStoreIndex.from_segments(segments, self.cluster_id, self.username,
                                                                    self.password)
        time.sleep(5)
        vector_index.delete_all_segments()
        time.sleep(5)
        self.assertEqual(vector_index.get_all_segments()["hits"]["total"]["value"], 0)


if __name__ == '__main__':
    unittest.main()
