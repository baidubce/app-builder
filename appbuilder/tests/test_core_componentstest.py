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
import appbuilder
import requests

from  unittest.mock import Mock
from appbuilder.core._exception import AppbuilderBuildexException


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestComponents(unittest.TestCase):
    def setUp(self):
        self.image_understand = appbuilder.ImageUnderstand()
        self.table_ocr = appbuilder.TableOCR()
        self.img_url = 'img_url'


    def test_components_raise(self):
        tool_eval_input = {}
        response = requests.Response()
        # 检查tool_eval必须有streaming参数
        with self.assertRaises(AppbuilderBuildexException) as e:
            appbuilder.AppbuilderTestToolEval(appbuilder_components=self.image_understand,
                                                tool_eval_input=tool_eval_input,
                                                response=response)
        exception = e.exception
        self.assertIn('是否定义streaming', str(exception))

        # 检查组件tool_eval的传入参数是否有traceid
        tool_eval_input = {
            'streaming': True,
        }
        with self.assertRaises(AppbuilderBuildexException) as e:
            appbuilder.AppbuilderTestToolEval(appbuilder_components=self.image_understand,
                                                tool_eval_input=tool_eval_input,
                                                response=response)
        exception = e.exception
        self.assertIn('传入参数是否有traceid', str(exception))
        
        # 检查组件tool_eval的传入参数是否正确或manifests的参数定义是否正确(required为anyOf)
        tool_eval_input = {
            'streaming': True,
            'traceid': 'traceid',
        }
        with self.assertRaises(AppbuilderBuildexException) as e:
            appbuilder.AppbuilderTestToolEval(appbuilder_components=self.image_understand,
                                                tool_eval_input=tool_eval_input,
                                                response=response)
        exception = e.exception
        self.assertIn('组件tool_eval的传入参数是否正确或manifests的参数定义是否正确', str(exception))

        # 检查组件tool_eval的传入参数是否正确或manifests的参数定义是否正确(required不为anyOf)
        tool_eval_input = {
            'streaming': True,
            'traceid': 'traceid',
        }
        with self.assertRaises(AppbuilderBuildexException) as e:
            appbuilder.AppbuilderTestToolEval(appbuilder_components=self.table_ocr,
                                            tool_eval_input=tool_eval_input,
                                            response=response)
        exception = e.exception
        self.assertIn('组件tool_eval的传入参数是否正确或manifests的参数定义是否正确', str(exception))
    
    def test_components_tool_eval_image_understand(self): 
        mock_response_data = {
            'result': {'task_id': '1821485837570181996'},
            'log_id': 1821485837570181996,
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'application/json'}
        def mock_json():
            return mock_response_data
        mock_response.json = mock_json
        
        tool_eval_input = {
            'streaming': True,
            'traceid': 'traceid',
            'name':"image_understand", 
            'img_url':self.img_url, 
            'origin_query':""
        }

        appbuilder.AppbuilderTestToolEval(appbuilder_components=self.image_understand,
                                                tool_eval_input=tool_eval_input,
                                                response=mock_response)
        

if __name__ == "__main__":
    unittest.main()
        