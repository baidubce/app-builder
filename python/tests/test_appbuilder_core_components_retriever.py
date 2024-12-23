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
import subprocess
import sys
import time 

from appbuilder.core.components.retriever.baidu_vdb.component import _try_import,BaiduVDBVectorStoreIndex


class TestAppbuilderCoreComponentsRetriever__try_import(unittest.TestCase):
    def test_baidu_vdb_baiduvdb_retriever_try_import(self):
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "pymochow"])
        with self.assertRaises(ImportError):
            _try_import()
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymochow"])
        _try_import()
    
    
    def test_baidu_vdb_baiduvdb_retriever_BaiduVDBVectorStoreIndex(self):
        # test not isinstance(instance_id, str): 
        with self.assertRaises(TypeError):
            BaiduVDBVectorStoreIndex(
                instance_id = 1,
                api_key="key", 
            )
        # test not isinstance(api_key, str): 
        with self.assertRaises(TypeError):
            BaiduVDBVectorStoreIndex(
                instance_id = "test",
                api_key=1, 
            )   
    

if __name__ == '__main__':
    unittest.main()