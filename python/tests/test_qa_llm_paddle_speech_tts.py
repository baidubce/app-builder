# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import os
import unittest
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestPaddleSpeechTTS(unittest.TestCase):
    def test_normal_case(self):
        text = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性"
        tts_model = "paddlespeech-tts"
        audio_type = "wav"
        
        # Setup
        tts = appbuilder.TTS()
        inp = appbuilder.Message(content={"text": text})
        param_dict = {
            "model": tts_model,
            "audio_type": audio_type,
        }
        
        out = tts.run(inp, **param_dict)
        self.assertGreaterEqual(len(out.content["audio_binary"]), 0)


if __name__ == '__main__':
    unittest.main()
