import unittest
import appbuilder
import os
import sys
import subprocess
import asyncio

from appbuilder.core.console.appbuilder_client.async_event_handler import (
    AsyncAppBuilderEventHandler,
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

class MyEventHandler(AsyncAppBuilderEventHandler):
    def __init__(self, mcp_client):
        super().__init__()
        self.mcp_client = mcp_client

    async def interrupt(self, run_context, run_response):  
        thought = run_context.current_thought
        print("\033[1;31m", "-> Agent 中间思考: ", thought, "\033[0m")

        tool_output = []
        for tool_call in run_context.current_tool_calls:
            function_name = tool_call.function.name
            function_arguments = tool_call.function.arguments
            result = ""
            function_map = {f.__name__: f for f in functions}
            if function_name in function_map:
                result = function_map[function_name](**tool_call.function.arguments)
                print("\033[1;33m", "本地function结果: {}\n\033[0m".format(result))
            else:
                print("\033[1;32m","MCP工具名称: {}, MCP参数:{}\n".format(function_name, function_arguments),"\033[0m")
                mcp_server_result = await self.mcp_client.call_tool(
                    function_name, function_arguments
                )
                print("\033[1;33m", "MCP结果: {}\n\033[0m".format(mcp_server_result))
                index = 0
                for i, content in enumerate(mcp_server_result.content):
                    if content.type == "text":
                        index = i
                        result = result + mcp_server_result.content[index].text    
            tool_output.append(
                {
                    "tool_call_id": tool_call.id,
                    "output": result,
                }
            )
        return tool_output

    async def success(self, run_context, run_response):
        print("\n\033[1;34m", "-> Agent 非流式回答: ", run_response.answer, "\033[0m")


# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
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

        async def agent_run(client, mcp_client, query):
            conversation_id = await client.create_conversation()
            tools = [appbuilder.Manifest.from_function(f) for f in functions]
            tools.extend(mcp_client.tools)
            with await client.run_with_handler(
                conversation_id=conversation_id,
                query=query,
                tools=tools,
                event_handler=MyEventHandler(mcp_client),
            ) as run:
                await run.until_done()

        async def handler():
            mcp_client = MCPClient()
            appbuilder_client = appbuilder.AsyncAppBuilderClient(self.app_id)
            try:
                await mcp_client.connect_to_server(
                    "./data/mcp_official_server_sample.py"
                )
                await agent_run(appbuilder_client, mcp_client, "北京的天气怎么样")
                await agent_run(appbuilder_client, mcp_client, "美国马萨诸塞州的天气")
            finally:
                await appbuilder_client.http_client.session.close()
                await mcp_client.cleanup()

        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "-y", "chainlit"]
        )
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mcp"])
        from appbuilder.modelcontextprotocol.client import MCPClient

        loop = asyncio.get_event_loop()
        loop.run_until_complete(handler())


if __name__ == "__main__":
    unittest.main()
