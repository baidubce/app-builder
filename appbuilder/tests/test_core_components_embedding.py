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

from appbuilder.core.components.embeddings.component import Embedding
from appbuilder.core.components.embeddings.base import EmbeddingBaseComponent
from appbuilder.core._exception import ModelNotSupportedException,AppBuilderServerException

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreComponentsEmbedding(unittest.TestCase):
            
    def test_embeddings_base(self):
        ebc=EmbeddingBaseComponent()
        message=[1,2,3]
        ebc.abatch(texts=message)
        
    def test_embeddings_component_init(self):
        # test_embeddings_component_init
        with self.assertRaises(ModelNotSupportedException):
            emb=Embedding()
            emb.accepted_models.append('test')
            emb.__init__('test')
            
    
    def test_embeddings_component(self):
        #test_embeddings_component_check_response_json
        emb=Embedding()
        data={
            'error_code':'error_code',
            'error_msg': 'error_msg'
        }
        with self.assertRaises(AppBuilderServerException):
            emb._check_response_json(data=data)
                    
        # test_embeddings_component_batchify
        texts=['test','test']
        with self.assertRaises(ValueError):
            emb._batchify(texts=texts,batch_size=17)
            
if __name__ == '__main__':
    unittest.main()