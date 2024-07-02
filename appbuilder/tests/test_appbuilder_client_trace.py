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
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-YQRhamcQ5FSMaUi5RltYv/f7c8aadbe3d6ba8b69c8d1367e6a30f71b53d682"
        app_id = "982aaa98-60d4-4120-b4ab-3404a95a61e1"
        app_builder_client = appbuilder.AppBuilderClient(app_id)
        for i in range(1):
            conversation_id = app_builder_client.create_conversation()
            answer = app_builder_client.run(conversation_id=conversation_id, query="AppBuilder是什么？".format(i+1), stream=True)
            for res in answer.content:
                pass
        tracer.end_trace()

if __name__ == '__main__':
    unittest.main()