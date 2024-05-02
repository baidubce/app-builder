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
import json
import subprocess

from appbuilder.core.agent import AgentRuntime
from appbuilder.core.component import Component

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreAgent(unittest.TestCase):
    def setup(self):
        self.APPBUILDER_RUN_CHAINLIT=os.getenv('APPBUILDER_RUN_CHAINLIT')
        
    def teardown(self):
        os.environ['APPBUILDER_RUN_CHAINLIT'] = self.APPBUILDER_RUN_CHAINLIT
    
    def test_core_agent_create_flask(self):
        # test_core_agent_create_flask_app
        component = Component()       
        agent = AgentRuntime(component=component)
        subprocess.check_call(['pip', 'uninstall', 'flask', '-y'])
        with self.assertRaises(ImportError):
            agent.create_flask_app()
        subprocess.check_call(['pip', 'install', 'flask==2.3.2'])
        subprocess.check_call(['pip', 'install', 'flask-restful==0.3.9'])
        subprocess.check_call(['pip', 'install', 'werkzeug'])
        app = agent.create_flask_app()
        
        # test_core_agent_serve
        agent.serve()

        # test_core_agent_chainlit_demo
        subprocess.check_call(['pip', 'uninstall', 'chainlit', '-y'])
        with self.assertRaises(ImportError):
            agent.chainlit_demo()
        subprocess.check_call(['pip', 'install', 'chainlit==1.0.200'])
        os.environ['APPBUILDER_RUN_CHAINLIT'] = '1'
        agent.chainlit_demo()
        os.environ['APPBUILDER_RUN_CHAINLIT'] = '0'
        agent.chainlit_demo()
              
    # 附加测试core/component,相关代码还未编写
    def test_core_component(self):
        component = Component()
        component.http_client
        with self.assertRaises(NotImplementedError):
            component.run()
        component.batch()
        component.arun()
        component.abatch()
        component._trace()
        component._debug()
        component.tool_desc()
        component.tool_name()
        component.tool_eval()
        
        
if __name__ == '__main__':
    unittest.main()
        
