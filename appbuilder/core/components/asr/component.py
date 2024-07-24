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

r"""ASR component.
"""
import os
import uuid
import json

import requests
import tempfile
from urllib.parse import urlparse

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core._client import HTTPClient
from appbuilder.core.components.asr.model import ShortSpeechRecognitionRequest, ShortSpeechRecognitionResponse, \
    ASRInMsg, ASROutMsg
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace

DEFAULT_AUDIO_MAX_DURATION = 55 * 1000  # 55s
# 参考短语音极速版API(https://ai.baidu.com/ai-doc/SPEECH/Jlbxdezuf)
DEFAULT_FRAME_RATE = 16000


class ASR(Component):
    r"""
    ASR组件，即对于输入的语音文件，输出语音识别结果

    Examples:

    .. code-block:: python

        import appbuilder
        asr = appbuilder.ASR()
        os.environ["APPBUILDER_TOKEN"] = '...'

        with open("xxxx.pcm", "rb") as f:
            audio_data = f.read()
        content_data = {"audio_format": "pcm", "raw_audio": audio_data, "rate": 16000}
        msg = appbuilder.Message(content_data)
        out = asr.run(msg)
        print(out.content) # eg: {"result": ["北京科技馆。"]}
     """
    name = "asr"
    version = "v1"

    manifests = [
        {
            "name": "asr",
            "description": "对于输入的语音文件进行识别，输出语音识别结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_url": {
                        "type": "string",
                        "description": "输入语音文件的url,根据url获取到语音文件"
                    },
                    "file_name": {
                        "type": "string",
                        "description": "待识别语音文件名,用于生成获取语音的url"
                    },
                    "file_type": {
                        "type": "string",
                        "description": "语音文件类型,支持pcm/wav/amr/m4a",
                        "enum": ["pcm", "wav", "amr", "m4a"]
                    }
                },
                "anyOf": [
                    {
                        "required": [
                            "file_url"
                        ]
                    },
                    {
                        "required": [
                            "file_name"
                        ]
                    }
                ]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, audio_format: str = "pcm", rate: int = 16000,
            timeout: float = None, retry: int = 0, **kwargs) -> Message:
        """
        输入语音文件并返回语音识别结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。举例: Message(content={"raw_audio": b"..."})。
            audio_format (str，可选): 语音文件的格式，pcm/wav/amr/m4a。不区分大小写。推荐pcm文件。
            rate (int， 可选): 采样率，16000，固定值。
            timeout (float, 可选): HTTP超时时间。
            retry (int, 可选): HTTP重试次数。

        返回:
            obj:`Message`: 短语音识别结果。举例: Message(content={"result": ["北京科技馆。"]})。
        """
        inp = ASRInMsg(**message.content)
        request = ShortSpeechRecognitionRequest()
        request.format = audio_format
        request.rate = rate
        request.cuid = str(uuid.uuid4())
        request.dev_pid = "80001"
        request.speech = inp.raw_audio
        traceid = kwargs.get("traceid", "")
        response = self._recognize(request, timeout, retry, request_id=traceid)
        out = ASROutMsg(result=list(response.result))
        return Message(content=out.model_dump())

    def _recognize(
            self,
            request: ShortSpeechRecognitionRequest,
            timeout: float = None,
            retry: int = 0,
            request_id: str = None,
    ) -> ShortSpeechRecognitionResponse:
        """
        使用给定的输入并返回语音识别的结果。

        参数:
            request (obj:`ShortSpeechRecognitionRequest`): 输入请求，这是一个必需的参数。
            timeout (float, 可选): 请求的超时时间。
            retry (int, 可选): 请求的重试次数。

        返回:
            obj:`ShortSpeechRecognitionResponse`: 接口返回的输出消息。
        """
        ContentType = "audio/" + request.format + ";rate=" + str(request.rate)
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = ContentType
        params = {
            'dev_pid': request.dev_pid,
            'cuid': request.cuid
        }
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        response = self.http_client.session.post(self.http_client.service_url("/v1/bce/aip_speech/asrpro"),
                                                 params=params, headers=headers, data=request.speech, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        response = ShortSpeechRecognitionResponse.from_json(payload=json.dumps(data))
        response.request_id = request_id
        return response

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查

            参数:
                request (dict) : 短语音识别body返回
            返回：
                无
        """
        if "err_no" in data and "err_msg" in data:
            if data["err_no"] != 0:
                raise AppBuilderServerException(
                    request_id=request_id,
                    service_err_code=data["err_no"],
                    service_err_message=data["err_msg"]
                )

    @components_run_stream_trace
    def tool_eval(self, name: str, streaming: bool, **kwargs):
        """
        asr for function call
        """
        file_url = kwargs.get("file_url", None)
        if not file_url:
            file_urls = kwargs.get("file_urls", {})
            file_path = kwargs.get("file_name", None)
            if not file_path:
                raise InvalidRequestArgumentError("request format error, file name is not set")
            file_name = os.path.basename(file_path)
            file_url = file_urls.get(file_name, None)
            if not file_url:
                raise InvalidRequestArgumentError(
                    f"request format error, file {file_url} url does not exist"
                )

        _, file_type = os.path.splitext(os.path.basename(urlparse(file_url).path))
        file_type = file_type.strip('.')

        audio_file = tempfile.NamedTemporaryFile("wb", suffix=file_type)
        audio_file.write(requests.get(file_url).content)

        raw_audios = _convert(audio_file.name, file_type)
        text = ""
        for raw_audio in raw_audios:
            content_data = {"audio_format": file_type, "raw_audio": raw_audio, "rate": DEFAULT_FRAME_RATE}
            msg = Message(content_data)
            out = self.run(msg)
            text += "".join(out.content["result"])
        results = {"识别结果": text}
        audio_file.close()
        res = json.dumps(results, ensure_ascii=False, indent=4)
        if streaming:
            yield {
                "type": "text",
                "text": res,
                "visible_scope": 'llm',
            }
            yield {
                "type": "text",
                "text": "",
                "visible_scope": 'user',
            }
        else:
            return res


def _convert(path, file_type):
    from pydub import AudioSegment
    if file_type.lower() == "mp3":
        audio = AudioSegment.from_mp3(path)
    elif file_type.lower() == "wav":
        audio = AudioSegment.from_wav(path)
    # 如果是pcm格式，则直接读取并返回
    elif file_type.lower() == "pcm":
        with open(path, "rb") as f:
            return [f.read()]
    else:
        # pydub自动检测音频类型
        audio = AudioSegment.from_wav(path)
    # 如果取样率为16000且时长小于60s，则直接读取音频并返回
    if (audio.frame_rate == DEFAULT_FRAME_RATE and audio.frame_count() * 1000
            / audio.frame_rate < DEFAULT_AUDIO_MAX_DURATION):
        with open(path, "rb") as f:
            return [f.read()]
    audio = audio.set_frame_rate(DEFAULT_FRAME_RATE)
    total_milliseconds = int(audio.frame_count() * 1000 / audio.frame_rate)
    start = 0
    raw_audios = []
    while start < total_milliseconds:
        end = start + DEFAULT_AUDIO_MAX_DURATION
        if start + DEFAULT_AUDIO_MAX_DURATION > total_milliseconds:
            end = total_milliseconds
        audio_seg = audio[start:end]
        audio_seg_file = tempfile.NamedTemporaryFile("wb", suffix="wav")
        try:
            audio_seg.export(audio_seg_file.name, format="wav")
            with open(audio_seg_file.name, "rb") as f:
                raw_audios.append(f.read())
        finally:
            audio_seg_file.close()
        start = end
    return raw_audios



