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
import asyncio
import unittest
import appbuilder
from appbuilder.core.console.appbuilder_client.async_event_handler import (
    AsyncAppBuilderEventHandler,
)


class MyEventHandler(AsyncAppBuilderEventHandler):
    def __init__(self):
        super().__init__()
        self.interrupt_ids = []

    async def handle_content_type(self, run_context, run_response):
        interrupt_event_id = None
        event = run_response.events[-1]
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
        if interrupt_event_id is not None:
            self.interrupt_ids.append(interrupt_event_id)

    def _create_action(self):
        if len(self.interrupt_ids) == 0:
            return None
        event_id = self.interrupt_ids.pop()
        return {
            "action_type": "resume",
            "parameters": {"interrupt_event": {"id": event_id, "type": "chat"}},
        }

    async def run(self, query=None):
        await super().new_dialog(
            query=query,
            action=self._create_action(),
        )

    def gen_action(self):
        while True:
            yield self._create_action()


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderClientChatflow(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "4403205e-fb83-4fac-96d8-943bdb63796f"

    def test_chatflow(self):
        appbuilder.logger.setLoglevel("DEBUG")

        async def agent_handle():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            event_handler = MyEventHandler()
            await event_handler.init(
                appbuilder_client=client,
                conversation_id=conversation_id,
                stream=False,
                query="查天气",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="查航班",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="CA1234",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="北京的",
            )
            async for data in event_handler:
                pass

            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_handle())

    def test_chatflow_stream(self):
        appbuilder.logger.setLoglevel("DEBUG")

        async def agent_handle():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            event_handler = MyEventHandler()
            await event_handler.init(
                appbuilder_client=client,
                conversation_id=conversation_id,
                stream=True,
                query="查天气",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="查航班",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="CA1234",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="北京的",
            )
            async for data in event_handler:
                pass

            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_handle())

    def test_chatflow_stream(self):
        appbuilder.logger.setLoglevel("DEBUG")

        async def agent_handle():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            event_handler = MyEventHandler()
            await event_handler.init(
                appbuilder_client=client,
                conversation_id=conversation_id,
                stream=True,
                query="查天气",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="查航班",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="CA1234",
            )
            async for data in event_handler:
                pass
            await event_handler.run(
                query="北京的",
            )
            async for data in event_handler:
                pass

            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_handle())
    
    def test_chatflow_multiple_dialog(self):
        appbuilder.logger.setLoglevel("DEBUG")

        async def agent_handle():
            client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await client.create_conversation()
            queries = ["查天气", "查航班", "CA1234", "北京的"]
            event_handler = MyEventHandler()
            event_handler = client.run_multiple_dialog_with_handler(
                    conversation_id=conversation_id,
                    queries=queries,
                    event_handler=event_handler,
                    stream=False,
                    actions=event_handler.gen_action(),
                )
            async for data in event_handler:
                async for answer in data:
                    print(answer)

            await client.http_client.session.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(agent_handle())


if __name__ == "__main__":
    unittest.main()
