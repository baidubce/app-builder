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
import os
import unittest

import appbuilder

from appbuilder.core.components.retriever.bes.bes_retriever import BESVectorStoreIndex,BESRetriever
from appbuilder.core.components.retriever.baidu_vdb.baiduvdb_retriever import BaiduVDBVectorStoreIndex
from appbuilder.core.components.embeddings.component import Embedding
from appbuilder.core.component import Message 

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestRetriever(unittest.TestCase):
    def test_bes_bes_retriever_BESVectorStoreIndex(self):
        # 需要密码
        with self.assertRaises(ConnectionError):
            bvs=BESVectorStoreIndex(
                cluster_id="test_id",
                user_name="test_name",
                password="<PASSWORD>"         
            )
            
    def test__bes_bes_retriever_BESRetriever(self):
        embedding=Embedding()
        br=BESRetriever(
            embedding=embedding,
            index_name="index_name",
            bes_client="bes_client"
        )
        message=Message("文心一言")
        with self.assertRaises(AttributeError):
            br.run(message)
            
    def test_baidu_vdb_baiduvdb_retrieve_BaiduVDBVectorStoreIndex(self):
        with self.assertRaises(Exception):
            bvvs=BaiduVDBVectorStoreIndex(
                instance_id="test_id",
                api_key=os.getenv("APPBUILDER_TOKEN", "")      
            )

        
if __name__ == '__main__':
    unittest.main()