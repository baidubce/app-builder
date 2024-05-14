import unittest
import pydantic
import os
import appbuilder
from unittest.mock import MagicMock


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        pass

    def test_err_http(self):
        """ 测试http """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K",
            lazy_certification=True,
        )
        agent = appbuilder.AgentRuntime(component=component)
        app = agent.create_flask_app(url_rule="/chat")
        app.config['TESTING'] = True
        client = app.test_client()
        
        payload = {
            "message": {"query": "你好"},
            "stream": False
        }
        headers = {}
        response = client.post('/chat', json=payload, headers=headers)
        self.assertNotEqual(response.json.get('code'), 0)
        

    def test_http(self):
        """ 测试http """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="ERNIE-3.5-8K",
            lazy_certification=True,
        )
        agent = appbuilder.AgentRuntime(component=component)
        app = agent.create_flask_app(url_rule="/chat")
        app.config['TESTING'] = True
        client = app.test_client()
        
        payload = {
            "message": {"query": "你好"},
            "stream": False
        }
        headers = {
            "X-Appbuilder-Authorization": os.environ.get("APPBUILDER_TOKEN", ""),
            "X-Appbuilder-Token": os.environ.get("APPBUILDER_TOKEN", "")
        }
        response = client.post('/chat', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get('code'), 0)
        
    def test_init_with_valid_component(self):
        """ 测试在component有效时运行 """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = appbuilder.AgentRuntime(component=component)
    
    def test_init_with_invalid_component(self):
        """ 测试在component非法时运行 """
        component = "invalid_component"
        with self.assertRaises(pydantic.ValidationError):
            agent = appbuilder.AgentRuntime(component=component)

    def test_chat_with_valid_message_and_blocking(self):
        """ 测试在消息有效时处理 """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = appbuilder.AgentRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        answer = agent.chat(message, stream=False)
        self.assertIs(type(answer.content), str)

    def test_chat_with_valid_message_and_streaming(self):
        """ 测试在消息有效时处理 """
        component = appbuilder.Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = appbuilder.AgentRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        answer = agent.chat(message, stream=True)
        for it in answer.content:
            self.assertIs(type(it), str)

if __name__ == '__main__':
    unittest.main()
