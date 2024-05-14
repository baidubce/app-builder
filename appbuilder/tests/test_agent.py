import os
import unittest
import pydantic
import appbuilder
from appbuilder.core.component import Component
from appbuilder import (
    AgentRuntime,
    Message,
    Playground,
)


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
        self.app_id = "aa8af334-df27-4855-b3d1-0d249c61fc08"

    def test_init_with_valid_component(self):
        """ 测试在component有效时运行 """
        component = Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = AgentRuntime(component=component)

    def test_init_with_invalid_component(self):
        """ 测试在component非法时运行 """
        component = "invalid_component"
        with self.assertRaises(pydantic.ValidationError):
            agent = AgentRuntime(component=component)

    def test_chat_with_valid_message_and_blocking(self):
        """ 测试在消息有效时处理 """
        component = Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = appbuilder.AgentRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        answer = agent.chat(message, stream=False)
        self.assertIs(type(answer.content), str)

    def test_chat_with_valid_message_and_streaming(self):
        """ 测试在消息有效时处理 """
        component = Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = AgentRuntime(component=component)
        message = Message({"query": "你好"})
        answer = agent.chat(message, stream=True)
        for it in answer.content:
            self.assertIs(type(it), str)

    def test_chainlit_agent_component_error(self):
        """ 测试chainlit agent组件错误 """
        component = Component()
        agent = AgentRuntime(component=component)
        with self.assertRaises(ValueError):
            agent.chainlit_agent()


if __name__ == '__main__':
    unittest.main()
