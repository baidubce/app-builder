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

import unittest
import appbuilder
import os


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestGetAppList(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "b2a972c5-e082-46e5-b313-acbf51792422"
        self.chatflow_app_id = "4403205e-fb83-4fac-96d8-943bdb63796f"

    def test_describe_app_agent(self):
        app_case = appbuilder.describe_app(self.app_id)
        self.assertIsInstance(app_case.id, str)
        self.assertIsInstance(app_case.name, str)
        self.assertIsInstance(app_case.description, str)

    def test_describe_app_chatflow(self):
        app_case = appbuilder.describe_app(self.chatflow_app_id)
        print(app_case)
        self.assertIsInstance(app_case.id, str)
        self.assertIsInstance(app_case.name, str)
        self.assertIsInstance(app_case.description, str)

if __name__ == '__main__':
    unittest.main()
