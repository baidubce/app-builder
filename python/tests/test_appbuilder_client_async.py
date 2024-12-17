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
import inspect
import appbuilder


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

        async def agent_run(client, conversation_id, text):
            ans = await client.run(conversation_id, text, stream=True)
            async for data in ans.content:
                print(data)

        async def agent_sample():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            task1 = asyncio.create_task(
                agent_run(client, conversation_id, "最早的邮展"))
            task2 = asyncio.create_task(
                agent_run(client, conversation_id, "最早的漫展"))
            await asyncio.gather(task1, task2)
            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_sample())

    def test_async_run(self):
        appbuilder.logger.setLoglevel("ERROR")

        async def agent_run(client, conversation_id, text):
            ans = await client.run(conversation_id, text, stream=False)
            print(ans.content.answer)

        async def agent_sample():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            task1 = asyncio.create_task(
                agent_run(client, conversation_id, "最早的邮展"))
            task2 = asyncio.create_task(
                agent_run(client, conversation_id, "最早的漫展"))
            await asyncio.gather(task1, task2)
            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_sample())


if __name__ == "__main__":
    unittest.main()
