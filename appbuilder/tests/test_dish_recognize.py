import unittest
import os

import appbuilder
from appbuilder.core.message import Message
from appbuilder.core.components.dish_recognize.component import DishRecognition


class TestDishRecognitionComponent(unittest.TestCase):
    def setUp(self):
        """
        在开始测试之前配置环境和实例化DishRecognition对象。

        Args:
            None

        Returns:
            None

        """
        self.dish_recognition = DishRecognition()

    def test_run_with_valid_image(self):
        """
        测试run函数在传入有效图像的情况下的行为。

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'dish_recognize_test.jpg')

        with open(file_path, "rb") as f:
            message = Message({"raw_image": f.read()})
            output_message = self.dish_recognition(message=message)
            self.assertIsInstance(output_message, Message)

    def test_run_with_invalid_image(self):
        """
        测试run函数在传入无效图像的情况下的行为。

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'test_translate.py')

        with open(file_path, "rb") as f:
            message = Message({"raw_image": f.read()})
            with self.assertRaises(appbuilder.AppBuilderServerException):
                self.dish_recognition(message=message)

    def test_run_with_valid_url(self):
        """
        测试run函数在传入有效URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        url = "https://img1.baidu.com/it/u=858635807,3718531454&fm=253&fmt=auto&app=138&f=PNG?w=500&h=333"
        message = Message({"url": url})
        output_message = self.dish_recognition(message=message)
        self.assertIsInstance(output_message, Message)

    def test_run_with_invalid_url(self):
        """
        测试run函数在传入无效URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        url = "http://example.com/invalid_url.jpg"
        message = Message({"url": url})
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.dish_recognition(message=message)

    def test_run_without_image_and_url(self):
        """
        测试run 函数在没有传入图像和URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        message = Message({})
        with self.assertRaises(ValueError):
            self.dish_recognition(message=message)


if __name__ == "__main__":
    unittest.main()
