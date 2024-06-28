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

# appbuilder.logger.setLoglevel("Debug")

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderTrace(unittest.TestCase):
    def test_appbuilder_client_trace(self):
        tracer = appbuilder.AppBuilderTracer(enable_console=False, host="http://localhost")
        tracer.start_trace()
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-5YNeRZpFfjpnCWYry9rKv/78b563903ba74c7a1417734b90658e5121ce0d76"
        app_id = "afb96fb5-545d-4a81-8c91-c43359e28ede"
        app_builder_client = appbuilder.AppBuilderClient(app_id)
        for i in range(1):
            conversation_id = app_builder_client.create_conversation()
            answer = app_builder_client.run(conversation_id=conversation_id, query="第{}次向你问好".format(i+1))
        tracer.end_trace()

if __name__ == '__main__':
    unittest.main()