import unittest
import os
import requests

import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestDishRecognitionComponent(unittest.TestCase):
    def setUp(self):
        """
        在开始测试之前配置环境和实例化DishRecognition对象。

        Args:
            None

        Returns:
            None

        """
        self.dish_recognition = appbuilder.DishRecognition()

    def test_run_with_valid_image(self):
        """
        测试run函数在传入有效图像的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        image_url = "https://bj.bcebos.com/v1/appbuilder/dish_recognize_test.jpg?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T" \
                    "10%3A58%3A25Z%2F-1%2Fhost%2F7b8fc08b2be5adfaeaa4e3a0bb0d1a1281b10da" \
                    "3d6b798e116cce3e37feb3438"
        raw_image = requests.get(image_url).content
        message = appbuilder.Message({"raw_image": raw_image})
        output_message = self.dish_recognition(message=message)
        self.assertIsInstance(output_message, appbuilder.Message)

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
            message = appbuilder.Message({"raw_image": f.read()})
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
        image_url = "https://bj.bcebos.com/v1/appbuilder/dish_recognize_test.jpg?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T" \
                    "10%3A58%3A25Z%2F-1%2Fhost%2F7b8fc08b2be5adfaeaa4e3a0bb0d1a1281b10da" \
                    "3d6b798e116cce3e37feb3438"
        message = appbuilder.Message({"url": image_url})
        output_message = self.dish_recognition(message=message)
        self.assertIsInstance(output_message, appbuilder.Message)

    def test_run_with_invalid_url(self):
        """
        测试run函数在传入无效URL的情况下的行为。

        Args:
            None

        Returns:
            None

        """
        url = "http://example.com/invalid_url.jpg"
        message = appbuilder.Message({"url": url})
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
        message = appbuilder.Message({})
        with self.assertRaises(ValueError):
            self.dish_recognition(message=message)


if __name__ == "__main__":
    unittest.main()
