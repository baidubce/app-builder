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
import appbuilder


class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 获取当前文件所在的目录路径
        cls.current_dir = os.path.dirname(__file__)
        cls.test_pdf_path = os.path.join(cls.current_dir, 'test.pdf')

    def test_dataset(self):
        # 创建知识库
        dataset = appbuilder.console.Dataset.create_dataset("baidu-test")
        self.assertIsNotNone(dataset.dataset_id)

        # 上传文档
        file_paths = [self.test_pdf_path]
        document_infos = dataset.add_documents(file_paths)
        self.assertEqual(len(document_infos.document_ids), 1)

        # 获取第一页的文档列表, 每页10条
        file_list = dataset.get_documents(1, 10)
        self.assertEqual(file_list.total, 1)

        # 删除文档
        file_ids = [document_infos.document_ids[0]]
        dataset.delete_documents(file_ids)

        # 获取第一页的文档列表, 每页10条
        document_list = dataset.get_documents(1, 10)
        self.assertEqual(document_list.total, 0)


if __name__ == '__main__':
    unittest.main()
