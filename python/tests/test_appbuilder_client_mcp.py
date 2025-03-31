import unittest
import appbuilder
import os
import sys
import subprocess
import asyncio

from appbuilder.core.console.appbuilder_client.async_event_handler import (
    AsyncToolCallEventHandler,
)


@appbuilder.manifest(
    description="获取指定中国城市的当前天气信息。仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。"
)
@appbuilder.manifest_parameter(
    name="location", description="城市名，例如：北京。"
)
@appbuilder.manifest_parameter(
    name="unit", description="温度单位，支持 'celsius' 或 'fahrenheit'"
)
def get_current_weather(location: str, unit: str) -> str:
    return "北京今天25度"


functions = [get_current_weather]


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderClientMCP(unittest.TestCase):
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
    def test_appbuilder_client_mcp(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败

        Args:
            self (unittest.TestCase): unittest的TestCase对象

        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """

        async def process():
            tools = [appbuilder.Manifest.from_function(f) for f in functions]
            mcp_client = MCPClient()
            await mcp_client.connect_to_server("./data/mcp_component_server_sample.py")
            tools.extend(mcp_client.tools)

            appbuilder_client = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await appbuilder_client.create_conversation()

            event_handler = AsyncToolCallEventHandler(
                mcp_client, functions=functions)
            with await appbuilder_client.run_with_handler(
                conversation_id=conversation_id,
                query="北京的天气怎么样",
                tools=tools,
                event_handler=event_handler,
                stream=False,
            ) as run:
                await run.until_done()

            with await appbuilder_client.run_with_handler(
                conversation_id=conversation_id,
                query="翻译hello world为中文",
                tools=tools,
                event_handler=event_handler,
                stream=True,
            ) as run:
                await run.until_done()
            

            await appbuilder_client.http_client.session.close()
            await mcp_client.cleanup()

        from appbuilder.mcp_server.client import MCPClient
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process())


if __name__ == "__main__":
    appbuilder.logger.setLoglevel("DEBUG")
    unittest.main()
