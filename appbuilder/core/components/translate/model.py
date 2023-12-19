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


# -*- coding: utf-8 -*-
"""
文本翻译model
"""

import proto
from typing import List
from pydantic import BaseModel


class TranslateRequest(proto.Message):
    """
    文本翻译请求体。

    Attributes:
        from_lang (str): 翻译的源语言。
        to_lang (str): 翻译的目标语言。
        q (str): 待翻译的文本。
    """
    from_lang: str = proto.Field(
        proto.STRING,
        number=1,
        json_name="from"
    )
    to_lang: str = proto.Field(
        proto.STRING,
        number=2,
        json_name="to"
    )
    q: str = proto.Field(
        proto.STRING,
        number=3,
    )


class TranslateResponse(proto.Message):
    """
    文本翻译请求响应体。

    Attributes:
        log_id (int): 文本翻译请求的标识符。
        result (TranslateRes): 文本翻译结果。
    """
    log_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    result: "TranslateRes" = proto.Field(
        proto.MESSAGE,
        number=2,
        message='TranslateRes',
    )


class TranslateRes(proto.Message):
    """
    表示翻译请求的结果。

    Attributes:
        from_lang (str): 翻译的源语言。
        to_lang (str): 翻译的目标语言。
        trans_result (List[TranslateResMeta]): 翻译结果列表。
    """
    from_lang: str = proto.Field(
        proto.STRING,
        number=1,
        json_name="from"

    )
    to_lang: str = proto.Field(
        proto.STRING,
        number=2,
        json_name="to"
    )
    trans_result: "TranslateResMeta" = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message='TranslateResMeta',
    )


class TranslateResMeta(proto.Message):
    """
    表示与翻译结果关联的proto结构元数据。

    Attributes:
        dst (str): 翻译后的文本。
        src (str): 源文本。
    """
    dst: str = proto.Field(
        proto.STRING,
        number=1,
    )
    src: str = proto.Field(
        proto.STRING,
        number=2,
    )


class TranslateResult(BaseModel):
    """
    表示与翻译结果关联的pydantic结构元数据。

    Attributes:
        src (str): 源文本。
        dst (str): 翻译后的文本。
    """
    src: str  # 源文本
    dst: str  # 目标文本


class TranslateOutMsg(BaseModel):
    """
    表示文本翻译输出的pydantic结构消息。

    Attributes:
        from_lang (str): 翻译的源语言。
        to_lang (str): 翻译的目标语言。
        trans_result (List[TranslateResult]): 一个包含翻译结果的列表。
            如果请求参数 `q` 包含 `\n`，则会以分段形式返回翻译结果。
    """
    from_lang: str
    to_lang: str
    trans_result: List[TranslateResult]
