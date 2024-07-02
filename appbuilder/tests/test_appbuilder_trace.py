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

from unittest.mock import patch,MagicMock

from appbuilder.utils.trace.tracer import AppBuilderTracer
from appbuilder.utils.trace.phoenix_wrapper import runtime_main
from appbuilder.core.console.appbuilder_client import get_app_list


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderTrace(unittest.TestCase):
    def setUp(self):
        self.app_id = "aa8af334-df27-4855-b3d1-0d249c61fc08"
    

    def test_appbuilder_client_trace(self):
        
        tracer=AppBuilderTracer(
            enable_phoenix = True,
            enable_console = True,
            )
        
        tracer.start_trace()

        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        
        # test stream = True
        builder.run(conversation_id=conversation_id, query="你可以做什么？",stream=True)

        # test stream = False
        builder.run(conversation_id=conversation_id, query="你可以做什么？")

        # test get_app_list
        get_app_list()

        tracer.end_trace()

    
    def test_appbuilder_phoenix_run(self):

        runtime_main()



if __name__ == '__main__':
    unittest.main()
            

        

    
        