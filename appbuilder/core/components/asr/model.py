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

r"""ASR model.py.
"""
from typing import MutableSequence, List

import proto
from pydantic import BaseModel


class ShortSpeechRecognitionRequest(proto.Message):
    r"""短语音识别的请求体
         参数:
            format(str):
                语音文件的格式，pcm/wav/amr/m4a。不区分大小写。推荐pcm文件。
            rate(int):
                采样率，16000，固定值。
            cuid(str):
                用户唯一标识，用来区分用户，计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内。
            dev_pid(int):
                80001（极速版输入法模型）
            speech(int):
                本地语音文件的的二进制语音数据。
         """
    format: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rate: int = proto.Field(
        proto.INT64,
        number=2,
    )
    cuid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    dev_pid: str = proto.Field(
        proto.STRING,
        number=4,
    )
    speech: bytes = proto.Field(
        proto.BYTES,
        number=5,
    )


class ShortSpeechRecognitionResponse(proto.Message):
    r"""短语音识别结果返回体.

         参数:
            request_id(str):
                网关层的请求ID.
            err_no(int):
                算子层的错误码.
            err_msg(str):
                算子层的错误信息.
            corpus_no(str):
            sn(str):
                语音数据唯一标识，系统内部产生。如果反馈及debug请提供sn。
            result(MutableSequence[str]):
                识别结果数组，返回1个最优候选结果。utf-8 编码。
         """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    err_no: int = proto.Field(
        proto.INT32,
        number=2,
    )

    err_msg: str = proto.Field(
        proto.STRING,
        number=3,
    )
    corpus_no: str = proto.Field(
        proto.STRING,
        number=4,
    )

    sn: str = proto.Field(
        proto.STRING,
        number=5,
    )
    result: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6
    )


class ASRInMsg(BaseModel):
    """ ASR输入message.
        参数:
            raw_audio(bytes):
                原始的语音文件字节数组.

    """
    raw_audio: bytes


class ASROutMsg(BaseModel):
    """ ASR输出message.

        参数:
            result(List[str]):
                输出识别后的文本结果.
    """
    result: List[str]

