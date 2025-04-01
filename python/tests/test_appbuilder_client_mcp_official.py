import unittest
import appbuilder
import os
import sys
import subprocess
import asyncio


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "b2a972c5-e082-46e5-b313-acbf51792422"

    @unittest.skipIf(sys.version_info < (3, 10), "Only for Python >= 3.10")
    def test_appbuilder_client_mcp_official(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败

        Args:
            self (unittest.TestCase): unittest的TestCase对象

        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """
        async def process(mcp_client):
            client = appbuilder.AppBuilderClient(self.app_id)
            conversation_id = client.create_conversation()

            await mcp_client.connect_to_server("./data/mcp_official_server_sample.py")
            msg = client.run(
                conversation_id=conversation_id,
                query="latitude:51.5，longtitude:-0.12",
                tools=mcp_client.tools,
            )

            event = msg.content.events[-1]
            assert event.status == "interrupt"
            assert event.event_type == "Interrupt"

            print(
                "\033[1;31m",
                "Agent思考过程：\n{}\n".format(
                    msg.content.events[-1].model_dump_json(indent=4)
                ),
                "\033[0m",
            )

            tool_call = msg.content.events[-1].tool_calls[-1]
            tool_call_id = tool_call.id
            tool_call_arg = tool_call.function.arguments

            print("\033[1;32m", "MCP参数:{}\n".format(tool_call_arg), "\033[0m")
            mcp_server_result = await mcp_client.session.call_tool(
                name=tool_call.function.name, arguments=tool_call.function.arguments
            )
            print("\033[1;33m", "MCP结果: {}\n".format(mcp_server_result))
            msg_2 = client.run(
                conversation_id=conversation_id,
                tool_outputs=[{
                    "tool_call_id": tool_call_id,
                    "output": mcp_server_result.content[0].text
                }]
            )
            print(
                "\033[1;34m",
                "Agent 最终结果:{}".format(msg_2.content.answer),
                "\033[0m",
            )

        async def handler():
            mcp_client = MCPClient()
            try:
                await process(mcp_client)
            finally:
                await mcp_client.cleanup()

        from appbuilder.mcp_server.client import MCPClient
        loop = asyncio.get_event_loop()
        loop.run_until_complete(handler())


if __name__ == "__main__":
    unittest.main()
