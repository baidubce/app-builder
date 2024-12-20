# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import appbuilder
from appbuilder.core._exception import InvalidRequestArgumentError
import os

@unittest.skip("测试API超限，暂时跳过")
class TestTTS(unittest.TestCase):
    def setUp(self):
        self.tts = appbuilder.TTS()
        self.text_message = appbuilder.Message(content={"text": """随着科技的迅速发展"""})

    def test_model_validation(self):
        with self.assertRaises(InvalidRequestArgumentError):
            self.tts.run(self.text_message, model="invalid_model")

    def test_text_validation(self):
        empty_message = appbuilder.Message(content={})
        with self.assertRaises(BaseException):
            self.tts.run(empty_message)

    def test_audio_type_validation_baidu_tts(self):
        with self.assertRaises(InvalidRequestArgumentError):
            self.tts.run(self.text_message, model="baidu-tts", audio_type="flac")

    def test_audio_type_validation_paddlespeech_tts(self):
        with self.assertRaises(InvalidRequestArgumentError):
            self.tts.run(self.text_message, model="paddlespeech-tts", audio_type="mp3")

    def test_run_baidu_tts(self):
        out = self.tts.run(self.text_message, model="baidu-tts", audio_type="wav")
        self.assertTrue("audio_binary" in out.content and "audio_type" in out.content)

    def test_run_paddlespeech_tts(self):
        out = self.tts.run(self.text_message, model="paddlespeech-tts", audio_type="wav")
        self.assertTrue("audio_binary" in out.content and "audio_type" in out.content)

    def test_run_paddlespeech_tts_stream(self):
        out = self.tts.run(self.text_message, model="paddlespeech-tts", audio_type="pcm", stream=True)
        for o in out:
            self.assertIsNotNone(o)

    def test_run_error_model_tts_stream(self):
        with self.assertRaises(InvalidRequestArgumentError):
            self.tts.run(self.text_message, model="baidu-tts", audio_type="pcm", stream=True)

    def test_run_paddlespeech_validation_tts_stream(self):
        with self.assertRaises(InvalidRequestArgumentError):
            self.tts.run(self.text_message, model="paddlespeech-tts", audio_type="mp3", stream=True)
            
    def test_run_raise_text_field_empty(self):
        message=appbuilder.Message(content={"text": ""})
        with self.assertRaises(InvalidRequestArgumentError):
            self.tts.run(message)


if __name__ == "__main__":
    unittest.main()
