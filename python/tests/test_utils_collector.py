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

from collections import OrderedDict
from appbuilder.utils.collector import Collector

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCollector(unittest.TestCase):
    def test_del_collection(self):
        collector = Collector()

        # test del_collection with not name
        collector.del_collection("test")

        # test del_collection with name
        collector.add_to_collection("test", 1)
        collector.del_collection("test")

    def test_other_collection(self):
        collector = Collector()
        # test if collection is None and index_key is None
        result=collector.get_collection("test")
        self.assertEqual(result, [])

        # test if index_key is not None
        collector.add_to_collection("test", 1,'test-key')
        result=collector.get_collection(name="test", index_key='test-key')
        self.assertEqual(result, 1)

        # test if index_key is None and collection is not None
        collector.add_to_collection("test01", 1)
        result=collector.get_collection(name="test01", index_key='test-key')
        self.assertEqual(result,None)

        # get_collection_as_dict
        result=collector.get_collection_as_dict("test")
        self.assertEqual(type(result), OrderedDict)
        result=collector.get_collection_as_dict("test", reverse=True)
        self.assertEqual(type(result), OrderedDict)
        result=collector.get_collection_as_dict("test02")
        self.assertEqual(type(result), OrderedDict)

        # get_all_collection_keys
        collector.get_all_collection_keys()
        
        # test clear_collection 清空collection
        collector.clear_collection("test")
        collector.clear_collection("test01")


if __name__ == "__main__":
    unittest.main()


