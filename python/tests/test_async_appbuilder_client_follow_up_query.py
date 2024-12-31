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
import os
import asyncio
import appbuilder
from appbuilder.core.console.appbuilder_client.async_event_handler import (
    AsyncAppBuilderEventHandler,
)


class MyEventHandler(AsyncAppBuilderEventHandler):
    def __init__(self):
        super().__init__()
        self.follow_up_queries = []

    async def handle_content_type(self, run_context, run_response):
        event = run_response.events[-1]
        if event.content_type == "json" and event.event_type == "FollowUpQuery":
            follow_up_queries = event.detail.get("json").get("follow_up_querys")
            self.follow_up_queries.extend(follow_up_queries)


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderClientAsync(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "fb64d96b-f828-4385-ba1d-835298d635a9"

    def test_async_run_stream(self):
        appbuilder.logger.setLoglevel("ERROR")
        async def agent_handle():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            event_handler = MyEventHandler()
            with await client.run_with_handler(
                conversation_id = conversation_id,
                query = "你能做什么",
                stream=True,
                event_handler=event_handler,
            ) as run:
                await run.until_done()

            print(event_handler.follow_up_queries)
            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_handle())

if __name__ == "__main__":
    unittest.main()
