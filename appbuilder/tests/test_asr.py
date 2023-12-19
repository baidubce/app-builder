import unittest
import os
import uuid

import appbuilder
from appbuilder.core.components.asr.model import ShortSpeechRecognitionRequest, ShortSpeechRecognitionResponse


class TestASRComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.asr = appbuilder.ASR()

    def test_run(self):
        """
        使用原始语音文件进行单测

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        asr_path = os.path.join(current_dir, 'asr_test.pcm')

        with open(asr_path, "rb") as f:
            inp = appbuilder.Message(content={"raw_audio": f.read()})
            out = self.asr.run(inp)
            self.assertIsNotNone(out)
            self.assertIsInstance(out, appbuilder.Message)
            self.assertIn('result', out.content)

    def test_run_different_rate(self):
        """
        使用不同rate进行单测

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        asr_path = os.path.join(current_dir, 'asr_test.pcm')

        with open(asr_path, "rb") as f:
            inp = appbuilder.Message(content={"raw_audio": f.read()})
            try:
                out = self.asr.run(inp, rate=8000)
                self.assertIsNotNone(out)
                self.assertIsInstance(out, appbuilder.Message)
            except appbuilder.AppBuilderServerException as ex:
                self.assertIsNotNone(ex, "请求捕获到异常")

    def test_run_invalid_audio(self):
        """
        使用非法语音文件进行单测

        Args:
            None

        Returns:
            None

        """
        inp = appbuilder.Message(content={"raw_audio": b"invalid"})
        with self.assertRaises(Exception):
            self.asr.run(inp)

    def test_recognition(self):
        """
        recognition方法单测

        Args:
            None

        Returns:
            None

        """

        current_dir = os.path.dirname(__file__)
        asr_path = os.path.join(current_dir, 'asr_test.pcm')

        with open(asr_path, "rb") as f:
            request = ShortSpeechRecognitionRequest()
            request.format = 'pcm'
            request.rate = 16000
            request.cuid = str(uuid.uuid4())
            request.dev_pid = "80001"
            request.speech = f.read()
            response = self.asr._recognize(request)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, ShortSpeechRecognitionResponse)

    def test_recognition_invalid_request(self):
        """
        recognition方法单测，非法请求体

        Args:
            None

        Returns:
            None

        """
        with self.assertRaises(Exception):
            self.asr._recognize(None)

    def test_check_service_error(self):
        """
        check_service_error方法单测

        Args:
            None

        Returns:
            None

        """
        data = {'err_msg': 'Error', 'err_no': 1}
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.asr._check_service_error(data)
        data = {'err_msg': 'No Error', 'err_no': 0}
        self.assertIsNone(self.asr._check_service_error(data))


if __name__ == '__main__':
    unittest.main()
