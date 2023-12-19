import unittest
import pydantic
import os
import appbuilder


class TestAgentBase(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        pass

    def test_init_with_valid_component(self):
        """ 测试在component有效时运行 """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ernie-bot-4"
        )
        agent = appbuilder.AgentBase(component=component)
    
    def test_init_with_invalid_component(self):
        """ 测试在component非法时运行 """
        component = "invalid_component"
        with self.assertRaises(pydantic.error_wrappers.ValidationError):
            agent = appbuilder.AgentBase(component=component)

    def test_chat_with_valid_message_and_blocking(self):
        """ 测试在消息有效时处理 """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ernie-bot-4"
        )
        agent = appbuilder.AgentBase(component=component)
        message = appbuilder.Message({"query": "你好"})
        session_id = agent._generate_session_id()
        answer = agent.chat(message, session_id, stream=False)
        self.assertIs(type(answer.content), str)

    def test_chat_with_valid_message_and_streaming(self):
        """ 测试在消息有效时处理 """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ernie-bot-4"
        )
        agent = appbuilder.AgentBase(component=component)
        message = appbuilder.Message({"query": "你好"})
        session_id = agent._generate_session_id()
        answer = agent.chat(message, session_id, stream=True)
        for it in answer.content:
            self.assertIs(type(it), str)

if __name__ == '__main__':
    unittest.main()
