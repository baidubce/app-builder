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

from appbuilder.utils.trace.tracer import AppBuilderTracer, AppbuilderInstrumentor
from appbuilder.utils.trace.phoenix_wrapper import runtime_main,stop_phoenix
from appbuilder.core.console.appbuilder_client import get_app_list

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderTrace(unittest.TestCase):
    def setUp(self):
        self.app_id = "2a19f6dd-de02-46d9-841d-ef5c52b00466"
    
    def test_appbuilder_client_trace(self):

        tracer=AppBuilderTracer(
            enable_phoenix = True,
            enable_console = True,
            )
        
        tracer.start_trace()

        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        
        # test stream = True
        msg = builder.run(conversation_id=conversation_id, query="人参有什么用？",stream=True)
        for m in msg.content:
            print(m)

        # test stream = False
        builder.run(conversation_id=conversation_id, query="人参有什么用？")

        # test get_app_list
        get_app_list()


        tracer.end_trace()


    def test_client_trace_function(self):
        from appbuilder.utils.trace._function import _client_tool_trace_output,_client_tool_trace_output_deep_iterate
        class Test:
            test = 'test'
        _client_tool_trace_output(Test,None)

        _client_tool_trace_output_deep_iterate({},None)

    def test_trace_tracer(self):
        tracer=AppbuilderInstrumentor()
        tracer.instrumentation_dependencies()
        tracer._instrument()
        

    def test_appbuilder_phoenix_run(self):

        runtime_main()
        with self.assertRaises(TypeError):
            stop_phoenix()


if __name__ == '__main__':
    unittest.main()
            

        

    
        