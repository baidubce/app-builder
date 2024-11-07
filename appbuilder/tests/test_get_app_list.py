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
from appbuilder.utils.model_util import GetModelListRequest, Models, GetModelListResponse
appbuilder.logger.setLoglevel("DEBUG")

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestApps(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.model = Models()

    def test_get_app_list(self):
        response = appbuilder.get_app_list()
        self.assertIsInstance(response, list)

    def test_get_app_list_v2(self):
        response = appbuilder.get_app_list(limit=2)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response),2)

    def test_get_app_list_v3(self):
        self.assertRaises(ValueError, appbuilder.get_app_list, limit=200)
        self.assertRaises(ValueError, appbuilder.get_app_list, limit=0)

    def test_get_app_list_v4(self):
        self.assertRaises(ValueError, appbuilder.get_app_list, limit="a")

    def test_get_app_number(self):
        app_list = appbuilder.get_all_apps()
        self.assertIsInstance(app_list, list)

if __name__ == '__main__':
    unittest.main()
