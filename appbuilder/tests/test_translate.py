import unittest
import appbuilder


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


if __name__ == '__main__':
    unittest.main()
