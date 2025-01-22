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
import time

import appbuilder

from appbuilder import BESVectorStoreIndex
from appbuilder import BaiduVDBVectorStoreIndex,TableParams
from appbuilder.core.component import Message 

@unittest.skip(reason="vdb欠费了,跳过")
class TestBaiduVbdRetriever(unittest.TestCase):
    def setUp(self):
        self.instance_id=os.getenv("INSTANCE_ID", "UNKNOWN")
        self.api_key=os.getenv("BAIDU_VDB_API_KEY", "UNKNOWN")

        
    def test_BaiduVDBVectorStoreIndex_init(self):
        bvvsi=BaiduVDBVectorStoreIndex(self.instance_id, self.api_key)
        
    def test_create_database_if_not_exists_and_create_table(self):
        bvvsi=BaiduVDBVectorStoreIndex(self.instance_id, self.api_key)
        dataset_name="test_dataset"+str(int(time.time()))
        bvvsi._create_database_if_not_exists(dataset_name)
        with self.assertRaises(ValueError):
            bvvsi._create_table(table_params=None)
        bvvsi._create_table(table_params=TableParams(dimension=384))
        
        # test_as_retriever
        retriever=bvvsi.as_retriever()
        
        # test_add_segments
        message=Message()
        with self.assertRaises(IndexError):
            bvvsi.add_segments(message)

        

        
if __name__ == '__main__':
    unittest.main()