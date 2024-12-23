import unittest
import uuid

import requests

import appbuilder
from appbuilder.core._exception import InvalidRequestArgumentError
from appbuilder.core.components.asr.model import ShortSpeechRecognitionRequest, ShortSpeechRecognitionResponse
import os

@unittest.skip("测试API超限，暂时跳过")
class TestASRComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.audio_file_url = "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                              "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                              "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
        self.audio_speech_too_long_url = ("https://bj.bcebos.com/v1/agi-dev-platform-sdk-test/speech_too_long.wav?"
                                          "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-07-01T03%3A41%3A00Z%2F300%2Fhost%2Febd71063a7ada87a722a6c9a801d95bd41f75f363236623882586ac9d37e7665")
        self.asr = appbuilder.ASR()

    def test_run(self):
        """
        使用原始语音文件进行单测

        Args:
            None

        Returns:
            None

        """
        raw_audio = requests.get(self.audio_file_url).content
        inp = appbuilder.Message(content={"raw_audio": raw_audio})
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
        raw_audio = requests.get(self.audio_file_url).content
        inp = appbuilder.Message(content={"raw_audio": raw_audio})
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
        raw_audio = requests.get(self.audio_file_url).content
        request = ShortSpeechRecognitionRequest()
        request.format = 'pcm'
        request.rate = 16000
        request.cuid = str(uuid.uuid4())
        request.dev_pid = "80001"
        request.speech = raw_audio
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
            self.asr._check_service_error("", data)
        data = {'err_msg': 'No Error', 'err_no': 0}
        self.assertIsNone(self.asr._check_service_error("", data))

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        result = self.asr.tool_eval(name="asr", streaming=True, file_url=self.audio_file_url)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(InvalidRequestArgumentError):
            result = self.asr.tool_eval(name="asr", streaming=True)
            next(result)

    def test_tool_eval_speech_too_long(self):
        """测试 tool 方法对有效请求的处理。"""
        result = self.asr.tool_eval(name="asr", streaming=True, file_url=self.audio_speech_too_long_url)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)


if __name__ == '__main__':
    unittest.main()
