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

from typing import MutableMapping, List

import proto
from pydantic import BaseModel


class ImageUnderstandRequest(proto.Message):
    r"""地标识别请求参数

         属性:
             image (str, 可选): 图像base64编码结果.
             url (str, 可选): 图像下载链接，base64编码后结果小于4MB, 短边大于15px，长边小于4096px.
             question(str): 针对图片的问题信息，限制在100个字符之内
         """
    image: str = proto.Field(
        proto.STRING,
        number=1,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    question: str = proto.Field(
        proto.STRING,
        number=3,
    )
    output_CHN: bool = proto.Field(
        proto.BOOL,
        number=4
    )
    subject_detect: bool = proto.Field(
        proto.BOOL,
        number=5
    )
    llm_switch: bool = proto.Field(
        proto.BOOL,
        number=6
    )


class ImageUnderstandTask(proto.Message):
    r"""地标识别返回结果

        属性:
             log_id (int): 随机日志ID
             request_id(str): 服务链路追踪ID.
             result (MutableMapping[str, str]): {"task_id":"task-123"}
    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    log_id: int = proto.Field(
        proto.INT64,
        number=2
    )
    result: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class ImageUnderstandLocation(proto.Message):
    """位置信息

          属性：
               left (int): 表示定位位置的长方形左上顶点的水平坐标
               top (int): 表示定位位置的长方形左上顶点的垂直坐标
               width (int): 表示定位位置的长方形的宽度
               height (int): 表示定位位置的长方形的高度
    """
    top: int = proto.Field(
        proto.INT32,
        number=1
    )
    left: int = proto.Field(
        proto.INT32,
        number=2
    )
    width: int = proto.Field(
        proto.INT32,
        number=3
    )
    height: int = proto.Field(
        proto.INT32,
        number=4
    )


class ImageUnderstandSubject(proto.Message):
    """主题信息

            属性：
                name (str): 主题名字
                location (ImageUnderstandLocation): 主题位置
    """
    name: str = proto.Field(
        proto.STRING,
        number=1
    )
    location = proto.Field(
        ImageUnderstandLocation,
        number=2
    )


class ImageUnderstandOCR(proto.Message):
    """主题信息
            属性：
                word (str): 文本识别结果
                rect (ImageUnderstandLocation): 位置信息
    """
    word: str = proto.Field(
        proto.STRING,
        number=1
    )
    rect = proto.Field(
        ImageUnderstandLocation,
        number=2
    )
    prob = proto.Field(
        proto.FLOAT,
        number=3
    )


class ImageUnderstandResult(proto.Message):
    """主题信息
            属性：
                task_id (str): 任务id
                ret_code (int): 返回错误码
                ret_msg（str）：错误信息
                description（str）：描述信息
                description_to_llm（str）：描述信息
                subject_result（ImageUnderstandSubject）：主题结果
                ocr_result（ImageUnderstandOCR）：ocr识别结果
                classify_result（str）：分类结果
    """
    task_id: str = proto.Field(
        proto.STRING,
        number=1
    )
    ret_code: int = proto.Field(
        proto.INT32,
        number=2
    )
    ret_msg: str = proto.Field(
        proto.STRING,
        number=3
    )
    description: str = proto.Field(
        proto.STRING,
        number=4
    )
    description_to_llm: str = proto.Field(
        proto.STRING,
        number=5,
    )
    subject_result = proto.RepeatedField(
        ImageUnderstandSubject,
        number=6
    )
    ocr_result = proto.RepeatedField(
        ImageUnderstandOCR,
        number=7,
    )
    classify_result = proto.RepeatedField(
        proto.STRING,
        number=8
    )


class ImageUnderstandResponse(proto.Message):
    """主题信息
            属性：
                request_id (str): 请求id
                log_id (int): 日志ID
                result（ImageUnderstandResult）：图像理解结果
        """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    log_id: int = proto.Field(
        proto.INT64,
        number=2
    )
    result = proto.Field(
        ImageUnderstandResult,
        number=3
    )


class ImageUnderstandInMsg(BaseModel):
    """ 图像理解输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""
    question: str = ""
    language: str = "zh-CN"


class ImageUnderstandOutMsg(BaseModel):
    """ 图像理解输出结果

        属性:
            description(str): 输出描述信息
    """
    description: str = ""
