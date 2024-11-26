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

from appbuilder.utils.trace.tracer import AppBuilderTracer, AppbuilderInstrumentor
from appbuilder.utils.trace.phoenix_wrapper import runtime_main,stop_phoenix,launch_phoenix
from appbuilder.core.console.appbuilder_client import get_app_list

class TestAppBuilderTrace(unittest.TestCase):
    def setUp(self):
        """
        初始化方法，用于设置测试前的环境。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        self.app_id = "2a19f6dd-de02-46d9-841d-ef5c52b00466"
    
    def test_appbuilder_client_trace_un_stream(self):
        """
        测试AppBuilderClient的跟踪功能
        
        Args:
            无
        
        Returns:
            无返回值，该函数主要用于测试跟踪功能
        
        """

        tracer=AppBuilderTracer(
            enable_phoenix = True,
            enable_console = False,
            )
        
        tracer.start_trace()

        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        
        # test stream = True
        msg = builder.run(conversation_id=conversation_id, query="人参有什么用？",stream=False)
        print(msg)
        tracer.end_trace()

    def test_appbuilder_client_trace_stream(self):
        """
        测试AppBuilderClient的跟踪功能
        
        Args:
            无
        
        Returns:
            无返回值，该函数主要用于测试跟踪功能
        
        """

        tracer=AppBuilderTracer(
            enable_phoenix = True,
            enable_console = False,
            )
        
        tracer.start_trace()

        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        
        # test stream = True
        msg = builder.run(conversation_id=conversation_id, query="人参有什么用？",stream=True)
        for m in msg.content:
            pass

        # test get_app_list
        get_app_list()


        tracer.end_trace()

    def test_trace_tracer(self):
        """
        测试AppbuilderInstrumentor类的trace_tracer方法。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        tracer=AppbuilderInstrumentor()
        tracer.instrumentation_dependencies()
        tracer._instrument()
        

    def test_appbuilder_phoenix_run(self):
        """
        测试appbuilder_phoenix_run方法
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        Raises:
            TypeError: 当调用runtime_main()或stop_phoenix()函数时，预期会抛出TypeError异常。
        
        """
        with self.assertRaises(ImportError):
            runtime_main()
        
        with self.assertRaises(ImportError):
            launch_phoenix()
            
        with self.assertRaises(ImportError):
            stop_phoenix()


if __name__ == '__main__':
    unittest.main()
            

        

    
        