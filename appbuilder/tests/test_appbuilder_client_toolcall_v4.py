import unittest
import appbuilder
import requests
import tempfile
import os
from appbuilder.core.console.appbuilder_client.event_handler import AppBuilderEventHandler

class MyEventHandler(AppBuilderEventHandler):
    def get_current_weather(self, location=None, unit="celsius"):
        return "{} 的温度是 {} {}".format(location, 20, unit)
    
    def tool_calls(self, run_context, run_response):
        tool_output = []
        for tool_call in run_context.current_tool_calls:
            tool_call_id = tool_call.id
            tool_res = self.get_current_weather(
                **tool_call.function.arguments)
            tool_output.append(
                {
                    "tool_call_id": tool_call_id,
                    "output": tool_res
                }
            )
        return tool_output
    
    def run_end(self, run_context, run_response):
        print(run_response.content.answer)
        


# appbuilder.logger.setLoglevel("DEBUG")
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-vGrDN4BvjP15rDrXBI9OC/6d435ece62ed09b396e1b051bd87869c11861332"
os.environ["GATEWAY_URL_V2"] = "https://apaas-api-sandbox.baidu-int.com"

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "4d4b1b27-d607-4d2a-9002-206134217a9f"

    def test_appbuilder_client_tool_call(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
    
        Args:
            self (unittest.TestCase): unittest的TestCase对象
    
        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "仅支持中国城市的天气查询，参数location为中国城市名称，其他国家城市不支持天气查询",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市名，举例：北京",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location", "unit"],
                    },
                },
            }
        ]

        cities = ["北京", "上海", "广州"]
        query = "下面这些城市的天气怎么样：{}".format(",".join(cities))

        with builder.run_with_handler(
            conversation_id = conversation_id,
            query = query,
            tools = tools,
            event_handler = MyEventHandler(),
        ) as run:
            run.until_done()

        
if __name__ == '__main__':
    unittest.main()
