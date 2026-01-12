import unittest
import appbuilder
import os


# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAgentRuntime(unittest.TestCase):

    def test_base_search_stream(self):
        client = appbuilder.AISearch()
        messages = [
            {
                "role": "user",
                "content": "请帮我写一个Python程序，实现斐波那契数列的输出。",
            }
        ]
        msg = client.run(messages=messages, stream=True)
        for data in msg.content:
            print(data)
    
    def test_ai_search_stream(self):
        client = appbuilder.AISearch()
        messages = [
            {
                "role": "user",
                "content": "请帮我写一个Python程序，实现斐波那契数列的输出。",
            }
        ]
        msg = client.run(messages=messages, model="deepseek-v3.1-250821", stream=True)
        for data in msg.content:
            print(data)


if __name__ == "__main__":
    unittest.main()
