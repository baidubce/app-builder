# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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
import sys
import asyncio
import os
import inspect


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestGetAppList(unittest.TestCase):

    def setUp(self):
        self.app_id = "aa8af334-df27-4855-b3d1-0d249c61fc08"

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_app_list_stdio(self):
        async def process():
            mcp_client = MCPClient()
            env = {"APPBUILDER_TOKEN": os.getenv("APPBUILDER_TOKEN")}
            await mcp_client.connect_to_server(
                inspect.getfile(app_server), env=env
            )
            tools = mcp_client.tools
            assert len(tools) > 0
            result = await mcp_client.call_tool("list_apps", {})
            print(result)
            assert result.content[0] != ""

        from appbuilder.mcp_server import MCPClient
        from appbuilder.mcp_server.app import app_server
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process())

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_app_run_stdio(self):
        async def process():
            mcp_client = MCPClient()
            env = {"APPBUILDER_TOKEN": os.getenv("APPBUILDER_TOKEN")}
            await mcp_client.connect_to_server(inspect.getfile(app_server), env=env)
            tools = mcp_client.tools
            assert len(tools) > 0
            create_conversation_result = await mcp_client.call_tool("create_conversation", {"app_id": self.app_id})
            conversation_id = create_conversation_result.content[0].text
            print(conversation_id)
            assert conversation_id is not None
            result = await mcp_client.call_tool("run", {
                "app_id": self.app_id,
                "conversation_id": conversation_id,
                "query": "北京的小学生数量",
                })
            answer = result.content[0].text
            print(answer)
            assert answer is not None

            await mcp_client.cleanup()

        from appbuilder.mcp_server import MCPClient
        from appbuilder.mcp_server.app import app_server

        loop = asyncio.get_event_loop()
        loop.run_until_complete(process())


if __name__ == "__main__":
    unittest.main()
