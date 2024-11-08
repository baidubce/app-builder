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
# !/usr/bin/env python3


import os
import unittest
from typing import List, Tuple
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestBaiduVDBRetrieverParameter(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ABCDE"

    def test_run_parameter_query(self):
        query = appbuilder.Message('')
        retriever = appbuilder.BaiduVDBRetriever(
            embedding="abcde",
            table="abcde")
        
        with self.assertRaises(ValueError) as context:
            retriever.run(query)
        self.assertIn("Parameter `query` content is empty", str(context.exception))
    
    def test_run_paramter_query_type(self):
        query = appbuilder.Message(content=12345)

        retriever = appbuilder.BaiduVDBRetriever(
            embedding="abcde",
            table="abcde")
        
        with self.assertRaises(ValueError) as context:
            retriever.run(query)
        self.assertIn("Parameter `query` content is not a string", str(context.exception))

    def test_run_parameter_query_length(self):
        query = appbuilder.Message(content="a" * 1025)
        retriever = appbuilder.BaiduVDBRetriever(
            embedding="abcde",
            table="abcde")
        with self.assertRaises(ValueError) as context:
            retriever.run(query)
        self.assertIn("Parameter `query` content is too long", str(context.exception))

    def test_run_parameter_topk_positive(self):
        query = appbuilder.Message()
        retriever = appbuilder.BaiduVDBRetriever(
            embedding="abcde",
            table="abcde")
        with self.assertRaises(ValueError) as context:
            retriever.run(query, top_k=-1)
        self.assertIn("Parameter `top_k` must be a positive integer", str(context.exception))

class TestVDBParameterCheck(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ABCDE"

    def test_vdb_parameter_account(self):
        with self.assertRaises(TypeError) as context:
            appbuilder.BaiduVDBVectorStoreIndex(
                instance_id="abcde",
                api_key="abcde",
                account=123456)
        self.assertIn("must be a string", str(context.exception))
        
    def test_vdb_parameter_database_name(self):
        with self.assertRaises(TypeError) as context:
            appbuilder.BaiduVDBVectorStoreIndex(
                instance_id="abcde",
                api_key="abcde",
                database_name=123456)
        self.assertIn("must be a string", str(context.exception))


    def test_vdb_parameter_table_params(self):
        with self.assertRaises(TypeError) as context:
            appbuilder.BaiduVDBVectorStoreIndex(
                instance_id="abcde",
                api_key="abcde",
                table_params=123456)
        self.assertIn("must be a TableParams", str(context.exception))

    def test_vdb_parameter_embedding(self):
        with self.assertRaises(TypeError) as context:
            appbuilder.BaiduVDBVectorStoreIndex(
                instance_id="abcde",
                api_key="abcde",
                embedding=123456)
        self.assertIn("must be a Embedding", str(context.exception))


if __name__ == '__main__':
    unittest.main()
