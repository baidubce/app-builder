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

"""doc_crop_enhance model."""
import proto

from typing import List, Dict
from pydantic import BaseModel


class DocCropEnhanceRequest(proto.Message):
    r"""文档矫正增强请求体参数.
            属性:
                image (str):
                    可选。图像内容的base64编码。
                url (str):
                    可选。图像的URL地址，经过base64编码。
                    图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。
                scan_type (int):
                    可选。选择是否对图片内主体内容进行四角点增强或矫正。
                    - scan_type = 1：只做检测，不对主体进行矫正，返回主体四角点坐标，可用作前端页面展示
                    - scan_type = 2：只做矫正，需传入主体四角点坐标，使用传入的坐标值对主体进行扣取及矫正
                    - scan_type = 3：默认值，检测并矫正，返回主体在原图中的四角点坐标以及矫正后的图像
                enhance_type (int):
                    可选。选择是否开启图像增强功能，如开启可选择增强效果，可选值如下：
                    - enhance_type = 0：默认值，不开启增强功能
                    - enhance_type = 1：去阴影
                    - enhance_type = 2：增强并锐化
                    - enhance_type = 3：黑白滤镜。
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
    scan_type: int = proto.Field(
        proto.INT32,
        number=3,
    )
    enhance_type: int = proto.Field(
        proto.INT32,
        number=4,
    )


class DocCropEnhanceResponse(proto.Message):
    """文档矫正增强识别响应消息。

        属性:
            request_id (str): 请求ID。
            log_id (int): 用于问题识别的唯一日志ID。
            image_processed (str):
                返回处理后的图片，base64编码，如请求参数 scan_type = 1 & enhance_type =0，则返回原图。
            points (List[DocLocation]):
                检测到的图片内主体在原图中的四角点坐标，scan_type = 2 时不返回此参数。
    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    image_processed: str = proto.Field(
        proto.STRING,
        number=3,
    )
    points: 'DocLocation' = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message='DocLocation',
    )


class DocLocation(proto.Message):
    """图片四角点坐标。

        属性:
            x (int): x坐标。
            y (int): y坐标。
    """
    x: int = proto.Field(
        proto.INT64,
        number=1,
    )
    y: int = proto.Field(
        proto.INT64,
        number=2,
    )


class DocCropEnhanceInMsg(BaseModel):
    """ 文档矫正增强识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
            enhance_type(int): 可选参数
                选择是否开启图像增强功能，如开启可选择增强效果，可选值如下：
                - enhance_type = 0：默认值，不开启增强功能
                - enhance_type = 1：去阴影
                - enhance_type = 2：增强并锐化
                - enhance_type = 3：黑白滤镜
    """
    raw_image: bytes = b''
    url: str = ""


class DocCropEnhanceOutMsg(BaseModel):
    """ 文档矫正增强识别响应体

        属性:
            image_processed(str): 处理后的图片，base64编码
            points(List[Dict[str, int]]): 检测主体在原图中的四角点坐标
    """
    image_processed: str
    points: List[Dict[str, int]]
