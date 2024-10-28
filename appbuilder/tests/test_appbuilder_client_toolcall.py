import unittest
import appbuilder
import requests
import tempfile
import os


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
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
        client = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = client.create_conversation()
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

        msg = client.run(
            conversation_id=conversation_id,
            query="今天北京天气怎么样？",
            tools=tools)
        print(msg.model_dump_json(indent=4))

        event = msg.content.events[-1]
        assert event.status == "interrupt"
        assert event.event_type == "Interrupt"

        msg_2 = client.run(
            conversation_id=conversation_id,
            tool_outputs=[
                {
                    "tool_call_id": event.tool_calls[-1].id,
                    "output": "北京今天35度"
                }
            ]
        )
        print(msg_2.model_dump_json(indent=4))


        """测试functions2tools功能"""
        #定义本地函数
        def get_current_weather(location: str, unit: str) -> str:
            """
            查询指定中国城市的当前天气。

            参数:
                location (str): 城市名称，例如："北京"
                unit (str): 温度单位，可选 "celsius" 或 "fahrenheit"

            返回:
                str: 天气情况描述

            抛出:
                ValueError: 如果传入的城市不支持或单位不正确
            """
            return "北京今天25度"
        #定义函数列表
        functions = [get_current_weather]
        function_map = {f.__name__: f for f in functions}
        #调用大模型
        msg = client.run(
        conversation_id=conversation_id,
        query="今天北京的天气怎么样？",
        tools = [appbuilder.function_to_json(f) for f in functions]
        )
        print(msg.model_dump_json(indent=4))
        # 获取最后的事件和工具调用信息
        event = msg.content.events[-1]
        tool_call = event.tool_calls[-1]

        # 获取函数名称和参数
        name = tool_call.function.name
        args = tool_call.function.arguments

        # 将函数名称映射到具体的函数并执行
        raw_result = function_map[name](**args)

        # 传递工具的输出
        msg_2 = client.run(
            conversation_id=conversation_id,
            tool_outputs=[{
                "tool_call_id": tool_call.id,
                "output": str(raw_result)
            }],
        )
        print(msg_2.model_dump_json(indent=4))      

if __name__ == '__main__':
    unittest.main()
