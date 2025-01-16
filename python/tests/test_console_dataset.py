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
import uuid
import time

import unittest
import appbuilder
from appbuilder.core._client import HTTPClient


@unittest.skip("暂时跳过")
class TestDataset(unittest.TestCase):
    def setUp(self):
        self.dataset_id = os.getenv("DATASET_ID", "UNKNOWN")
    
    @classmethod
    def setUpClass(cls):
        # 获取当前文件所在的目录路径
        cls.current_dir = os.path.dirname(__file__)
        cls.test_pdf_path = os.path.join(cls.current_dir, 'test.pdf')

    def test_create_dataset(self):
        # test_dataset
        dataset_name = "baidu-test"+str(int(time.time()))
        dataset_id=str(uuid.uuid4())
        dataset = appbuilder.console.Dataset(dataset_id=dataset_id, dataset_name=dataset_name)
        dataset.create_dataset
        http_result=dataset.http_client
        self.assertIsInstance(http_result, HTTPClient)
    
    def test_dataset(self):
        # 初始化数据库
        dataset = appbuilder.console.Dataset(
            dataset_id=self.dataset_id,
            dataset_name="勿删-appbuilder-sdk测试数据集"
        )
        self.assertIsNotNone(dataset.dataset_id)

        # 上传文档
        file_paths = [self.test_pdf_path]
        document_infos = dataset.add_documents(file_paths)
        self.assertEqual(len(document_infos.document_ids), 1)

        # 获取第一页的文档列表, 每页10条
        file_list = dataset.get_documents(1, 10)
        self.assertIsInstance(file_list.total, int)

        # 删除文档
        file_ids = [document_infos.document_ids[0]]
        dataset.delete_documents(file_ids)

        # 获取第一页的文档列表, 每页10条
        document_list = dataset.get_documents(1, 10)
        self.assertIsInstance(document_list.total, int)


if __name__ == '__main__':
    unittest.main()
