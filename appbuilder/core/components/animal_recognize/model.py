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

"""animal recognize client."""
import proto

from typing import List
from pydantic import BaseModel


class AnimalRecognitionRequest(proto.Message):
    r"""动物识别请求体参数.
            属性:
                image (str):
                    可选。图像内容的base64编码。
                url (str):
                    可选。图像的URL地址，经过base64编码。
                    图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。
                top_num (int):
                    返回预测得分top结果数，默认为6
                baike_num (int):
                    控制返回结果是否带有百科信息，默认为0，不返回
            必须设置image或url属性之一，如果两者都设置了，将使用image属性。
        """
    image: str = proto.Field(
        proto.STRING,
        number=1,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    top_num: int = proto.Field(
        proto.INT32,
        number=3,
    )
    baike_num: int = proto.Field(
        proto.INT64,
        number=4,
    )


class AnimalRecognitionResponse(proto.Message):
    """动物识别响应消息。

        属性:
            request_id (str): 请求ID。
            log_id (int): 用于问题识别的唯一日志ID。
            result (List[AnimalRecognitionRes]): 动物识别结果列表。
    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    result: 'AnimalRecognitionRes' = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message='AnimalRecognitionRes',
    )


class AnimalRecognitionRes(proto.Message):
    """动物识别结果详情。

        属性:
            name (str): 请求ID。
            score (int): 用于问题识别的唯一日志ID。
            baike_info (AnimalBaikeInfo): 动物识别百科信息。
    """
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    score: str = proto.Field(
        proto.STRING,
        number=2,
    )
    baike_info: 'AnimalBaikeInfo' = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="AnimalBaikeInfo",
    )


class AnimalBaikeInfo(proto.Message):
    """物体识别百科信息。

           属性:
               baike_url (str): 与识别结果对应的百度百科页面的URL。
               image_url (str): 与识别结果相关联的图像的URL。
               description (str): 百度百科提供的识别结果的描述。
       """
    baike_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    image_url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )


class AnimalRecognitionInMsg(BaseModel):
    """ 动物识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""


class AnimalRes(BaseModel):
    """动物识别对象信息

        属性:
            name (str): 动物名称，示例：蒙古马
            score (str): 置信度，示例：0.5321
    """
    name: str
    score: str


class AnimalRecognitionOutMsg(BaseModel):
    r"""识别结果列表"""
    result: List[AnimalRes]  # 结果列表
