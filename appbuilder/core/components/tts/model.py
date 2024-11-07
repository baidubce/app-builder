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

r"""short text to speech model."""
import proto

from pydantic import BaseModel


class TTSRequest(proto.Message):
    r"""文本转语音请求参数.

        属性:
            tex (str): 如果选择`baidu-tts`模型，`tex`最大文本长度为1024 GBK编码长度, 如果选择`paddlespeech-tts`模型,
            `tex`最大文本长度是510个字符.
            tok (str, 可选): 用户token.
            cuid (str, 可选): 用户ID.
            ctp (str, 可选): 用户客户端类型.
            lan (str): 目前仅支持中英-ZH.
            spd(int, 可选): 语音语速，默认是5中等语速，取值范围在0~15之间，如果选择模型为paddlespeech-tts，参数自动失效.
            pit(int, 可选): 语音音调，默认是5中等音调，取值范围在0~15之间，如果选择模型为paddlespeech-tts，参数自动失效.
            vol(int, 音量): 语音音量，默认是5中等音量，取值范围在0~15之间，如果选择模型为paddlespeech-tts，参数自动失效.
            per(int, 可选): 语音人物特征，默认是0,可选值包括度小宇=1 度小美=0 度逍遥（基础）=3 度丫丫=4 度逍遥（精品）=5003
                度小鹿=5118 度博文=106 度小童=110 度小萌=111 度米朵=103 度小娇=5，如果选择模型为paddlespeech-tts，参数自动失效.
            aue(int, 可选): 语音格式, 默认是3(mp3)  4(pcm-16k) 5(pcm-8k) 6-wav.
            tp_project_id(str): paddlespeech-tts项目ID
            tp_per_id(str): paddlespeech-tts音频ID

    """
    tex: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tok: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    cuid: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    ctp: str = proto.Field(
        proto.STRING,
        number=4,
    )
    lan: str = proto.Field(
        proto.STRING,
        number=5,
    )
    spd: int = proto.Field(
        proto.INT32,
        number=6,
    )
    pit: int = proto.Field(
        proto.INT32,
        number=7,
    )
    vol: int = proto.Field(
        proto.INT32,
        number=8,
    )
    per: int = proto.Field(
        proto.INT32,
        number=9,
    )
    aue: int = proto.Field(
        proto.INT32,
        number=10,
    )
    tp_project_id: str = proto.Field(
        proto.STRING,
        number=11,
        optional=True,
    )
    tp_per_id: str = proto.Field(
        proto.STRING,
        number=12,
        optional=True,
    )
    stream: bool = proto.Field(
        proto.BOOL,
        number=13,
        optional=True,
    )

    def __validate(self):
        """检查公共参数"""
        if len(self.tex) == 0:
            raise ValueError("tex field must be set")
        if self.spd < 0 or self.spd > 15:
            raise ValueError("spd value must in [0,15]")
        if self.pit < 0 or self.pit > 15:
            raise ValueError("pit value must in [0,15]")
        if self.vol < 0 or self.vol > 15:
            raise ValueError("vol value must in [0,15]")

    def validate_baidu_tts(self):
        """检查baidu-tts模型请求参数"""
        self.__validate()
        if self.per not in {0, 1, 3, 4, 5, 103, 106, 110, 111, 5003, 5118}:
            raise ValueError(
                f"per value is illegal, exepcted in {0, 1, 3, 4, 5, 103, 106, 110, 111, 5003, 5118}, got {self.per}"
            )
        if self.aue == 0:
            self.aue = 3
        if self.aue not in {3, 4, 5, 6}:
            raise ValueError(f"aue value is illegal, exepect in {3, 4, 5, 6}, got {self.aue}")

    def validate_paddle_speech_tts(self):
        """验证参数是否合法"""
        self.__validate()
        if self.aue == 0:
            self.aue = 6
        if self.aue not in {6}:
            raise ValueError("aue value is illegal, expectd aue value is 6, got{}".format(self.aue))


class TTSResponse(proto.Message):
    r"""文本转语音返回.

         属性:
             binary (bytes): 语音二进制流.
             aue (int):语音格式, 3(mp3), 4(pcm-16k), 5(pcm-8k) 6(wav).
             request_id(str): 请求ID
     """
    binary: bytes = proto.Field(
        proto.BYTES,
        number=1
    )
    aue: int = proto.Field(
        proto.INT32,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class TTSInMsg(BaseModel):
    r"""文本转语音输入消息.

        属性:
            text(str): 待转为语音的文本, 如果选择`baidu-tts`模型，最大文本长度为1024 GBK编码长度
            如果选择`paddlespeech-tts`模型, 最大文本长度是510个字符.
    """
    text: str


class TTSOutMsg(BaseModel):
    r""" 文本转语音输出消息.

        属性:
            audio_binary(bytes): 语音二进制流.
            audio_type(AudioType): 语音类型，`mp3`或`wav`.
    """
    audio_binary: bytes
    audio_type: str
