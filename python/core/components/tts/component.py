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

r"""text to speech component."""
import base64
import traceback

from typing import Literal
from urllib.parse import quote_plus
from appbuilder.core.component import Component
from appbuilder.core._client import HTTPClient
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.components.tts.model import *
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class TTS(Component):
    r"""
      文本转语音组件，即输入一段文本将其转为一段语音

      Examples:

      .. code-block:: python

        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'
        tts = appbuilder.TTS()

        # 默认使用baidu-tts模型, 默认返回MP3格式
        inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
        out = tts.run(inp)
        with open("sample.mp3", "wb") as f:
            f.write(out.content["audio_binary"])

        # 使用paddlespeech-tts模型，目前只支持返回WAV格式
        inp = appbuilder.Message(content={"text": "欢迎使用语音合成"})
        out = tts.run(inp, model="paddlespeech-tts", audio_type="wav")
        with open("sample.wav", "wb") as f:
            f.write(out.content["audio_binary"])
    """
    Baidu_TTS = "baidu-tts"
    PaddleSpeech_TTS = "paddlespeech-tts"

    def __init__(self, *args, **kwargs):
        r"""初始化语音识别实例

            参数:
                *args (any, 可选): 位置参数
                **kwargs(any, 可选)： 关键字参数
            返回:
                无
           """
        r""""implement __init__ method"""
        super().__init__(*args, **kwargs)
        self.model = ""

    @HTTPClient.check_param
    @components_run_trace
    def run(self,
            message: Message,
            model: Literal["baidu-tts", "paddlespeech-tts"] = "baidu-tts",
            speed: int = 5,
            pitch: int = 5,
            volume: int = 5,
            person: int = 0,
            audio_type: Literal["mp3", "wav", "pcm"] = "mp3",
            timeout: float = None,
            retry: int = 0,
            stream: bool = False) -> Message:
        """
        执行文本转语音。
        
        Args:
            message (Message): 待转为语音的文本。
                举例: Message(content={"text": "欢迎使用百度语音"})如果选择baidu-tts模型，text最大文本长度为1024 GBK编码长度,大约为512个中英文字符;如果选择paddlespeech-tts模型, text最大文本长度是510个字符。
            model (str, 可选): 默认是`baidu-tts`模型，可设置为`paddlespeech-tts`。
            speed (int, 可选): 语音语速，默认是5中等语速，取值范围在0~15之间，
                如果选择模型为paddlespeech-tts，参数自动失效。
            pitch (int, 可选): 语音音调，默认是5中等音调，取值范围在0~15之间，
                如果选择模型为paddlespeech-tts，参数自动失效。
            volume (int, 音量): 语音音量，默认是5中等音量，取值范围在0~15之间，
                如果选择模型为paddlespeech-tts，参数自动失效。
            person (int, 可选): 语音人物特征，默认是0,
                可选值包括:
                度小宇=1 度小美=0 度逍遥（基础）=3 度丫丫=4 度逍遥（精品）=5003
                度小鹿=5118 度博文=106 度小童=110 度小萌=111 度米朵=103 度小娇=5
                度逍遥-情感男声=4003 度博文-专业男主播=4106 度小贤-电台男主播=4115
                度小鹿-甜美女声=4119 度灵儿-清激女声=4105 度小乔-活泼女声=4117
                度小雯-活力女主播=4100 度米朵-可爱女声=4103 度姗姗-娱乐女声=4144
                度小贝-知识女主播=4278 度清风-配音男声=4143 度小新-专业女主播=4140
                度小彦-知识男主播=4129 度星河-广告男声=4149 度小清-广告女声=4254
                度博文-综艺男声=4206 南方-电台女主播=4226，
                如果选择模型为paddlespeech-tts，参数自动失效。
            audio_type (str, 可选): 音频文件格式，默认是`mp3`，
                如果选择`paddlespeech-tts`模型，参数只能设为`wav`。
            timeout (float, 可选): HTTP超时时间。
            retry (int, 可选): HTTP重试次数。
            stream (bool, 可选): 是否以流的形式返回音频数据，默认为False。
        
        Returns:
            message (Message): 文本转语音结果。举例: Message(content={"audio_binary": b"xxx", "audio_type": "mp3"})
        """
        if model != self.Baidu_TTS and model != self.PaddleSpeech_TTS:
            raise InvalidRequestArgumentError(
                f"unsupported model {model}, expected model in {'baidu-tts', 'paddlespeech-tts'}"
            )
        self.model = model
        inp = TTSInMsg(**message.content)
        if len(inp.text) == 0:
            raise InvalidRequestArgumentError("request format error, text field is empty")
        if model == self.Baidu_TTS and (stream or audio_type not in ["mp3", "wav"]):
            raise InvalidRequestArgumentError("Baidu_TTS argument error, expected audio type in {'mp3', 'wav'}")
        elif model == self.PaddleSpeech_TTS:
            if stream and audio_type != "pcm":
                raise InvalidRequestArgumentError("Invalid audio type, expected audio type is {'pcm'}")
            elif not stream and audio_type != "wav":
                raise InvalidRequestArgumentError("Invalid audio type, expected audio type is {'wav'}")

        request = TTSRequest()
        request.tex = inp.text
        request.spd = speed
        request.pit = pitch
        request.vol = volume
        request.per = person
        request.stream = stream
        if audio_type == "mp3":
            request.aue = 3
        elif audio_type == "wav" or audio_type == "pcm":
            request.aue = 6
        if stream and self.model == self.PaddleSpeech_TTS:
            return Message(content=self.__synthesis(request=request, stream=True, retry=retry))
        else:
            response = self.__synthesis(request=request, timeout=timeout, retry=retry)
            out = TTSOutMsg(audio_binary=response.binary, audio_type=audio_type)
            return Message(content=out.model_dump())

    def __synthesis(self,
                    request: TTSRequest,
                    stream: bool = False,
                    timeout: float = None,
                    retry: int = 0
                    ) -> TTSResponse:
        r"""调用底层接口进行语音合成

            参数:
                request (obj: `[PaddleTTSRequest, TTSRequest]`) : 语音合成输入参数

            返回：
                response (obj: `TTSResponse`): 语音合成输出参数
        """
        request.ctp = "1"
        request.lan = "zh"
        request.cuid = "1"
        if self.model == self.Baidu_TTS:
            request.tex = quote_plus(request.tex)
            request.validate_baidu_tts()
            url = self.http_client.service_url("/v1/bce/aip_speech/tts_online")
        elif self.model == self.PaddleSpeech_TTS:
            request.tp_project_id = "paddlespeech"
            request.tp_per_id = "100001"
            request.validate_paddle_speech_tts()
            url = self.http_client.service_url("/v1/bce/paddle_speech/text2audio")
        else:
            raise ValueError("model '{}' is not supported".format(self.model))
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        auth_header = self.http_client.auth_header()
        if self.model == self.Baidu_TTS:
            response = self.http_client.session.post(url, data=TTSRequest.to_dict(request), timeout=timeout,
                                                     headers=auth_header)
        elif self.model == self.PaddleSpeech_TTS:
            auth_header = self.http_client.auth_header()
            auth_header['Content-type'] = "application/json"
            if not stream:
                response = self.http_client.session.post(url, json=TTSRequest.to_dict(request),
                                                         timeout=timeout, headers=auth_header)
            if stream:
                response = self.http_client.session.post(url, json=TTSRequest.to_dict(request), timeout=(10, 200),
                                                         headers=auth_header, stream=True)

        self.http_client.check_response_header(response)
        content_type = response.headers.get("Content-Type", "application/json")
        request_id = self.http_client.response_request_id(response)
        if content_type.find("application/json") != -1:
            data = response.json()
            self.http_client.check_response_json(data)
            self.__class__.__check_service_error(request_id, data)
        if not stream:
            return TTSResponse(
                binary=response.content,
                request_id=request_id,
                aue=request.aue
            )
        else:
            return _iterate_chunk(request_id, response)

    @staticmethod
    def __check_service_error(request_id: str, data: dict):
        r"""个性化服务response检查

              参数:
                  request (dict) : 文本转语音body返回
              返回：
                  无
          """

        if "err_no" in data or "err_msg" in data or 'sn' in data or 'idx' in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("err_no", 0),
                service_err_message="{} . {} . {}]".
                format(data.get("err_msg", ""),
                       data.get("sn", ""),
                       data.get("idx", ""))
            )


def _iterate_chunk(request_id, response):
    try:
        for line in response.iter_lines():
            chunk = line.decode('utf-8')
            if chunk.startswith('data:'):
                chunk = chunk.replace('data: ', '')
                yield base64.b64decode(chunk)
    except Exception as e:
        raise AppBuilderServerException(request_id=request_id, message=traceback.format_exc())
    finally:
        response.close()
