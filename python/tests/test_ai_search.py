import unittest
import appbuilder
import os


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAgentRuntime(unittest.TestCase):

    def test_base_search(self):
        client = appbuilder.AISearch()
        messages = [
            {
                "role": "user",
                "content": "请帮我写一个Python程序，实现斐波那契数列的输出。",
            }
        ]
        msg = client.run(messages=messages)
        assert msg.content is not None
    
    def test_ai_search(self):
        client = appbuilder.AISearch()
        messages = [
            {
                "role": "user",
                "content": "请帮我写一个Python程序，实现斐波那契数列的输出。",
            }
        ]
        msg = client.run(messages=messages, model="ernie-3.5-8k")
        assert msg.content is not None


if __name__ == "__main__":
    unittest.main()
