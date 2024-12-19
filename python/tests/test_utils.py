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
import asyncio

from unittest.mock import MagicMock
from appbuilder.utils.sse_util import SSEClient,AsyncSSEClient, Event
from appbuilder.utils.model_util import RemoteModel,Models
from appbuilder.utils.logger_util import LoggerWithLoggerId,_setup_logging,logger
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
    
    def test_sse_util_AsyncSSEClient(self):
        async def mock_client():
            mock_event_source = MagicMock()
            mock_event_source.__iter__.return_value = iter([
                b'data: Test event 1\n\n',
                b'data: Last incomplete event'
            ])
            sse_client = AsyncSSEClient(mock_event_source)
            event_generator = sse_client._read()
            async for data in event_generator:
                pass

            # test_events
            mock_event_source.__aiter__.return_value = iter([
                b': Test event 1\n\n',
                b'test: Test event 2\n\n',
                b'data:Testevent3\n\n',
                b'data\n\n',
                b'event:Testevent5\n\n',
            ])
            sse_client = AsyncSSEClient(mock_event_source)
            async for event in sse_client.events():
                pass

        loop = asyncio.get_event_loop()
        loop.run_until_complete(mock_client())

    def test_sse_util_SSEClient_DEBUG(self):
        logger.setLoglevel("DEBUG")
        mock_event_source = MagicMock()
        mock_event_source.__iter__.return_value = iter(
            [b"data: Test event 1\n\n", b"data: Last incomplete event"]
        )
        sse_client = SSEClient(event_source=mock_event_source)
        event_generator = sse_client._read()
        self.assertEqual(next(event_generator), b"data: Test event 1\n\n")
        self.assertEqual(next(event_generator), b"data: Last incomplete event")
        # 测试是否抛出 StopIteration 异常，表示没有更多事件
        with self.assertRaises(StopIteration):
            next(event_generator)

        # test_events
        mock_event_source.__iter__.return_value = iter(
            [
                b": Test event 1\n\n",
                b"test: Test event 2\n\n",
                b"data:Testevent3\n\n",
                b"data\n\n",
                b"event:Testevent5\n\n",
            ]
        )
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


if __name__ == '__main__':
    unittest.main()
