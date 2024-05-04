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

from unittest.mock import MagicMock
from appbuilder.utils.sse_util import SSEClient,Event
from appbuilder.utils.model_util import RemoteModel,Models
from appbuilder.utils.logger_util import LoggerWithLoggerId,_setup_logging
from threading import current_thread 

# 创建一个logger类
class test_logger_level():
    def __init__(self):
        self.level='level'

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestUtils(unittest.TestCase):
    def test_sse_util_SSEClient(self):
        mock_event_source = MagicMock()
        mock_event_source.__iter__.return_value = iter([
            b'data: Test event 1\n\n',
            b'data: Last incomplete event'
        ])
        sse_client = SSEClient(event_source=mock_event_source)
        event_generator = sse_client._read()
        self.assertEqual(next(event_generator), b'data: Test event 1\n\n')
        self.assertEqual(next(event_generator), b'data: Last incomplete event')
        # 测试是否抛出 StopIteration 异常，表示没有更多事件
        with self.assertRaises(StopIteration):
            next(event_generator)
        
        # test_events
        mock_event_source.__iter__.return_value = iter([
            b': Test event 1\n\n',
            b'test: Test event 2\n\n',
            b'data:Testevent3\n\n',
            b'data\n\n',
            b'event:Testevent5\n\n',
        ])
        sse_client = SSEClient(event_source=mock_event_source)
        for event in sse_client.events():
            pass
        # test_close
        sse_client.close()
        
    def test_sse_util_Event(self):
        # test_str_
        event_str=str(Event(id='id',retry=10))
        assert event_str.startswith('message')
        
    def test_model_util_RemoteModel(self):
        # test_get_remote_name_by_short_name
        rm=RemoteModel(remote_name='test_remote')
        rm.get_remote_name_by_short_name(short_name="eb-turbo-appbuilder")
    
    def test_model_util_Models(self):
        # test_list
        models=Models()
        models.list(retry=-1)
        
    def test_logger_util_LoggerWithLoggerId(self):
        # test_get_logid
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        self.assertEqual(lwl.get_logid(),None)
        lwl.logid_dict[current_thread().ident]='ident'
        self.assertEqual(lwl.get_logid(),'ident')
        
        # test_process
        kwargs={
            'extra':{'logid':'test_logid'}
        }
        msg,kwargs=lwl.process(msg='test_msg',kwargs=kwargs)
        self.assertEqual(kwargs['extra']['logid'],lwl.logid_dict[current_thread().ident])
        msg,kwargs=lwl.process(msg='test_msg',kwargs={})
        self.assertEqual(kwargs['extra']['logid'],lwl.logid_dict[current_thread().ident])
        
        # test_level
        test_logger=test_logger_level()
        lwl.logger=test_logger
        self.assertEqual(lwl.level,'level')
        
    def test_setup_logging(self):
        # test_setup_logging
        os.environ["APPBUILDER_LOGLEVEL"]="test" 
        with self.assertRaises(ValueError):
            _setup_logging()
                
        
            
if __name__ == '__main__':
    unittest.main()
        
        