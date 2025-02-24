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
from unittest.mock import patch, MagicMock
import requests
import appbuilder
from appbuilder.core._exception import *
from appbuilder.core.component import ComponentOutput
from appbuilder.core._client import HTTPClient, AsyncHTTPClient

class Response:
    def __init__(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCheckResponse(unittest.TestCase):
    def test_check_response(self):
        client = HTTPClient()
        response = Response(405, {'Content-Type': 'application/json'}, '{"code": 0, "message": "MethodNotAllowedException", "requestId": "1673896516"}')
        with self.assertRaises(MethodNotAllowedException):
            client.check_response(response)

if __name__ == "__main__":
    unittest.main()