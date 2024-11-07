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
import unittest
import os
import base64

import appbuilder.core.utils as ut
from appbuilder.utils.sse_util import SSEClient,Event



@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreUtils(unittest.TestCase):
    def test_utils_get_user_agent(self):
        user_agent=ut.utils_get_user_agent()
    
    def test_get_model_list(self):
        from appbuilder.core._exception import TypeNotSupportedException 
        with self.assertRaises(TypeNotSupportedException):
            model_list=ut.get_model_list(api_type_filter=["unknown"])

    def test_convert_cloudhub_url(self):
        try:    
            from appbuilder.core._client import HTTPClient
        except:
            pass
        with self.assertRaises(ValueError):
            url=ut.convert_cloudhub_url(client=HTTPClient,qianfan_url="unknown")

    def test_is_url(self):
        is_url=ut.is_url("unknown")

    # def test_utils_sse_uti_events(self):
    #     binary_data = os.urandom(100)  # 生成100字节的随机数据
    #     encoded_data = base64.b64encode(binary_data).decode('utf-8')
    #     sseClient=SSEClient(event_source=encoded_data)
    #     sseClient.events()

    # def test_utils_sse_uti_events(self):
    #     binary_data = os.urandom(100)  # 生成100字节的随机数据
    #     encoded_data = base64.b64encode(binary_data).decode('utf-8')
    #     sseClient=SSEClient(event_source=encoded_data)
    #     sseClient.close()

    def test_utils_sse_uti_Events(self):
        event_null_data=Event(id="id")
        s=event_null_data.debug_str
        event=Event(id="id",data='data',retry="retry")
        s=event.debug_str
        event.raw="raw"
        s_change_raw=event.debug_str


if __name__ == '__main__':
    unittest.main()

        



    
    

