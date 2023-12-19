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


"""Landmark recognition model."""

from typing import MutableMapping

import proto
from pydantic import BaseModel


class LandmarkRecognitionRequest(proto.Message):
    r"""地标识别请求参数

         属性:
             image (str, 可选): 图像base64编码结果.
             url (str, 可选): 图像下载链接，base64编码后结果小于4MB, 短边大于15px，长边小于4096px.
         """
    image: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class LandmarkRecognitionResponse(proto.Message):
    r"""地标识别返回结果

        属性:
             log_id (int): 随机日志ID
             result (MutableMapping[str, str]): 地标识别结果, eg: {"landmark": "狮身人面像"}.
             request_id(str): 服务链路追踪ID.
    """
    log_id: int = proto.Field(
        proto.INT64,
        number=1
    )
    result: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class LandmarkRecognitionInMsg(BaseModel):
    """ 地标识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""


class LandmarkRecognitionOutMsg(BaseModel):
    """ 地标识别输出消息

        属性:
            landmark(str): 地标识别结果
    """
    landmark: str
