import unittest
import os
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestPlayground(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """

        self.model_name = "ERNIE-3.5-8K"
        self.play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model=self.model_name)

    def test_run_with_valid_message(self):
        """ 测试在消息有效时运行 """
        msg = appbuilder.Message({
            "name": "小明",
            "bot_name": "机器人",
            "bot_type": "聊天机器人",
            "bot_function": "聊天",
            "bot_question": "你好吗？"
        })

        answer = self.play.run(message=msg, stream=False, temperature=1)
        self.assertIsNotNone(answer)

    def test_run_with_invalid_message(self):
        """ 测试在消息无效时处理 """
        msg = appbuilder.Message({
            "name": "小明"
        })

        with self.assertRaises(ValueError):
            self.play.run(message=msg, stream=False, temperature=1)

    def test_run_with_string_message(self):
        """ 测试在消息为字符串时运行 """
        msg = appbuilder.Message("你好，小明。")

        self.play = appbuilder.Playground(prompt_template="你好，{name}。", model=self.model_name)
        answer = self.play.run(message=msg, stream=False, temperature=1)
        self.assertIsNotNone(answer)

    def test_run_with_stream_and_temperature(self):
        """测试运行时使用参数 stream 和 temperature"""
        msg = appbuilder.Message({
            "name": "小明",
            "bot_name": "机器人",
            "bot_type": "聊天机器人",
            "bot_function": "聊天",
            "bot_question": "你好吗？"
        })

        answer = self.play.run(message=msg, stream=True, temperature=0.5, top_p=0.2)

        for ans in answer.content:
            self.assertIsNotNone(ans)

    def test_run_with_max_output_tokens(self):
        """测试运行时使用参数 max_output_tokens 和 disable_search"""
        msg = appbuilder.Message({
            "name": "小明",
            "bot_name": "机器人",
            "bot_type": "聊天机器人",
            "bot_function": "聊天",
            "bot_question": "2023年北京昌平线地铁出轨事件发生在哪一天？"
        })

        answer = self.play.run(message=msg, stream=False, temperature=1, max_output_tokens=20, disable_search=False)
        print(answer)
        token_usage = answer.token_usage.get("completion_tokens",100)
        self.assertLessEqual(token_usage, 20)
    
    def test_run_with_extra_params(self):
        """测试运行时使用额外的参数"""
        msg = appbuilder.Message({
            "name": "小明",
            "bot_name": "机器人",
            "bot_type": "聊天机器人",
            "bot_function": "聊天",
            "bot_question": "2023年北京昌平线地铁出轨事件发生在哪一天？"
        })
        answer = self.play.run(message=msg, stream=False, temperature=1,system="你是北京市公安局刑事侦查支队的一名警员" )
        for ans in answer.content:
            self.assertIsNotNone(ans)


if __name__ == '__main__':
    unittest.main()
