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
import requests
import appbuilder
import os
import logging

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestGetAppList(unittest.TestCase):
    def test_get_app_list_v1(self):
        app_list = appbuilder.get_app_list()
        print(app_list)
        self.assertIsInstance(app_list, list)

if __name__ == '__main__':
    unittest.main()
