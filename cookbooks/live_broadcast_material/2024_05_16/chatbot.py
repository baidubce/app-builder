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
import time
import wave
import sys
import pyaudio
import webrtcvad
import appbuilder
import re

os.environ["APPBUILDER_TOKEN"] = "密钥"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 16000
DURATION = 30  # ms
CHUNK = RATE // 1000 * DURATION


class Chatbot:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.tts = appbuilder.TTS()
        self.asr = appbuilder.ASR()
        self.agent = appbuilder.AppBuilderClient("应用iD")

    def run(self):
        self.run_tts_and_play_audio("我是你的专属聊天机器人，小智，如果你有什么问题，可以直接问我")
        while True:
            print("loop...")
            audio_path = "output.wav"
            # 记录音频，如果语音时长小于1秒，则忽略本次对话
            print("开始记录音频...")
            if self.record_audio(audio_path) < 1000:
                time.sleep(1)
                continue
            print("音频记录结束")
            # 音频转文本
            print("开始执行ASR...")
            query = self.run_asr(audio_path)
            print("结束执行ASR")
            # 询问智能体
            print("正在执行智能体...")
            if len(query) == 0:
                continue
            answer = self.run_agent(query)
            results = re.findall(r'(https?://[^\s]+)', answer)
            for result in results:
                print("链接地址:", result)
                answer = answer.replace(result, "")
            print("answer:", answer)
            print("结束调用智能体")
            # 文本转语音
            print("开始执行TTS并播报...")
            self.run_tts_and_play_audio(answer)
            print("结束TTS并播报结束")

    def record_audio(self, path):
        with (wave.open(path, 'wb') as wf):
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
            vad = webrtcvad.Vad(1)
            not_speech_times = 0
            speech_times = 0
            total_times = 0
            start_up_times = 33 * 5  # 初始时间设置为5秒
            history_speech_times = 0
            while True:
                if history_speech_times > 33 * 10:
                    break
                data = stream.read(CHUNK, False)
                if vad.is_speech(data, RATE):
                    speech_times += 1
                    wf.writeframes(data)
                else:
                    not_speech_times += 1
                total_times += 1
                if total_times >= start_up_times:
                    history_speech_times += speech_times
                    # 模拟滑窗重新开始计数
                    if float(not_speech_times) / float(total_times) > 0.7:
                        break
                    not_speech_times = 0
                    speech_times = 0
                    total_times = 0
                    start_up_times = start_up_times / 2
                    if start_up_times < 33:
                        start_up_times = 33
            stream.close()
            return history_speech_times * DURATION

    def run_tts_and_play_audio(self, text: str):
        msg = self.tts.run(appbuilder.Message(content={"text": text}), audio_type="pcm", model="paddlespeech-tts",
                           stream=True)
        stream = self.p.open(format=self.p.get_format_from_width(2),
                             channels=1,
                             rate=24000,
                             output=True,
                             frames_per_buffer=2048)
        for pcm in msg.content:
            stream.write(pcm)
        stream.stop_stream()
        stream.close()

    def run_asr(self, audio_path: str):
        with open(audio_path, "rb") as f:
            content_data = {"audio_format": "wav", "raw_audio": f.read(), "rate": 16000}
            msg = appbuilder.Message(content_data)
            out = self.asr.run(msg)
            text = out.content["result"][0]
            return text

    def run_agent(self, query):
        conversation_id = self.agent.create_conversation()
        msg = self.agent.run(conversation_id, query, stream=True)
        answer = ""
        for content in msg.content:
            answer += content.answer
        return answer


if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()
