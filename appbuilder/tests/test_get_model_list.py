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

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestModels(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.model = Models()

    def get_model_list(self):
        """
        get_model_list方法单测

        Args:
            None

        Returns:
            None

        """
        response = appbuilder.get_model_list(api_type_filter=["chat"])
        self.assertIsNotNone(response)
        self.assertIsInstance(response, GetModelListResponse)
        self.assertTrue(response.success)

    def test_list(self):
        """
        list方法单测

        Args:
            None

        Returns:
            None

        """

        request = GetModelListRequest()
        response = self.model.list(request)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, GetModelListResponse)

    def test_check_service_error(self):
        """
        check_service_error方法单测

        Args:
            None

        Returns:
            None

        """
        data = {'error_msg': 'Error', 'error_code': 1}
        request_id = "request_id"
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.model._check_service_error(request_id, data)
        data = {'error_msg': 'No Error', 'error_code': 0}
        self.assertIsNone(self.model._check_service_error(request_id, data))


if __name__ == '__main__':
    unittest.main()
