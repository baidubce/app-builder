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
from appbuilder.utils.model_util import (
    GetModelListRequest, 
    Models, 
    GetModelListResponse,
    GetModelListRequestV2,
    GetModelListResponseV2,
    CommonModelV2
)
token = "Bearer bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd"

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
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

    def test_get_model_list(self):
        """
        get_model_list方法单测

        Args:
            None

        Returns:
            None

        """
        response = appbuilder.get_model_list(secret_key=token, api_type_filter=["text2image"])
        print(response)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)

    def _test_list(self):
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

    def _test_check_service_error(self):
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

    # def test_model(self):
    #     model = {'serviceId': 'svcp-0bf727e92474', 'name': 'Qianfan-PublicOpinion-Classification', 'url': 'http://qianfan.baidubce.com/v2/chat/completions', 'serviceType': 'image2text', 'chargeStatus': 'Opened', 'protocolVersion': 2, 'isPublic': True, 'chargeType': 'Calls', 'modelCallName': 'qianfan-publicopinion-classification', 'supportedProtocolVersions': [2], 'maxContextTokens': None, 'maxInputTokens': None, 'maxOutputTokens': None, 'reasoningModel': False, 'supportsSearch': False}
    #     a = CommonModelV2.model_validate(model)

if __name__ == '__main__':
    unittest.main()
