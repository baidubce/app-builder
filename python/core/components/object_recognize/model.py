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

"""object recognize client."""
import proto

from typing import List
from pydantic import BaseModel


# PB Definition
class ObjectRecognitionRequest(proto.Message):
    r"""通用物体与场景识别请求体.

        属性:
            image (str):
                可选。图像内容的base64编码。
            url (str):
                可选。图像的URL地址，经过base64编码。
                图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。

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
    baike_num: int = proto.Field(
        proto.INT64,
        number=3,
    )


class ObjectRecognitionResponse(proto.Message):
    """通用物体与场景识别响应消息。

        属性:
            request_id (str): 请求ID。
            log_id (int): 用于问题识别的唯一日志ID。
            result_num (int): 结果数量，即结果数组中的元素数量。最多返回5个结果。
            result (List[ObjectResult]): 物体识别结果列表。
    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    result_num: int = proto.Field(
        proto.UINT32,
        number=3,
    )
    result: 'ObjectResult' = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="ObjectResult",
    )


class ObjectResult(proto.Message):
    """物体识别信息.

        属性:
            keyword (str): 图像中物体或场景的名称。
            score (float): 置信度得分，范围从0到1。
            root (str): 识别结果中的顶级标签。一些标签，如硬币、动漫、烟草等，可能没有顶级标签。
            baike_info (List[BaikeInfo]): 与识别结果对应的百科信息列表。
    """
    keyword: str = proto.Field(
        proto.STRING,
        number=1,
    )
    score: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    root: str = proto.Field(
        proto.STRING,
        number=3,
    )
    baike_info: 'BaikeInfo' = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="BaikeInfo",
    )


class BaikeInfo(proto.Message):
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


class ObjectRecognitionInMsg(BaseModel):
    """ 通用物体与场景识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""


class Object(BaseModel):
    """物体识别输入消息。
        属性:
            keyword(bytes):
                原始二进制图像数据。
            score(float):
                置信度得分，范围从0到1。
            root(str):
                识别结果中的顶级标签。
    """
    keyword: str
    score: float
    root: str


class ObjectRecognitionOutMsg(BaseModel):
    r"""识别结果列表"""
    result: List[Object]  # 结果列表
