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
菜品识别model
"""
import proto
import pydantic
from typing import Optional, List


class DishRecognitionRequest(proto.Message):
    """
    菜品识别请求的请求体。

    Attributes:
	    image (str): 表示图像数据的 Base64 编码字符串。
        url (str): 图像的 URL，用于识别。
        top_num (int): 要返回的顶部结果的数量。
        filter_threshold (float): 过滤识别结果的置信度阈值。
        baike_num (int): 要返回的百科结果的数量。

    Note:
        'image' 或 'url' 字段至少传一个，两个都传默认使用 'image'。
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
    filter_threshold: float = proto.Field(
        proto.FLOAT,
        number=4,
    )
    baike_num: int = proto.Field(
        proto.INT32,
        number=5,
    )


class DishRecognitionResponse(proto.Message):
    """
    表示菜品识别返回的响应结果。

    Attributes:
        log_id (str): 识别请求的唯一标识符。
        request_id (str): 识别请求的唯一标识符。
        result_num (int): 返回的识别结果数量。
        result (List[DishRecognitionRes]): 识别结果列表。
    """
    log_id: str = proto.Field(
        proto.INT64,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    result_num: int = proto.Field(
        proto.INT32,
        number=3,
    )
    result: "DishRecognitionRes" = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message='DishRecognitionRes',
    )


class DishRecognitionRes(proto.Message):
    """
    表示菜品识别结果。

    Attributes:
        name (str): 识别的菜品名称。
        calorie (str): 识别的菜品热量信息。
        has_calorie (bool): 指示识别菜品是否返回了热量信息。
        probability (str): 识别置信度分数。
        baike_info (DishBaikeInfo): 与被识别菜品相关的百度百科信息。
    """
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    calorie: str = proto.Field(
        proto.STRING,
        number=2,
    )
    has_calorie: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    probability: str = proto.Field(
        proto.STRING,
        number=4,
    )
    baike_info: "DishBaikeInfo" = proto.Field(
        proto.MESSAGE,
        number=5,
        message='DishBaikeInfo',
    )


class DishBaikeInfo(proto.Message):
    """
    与被识别菜品相关的百度百科信息。

    Attributes:
        baike_url (str): 识别菜品的百度百科页面URL。
        image_url (str): 百度百科中与被识别菜品相关的图像URL。
        description (str): 百度百科中关于被识别菜品的描述或信息。
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


class DishRecognitionInMsg(pydantic.BaseModel):
    """
    菜品识别的输入消息模型。

    :param raw_image: 图像的字节数组，包含要识别的菜品图像的原始数据。
                      此字段是可选的，可以为 None。
    :param url: 图像的可下载URL。如果提供，则将从此URL下载图像进行识别。
                      此字段也是可选的，可以为 None。
    注意：raw_image 和 url 至少传一个，不能同时为 None，两个都传默认使用 raw_image。
    """
    raw_image: bytes = None
    url: str = None


class DishRecognitionResult(pydantic.BaseModel):
    """
    表示菜品识别结果。

    Attributes:
        name (str): 识别到的菜品名称。
        calorie (Optional[str]): 菜品的卡路里信息。如果未返回卡路里信息，默认为 None。
    """
    name: str
    calorie: Optional[str] = None


class DishRecognitionOutMsg(pydantic.BaseModel):
    """
    表示菜品识别组件返回的结构。

    Attributes:
        result (List[DishRecognitionResult]): 包含菜品识别结果的列表。
    """
    result: List[DishRecognitionResult]
