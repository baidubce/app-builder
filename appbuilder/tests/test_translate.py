import unittest
import appbuilder
from appbuilder.core._exception import InvalidRequestArgumentError
import os

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestTranslationComponent(unittest.TestCase):
    def setUp(self):
        self.translation = appbuilder.Translation()

    def test_run_valid_request(self):
        """测试 run 方法对有效请求的处理。"""
        msg = appbuilder.Message(content="你好")
        result = self.translation(msg)
        self.assertEqual(result.content['from_lang'], 'zh')
        self.assertEqual(result.content['to_lang'], 'en')

    def test_run_invalid_request(self):
        """测试 run 方法对无效请求的处理。"""
        msg = appbuilder.Message(content="")
        with self.assertRaises(ValueError):
            _ = self.translation(msg)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        result = self.translation.tool_eval(name="translation", streaming=True, q="你好\n中国", to_lang="en")
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(InvalidRequestArgumentError):
            result = self.translation.tool_eval(name="translation", streaming=True, to_lang="en")
            next(result)


if __name__ == '__main__':
    unittest.main()
