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


"""植物识别数据类"""

from typing import List

import proto
from pydantic import BaseModel


TOP_NUM = 1
BAIKE_NUM = 0

class PlantBaikeInfo(proto.Message):
    """
    植物百度百科信息

    属性:
        baike_url (str): 百度百科页面URL
        image_url (str): 百度百科中的图像URL
        description (str): 百度百科中的描述信息
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


class Plant(proto.Message):
    """
    植物识别结果

    属性:
        name(str): 植物名称
        score(float): 置信度
        baike_info (List[PlantBaikeInfo]): 植物百科信息
    """
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    score: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    baike_info = proto.RepeatedField(
        PlantBaikeInfo,
        number=3,
    )


class PlantRecognitionRequest(proto.Message):
    r"""植物识别请求参数

         属性:
             image (str, 可选): 图像base64编码结果，支持jpg/png/bmp格式
             url (str, 可选): 图像下载链接，base64编码后结果小于4MB, 短边大于15px，长边小于4096px
             如果image存在，url字段则自动失效
             top_num(int，可选): 返回得分较高的结果
             baike_num(int，可选): 返回百科信息的个数

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
        proto.INT64,
        number=3,
    )
    baike_num: int = proto.Field(
        proto.INT64,
        number=4,
    )


class PlantRecognitionResponse(proto.Message):
    r"""植物识别返回结果

        属性:
             log_id (int): 随机日志ID
             request_id(str): 请求链路ID
             result (List[Plant]): 识别植物列表信息
    """
    log_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    result = proto.RepeatedField(
        Plant,
        number=3,
    )


class PlantRecognitionInMsg(BaseModel):
    """ 植物识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""


class PlantScore(BaseModel):
    """ 植物识别输出消息
        属性:
            name(str): 植物名
            score(float): 识别分数
      """
    name: str
    score: float


class PlantRecognitionOutMsg(BaseModel):
    """ 植物识别输出消息
        属性:
            PlantScores(List[PlantScore]): 植物识别结果列表
    """
    plant_score_list: List[PlantScore]
