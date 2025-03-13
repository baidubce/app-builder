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

"""general ocr model."""
import proto

from typing import List
from pydantic import BaseModel


# PB definition
class GeneralOCRRequest(proto.Message):
    """通用ocr识别请求体

    属性:
        image (str):
            可选。图像内容的base64编码。
        url (str):
            可选。图像的URL地址，经过base64编码。
            图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。
        pdf_file (str):
            可选。PDF文件内容的base64编码。
        pdf_file_num (str):
            可选。PDF文件的页数。
        ofd_file (str):
            可选。OFD（Open Format Document）文件内容的base64编码。
        ofd_file_num (str):
            可选。OFD文件的页数。
        language_type (str):
            可选。文本使用的语言类型。默认为"CHN_ENG"。
            可能的取值包括：
            - "auto_detect": 自动检测语言并识别。
            - "CHN_ENG": 中英文混合。
            - "ENG": 英文。
            - "JAP": 日文。
            - "KOR": 韩文。
            - "FRE": 法文。
            - "SPA": 西班牙文。
            - "POR": 葡萄牙文。
            - "GER": 德文。
            - "ITA": 意大利文。
            - "RUS": 俄文。
            - "DAN": 丹麦文。
            - "DUT": 荷兰文。
            - "MAL": 马来文。
            - "SWE": 瑞典文。
            - "IND": 印度尼西亚文。
            - "POL": 波兰文。
            - "ROM": 罗马尼亚文。
            - "TUR": 土耳其文。
            - "GRE": 希腊文。
            - "HUN": 匈牙利文。
            - "THA": 泰文。
            - "VIE": 越南文。
            - "ARA": 阿拉伯文。
            - "HIN": 印地文。
        detect_direction (str):
            可选。是否检测文本方向。默认为"false"。
            可能的取值包括：
            - "true": 检测文本方向。
            - "false": 不检测文本方向。
        paragraph (str):
            可选。是否输出段落信息。默认为"false"。
            可能的取值包括：
            - "true": 输出段落信息。
            - "false": 不输出段落信息。
        probability (str):
            可选。是否输出置信度。默认为"false"。
            可能的取值包括：
            - "true": 返回识别结果中每行的置信度。
            - "false": 不返回置信度。
    """
    image: str = proto.Field(
        proto.STRING,
        number=1,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    pdf_file: str = proto.Field(
        proto.STRING,
        number=3,
    )
    pdf_file_num: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    ofd_file: str = proto.Field(
        proto.STRING,
        number=5,
    )
    ofd_file_num: str = proto.Field(
        proto.STRING,
        number=6,
    )
    language_type: str = proto.Field(
        proto.STRING,
        number=7,
    )
    detect_direction: str = proto.Field(
        proto.STRING,
        number=8,
    )
    paragraph: str = proto.Field(
        proto.STRING,
        number=9,
    )
    probability: str = proto.Field(
        proto.STRING,
        number=10,
    )
    multidirectional_recognize: str = proto.Field(
        proto.STRING,
        number=11,
    )

class GeneralOCRResponse(proto.Message):
    """通用ocr识别结果

        属性:
        log_id (int):
            必填。用于问题跟踪的唯一日志ID。
        direction (int):
            可选。当detect_direction=true时的图像方向。
            - -1: 未定义。
            - 0: 正常。
            - 1: 逆时针旋转90度。
            - 2: 逆时针旋转180度。
            - 3: 逆时针旋转270度。
        words_result_num (int):
            必填。识别结果的数量。
        words_result (List[Dict[str, Any]]):
            必填。识别结果的数组。
            - words (str): 识别出的文本。
            - probability (Dict[str, float]): 识别结果中每行的置信度值。
            包括平均值、方差和最小置信度值。
            当probability=true时返回。
        paragraphs_result (List[Dict[str, Any]]):
            可选。段落检测结果。当paragraph=true时返回。
            - words_result_idx (List[int]): 包含在段落中的行索引。
        paragraphs_result_num (int):
            可选。段落检测结果的数量。当paragraph=true时返回。
        pdf_file_size (int):
            可选。输入PDF文件的总页数。当pdf_file参数有效时返回。
        ofd_file_size (str):
            可选。输入OFD文件的总页数。当ofd_file参数有效时返回。

    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_id: int = proto.Field(
        proto.UINT64,
        number=2,
    )
    direction: int = proto.Field(
        proto.INT32,
        number=3,
    )
    words_result_num: int = proto.Field(
        proto.UINT32,
        number=4,
    )
    words_result: 'WordResult' = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message='WordResult'
    )
    paragraphs_result: 'ParagraphResult' = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message='ParagraphResult'
    )
    paragraphs_result_num: int = proto.Field(
        proto.UINT32,
        number=7,
    )
    pdf_file_size: int = proto.Field(
        proto.UINT32,
        number=8,
    )
    ofd_file_size: str = proto.Field(
        proto.STRING,
        number=9,
    )


class WordResult(proto.Message):
    """ 识别结果列表.

        属性:
            - words (str): 识别出的文本。
            - probability (Dict[str, float]): 识别结果中每行的置信度值。
                包括平均值、方差和最小置信度值。
                当probability=true时返回。
     """
    words: str = proto.Field(
        proto.STRING,
        number=1,
    )
    probability: 'Probability' = proto.Field(
        proto.MESSAGE,
        number=2,
        message='Probability'
    )


class Probability(proto.Message):
    """置信度

           属性:
              - average (float): 每行的平均置信度
              - variance (float): 每行置信度的方差
              - minimum (float)：每行的最小置信度
    """

    average: float = proto.Field(
        proto.FLOAT,
        number=1,
    )
    variance: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    min: float = proto.Field(
        proto.FLOAT,
        number=3,
    )


class ParagraphResult(proto.Message):
    """
        段落检测结果，当paragraph=true时将返回该字段。
    """
    words_result_idx: int = proto.Field(
        proto.INT32,
        number=1,
    )


class GeneralOCRInMsg(BaseModel):
    """ 通用文字识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    image_base64: str = ""  # 原始图片base64数据
    image_url: str = ""  # 图片可下载链接
    pdf_base64: str = "" #pdf base64数据
    pdf_url: str = "" #pdf 可下载链接
    pdf_file_num: str = "1" #需要识别的PDF文件的对应页码
    detect_direction: str = "false" #是否检测图像朝向
    multidirectional_recognize: str = "true" #是否开启行级别的多方向文字识别


class Words(BaseModel):
    """ 识别文字

        属性：
            words(str):识别文字结果
    """
    words: str


class GeneralOCROutMsg(BaseModel):
    """ 识别文字结果列表

        属性：
            words_result([]array):识别文字结果列表
    """
    words_result: List['Words']
