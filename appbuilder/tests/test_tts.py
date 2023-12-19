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
import os
import appbuilder


class TestTTS(unittest.TestCase):
    def setUp(self):
        self.tts = appbuilder.TTS()
        self.text_message = appbuilder.Message(content={"text": "欢迎使用语音合成"})

    def test_model_validation(self):
        with self.assertRaises(ValueError):
            self.tts.run(self.text_message, model="invalid_model")

    def test_text_validation(self):
        empty_message = appbuilder.Message(content={})
        with self.assertRaises(ValueError):
            self.tts.run(empty_message)

    def test_audio_type_validation_baidu_tts(self):
        with self.assertRaises(ValueError):
            self.tts.run(self.text_message, model="baidu-tts", audio_type="flac")

    def test_audio_type_validation_paddlespeech_tts(self):
        with self.assertRaises(ValueError):
            self.tts.run(self.text_message, model="paddlespeech-tts", audio_type="mp3")

    def test_run_baidu_tts(self):
        out = self.tts.run(self.text_message, model="baidu-tts", audio_type="wav")
        self.assertTrue("audio_binary" in out.content and "audio_type" in out.content)

    def test_run_paddlespeech_tts(self):
        out = self.tts.run(self.text_message, model="paddlespeech-tts", audio_type="wav")
        self.assertTrue("audio_binary" in out.content and "audio_type" in out.content)


if __name__ == "__main__":
    unittest.main()
