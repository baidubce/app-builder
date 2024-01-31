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

"""qrcode ocr model."""
import proto

from typing import List
from pydantic import BaseModel


class QRcodeRequest(proto.Message):
    r"""二维码识别请求体参数.
            属性:
                image (str):
                    可选。图像内容的base64编码。
                url (str):
                    可选。图像的URL地址，经过base64编码。
                    图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。
                location (str):
                    可选。是否输出二维码/条形码位置信息
                    - false：默认值，不返回位置信息；
                    - true：返回图中二维码/条形码的位置信息，包括上边距、左边距、宽度、高度
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
    location: str = proto.Field(
        proto.STRING,
        number=3,
    )


class QRcodeResponse(proto.Message):
    """二维码识别响应消息。

        属性:
            request_id (str): 请求ID。
            log_id (int): 用于问题识别的唯一日志ID。
            codes_result_num (int):识别结果数，表示codes_result的元素个数
            result (List[QRcodeRes]): 定位和识别结果数组。
    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    codes_result_num: int = proto.Field(
        proto.INT32,
        number=3,
    )
    codes_result: 'QRcodeRes' = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message='QRcodeRes',
    )


class QRcodeRes(proto.Message):
    """二维码识别结果。

        属性:
            type (str):
                识别码类型条码类型包括：9种条形码（UPC_A、UPC_E、EAN_13、EAN_8、CODE_39、CODE_93、CODE_128、ITF、CODABAR），
                4种二维码（QR_CODE、DATA_MATRIX、AZTEC、PDF_417）。
            text (str):
                条形码/二维码识别内容,目前仅支持输出中英文结果。
            location (QRcodeLocation):
                条形码/二维码位置信息，包括上边距、左边距、宽度、高度，当请求参数 location = true 时返回
    """
    type: str = proto.Field(
        proto.STRING,
        number=1,
    )
    text: str = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    location: 'QRcodeLocation' = proto.Field(
        proto.MESSAGE,
        number=3,
        message="QRcodeLocation",
    )


class QRcodeLocation(proto.Message):
    """条形码/二维码位置信息。

           属性:
               top (int): 条形码/二维码的上边距。
               left (int): 条形码/二维码的左边距。
               width (int): 条形码/二维码的宽度。
               height (int): 条形码/二维码的高度。
       """
    top: int = proto.Field(
        proto.INT32,
        number=1,
    )
    left: int = proto.Field(
        proto.INT32,
        number=2,
    )
    width: int = proto.Field(
        proto.INT32,
        number=3,
    )
    height: int = proto.Field(
        proto.INT32,
        number=4,
    )


class QRcodeInMsg(BaseModel):
    """ 二维码识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""


class QRcodeOCRLocation(BaseModel):
    """ 条形码/二维码位置信息

        属性:
            top(int): 条形码/二维码的上边距
            left(int): 条形码/二维码的左边距
            width(int): 条形码/二维码的宽度
            height(int): 条形码/二维码的高度
    """
    top: int
    left: int
    width: int
    height: int


class QRcodeOCRRes(BaseModel):
    """ 条形码/二维码位置信息

        属性:
            type(int): 识别码类型条码类型
            text(List[str]): 条形码/二维码识别内容
            location(Object): 条形码/二维码位置信息
    """
    type: str = ""
    text: List[str]
    location: QRcodeOCRLocation = {}


class QRcodeOutMsg(BaseModel):
    r"""识别结果列表"""
    codes_result: List[QRcodeOCRRes]  # 结果列表
