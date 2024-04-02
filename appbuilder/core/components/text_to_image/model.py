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


r"""Text2Image model.py.
"""
from typing import MutableSequence, List

import proto
from pydantic import BaseModel


class Text2ImageSubmitRequest(proto.Message):
    r"""文生图提交任务的请求体。

         参数:
            prompt(str):
                生图的文本描述。仅支持中文、日常标点符号。不支持英文，特殊符号，限制 200 字。
            width(int):
                图片宽度，支持：512x512、640x360、360x640、1024x1024、1280x720、720x1280、2048x2048、2560x1440、1440x2560。
            height(int):
                图片高度，支持：512x512、640x360、360x640、1024x1024、1280x720、720x1280、2048x2048、2560x1440、1440x2560.
            image_num(int):
                生成图片数量，默认一张，支持生成 1-8 张。
            image(string):
                参考图，需 base64 编码，大小不超过 10M，最短边至少 15px，最长边最大 8192px，支持jpg/jpeg/png/bmp 格式。
                优先级：image > url > pdf_file，当image 字段存在时，url、pdf_file 字段失效。
            url(str):
                参考图完整 url，url 长度不超过 1024 字节，url 对应的图片需 base64 编码，大小不超过 10M，最短边至少 15px，
                最长边最大8192px，支持 jpg/jpeg/png/bmp 格式。优先级：image > url > pdf_file，当image 字段存在时，url 字段失效请注意关闭 URL 防盗链。
            pdf_file(string):
                参考图 PDF 文件，base64 编码，大小不超过10M，最短边至少 15px，最长边最大 8192px 。
                优先级：image > url > pdf_file，当image 字段存在时，url、pdf_file 字段失效。
            pdf_file_num(str):
                需要识别的 PDF 文件的对应页码，当pdf_file 参数有效时，识别传入页码的对应页面内容，若不传入，则默认识别第 1 页。
            change_degree(int):
               参考图影响因子，支持 1-10 内；数值越大参考图影响越大。
         """
    prompt: str = proto.Field(
        proto.STRING,
        number=1,
    )
    width: int = proto.Field(
        proto.INT32,
        number=2,
    )
    height: int = proto.Field(
        proto.INT32,
        number=3,
    )
    image_num: int = proto.Field(
        proto.INT32,
        number=4,
        optional=True,
    )
    image: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    url: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )
    pdf_file: str = proto.Field(
        proto.STRING,
        number=7,
        optional=True,
    )
    pdf_file_num: str = proto.Field(
        proto.STRING,
        number=8,
        optional=True,
    )
    change_degree: int = proto.Field(
        proto.INT32,
        number=9,
        optional=True,
    )


class Text2ImageQueryRequest(proto.Message):
    r"""文生图生成结果查询请求体。

         参数:
            task_id(int):
                从提交请求的提交接口的返回值中获取，可使用task_id 查询总任务。
         """
    task_id: int = proto.Field(
        proto.INT64,
        number=1,
    )


class Text2ImageSubmitResponse(proto.Message):
    r"""文生图任务提交接口返回体。

         参数:
            request_id(str):
                网关层的请求ID。
            log_id(str):
                算子层请求唯一标识码。
            data(Text2ImageSubmitData):
                任务提交接口返回数据。
         """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    data: "Text2ImageSubmitData" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Text2ImageSubmitData",
    )


class Text2ImageQueryResponse(proto.Message):
    r"""文生图任务结果查询接口返回体。.

         参数:
            request_id(str):
                Request ID of gateway layer.
            log_id(str):
                Request ID of service layer.
            data(Text2ImageQueryData):
                Text to Image query response data .
         """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )

    data: "Text2ImageQueryData" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Text2ImageQueryData",
    )


class Text2ImageSubmitData(proto.Message):
    r"""文生图提交任务接口返回体数据。

         参数:
            primary_task_id(str):
                生成图片任务long类型 id，与“task_id”参数输出相同，该 id 可用于查询任务状态。
            task_id(str):
                生成图片任务string类型 id，与“primary_task_id”参数输出相同，该 id 可用于查询任务状态。
         """
    primary_task_id: int = proto.Field(
        proto.INT64,
        number=1,
    )

    task_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Text2ImageQueryData(proto.Message):
    r"""文生图任务查询接口返回体数据。
         参数:
            task_id(int):
                任务 ID.
            task_status(str):
                计算总状态。有 INIT（初始化），WAIT（排队中）, RUNNING（生成中）, FAILED（失败）, SUCCESS（成功）四种状态，只有 SUCCESS 为成功状态。
            task_progress(int):
                图片生成总进度，进度包含2种，0为未处理完，1为处理完成。
            sub_task_result_list(Text2ImageSubTaskResultList):
                子任务生成结果列表。
         """
    task_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    task_status: str = proto.Field(
        proto.STRING,
        number=2,
    )
    task_progress: int = proto.Field(
        proto.INT64,
        number=3,
    )

    sub_task_result_list: MutableSequence["Text2ImageSubTaskResultList"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="Text2ImageSubTaskResultList",
    )


class Text2ImageSubTaskResultList(proto.Message):
    r"""文生图子任务结果列表。
         参数:
            sub_task_status(int):
                单风格图片状态。有 INIT（初始化），WAIT（排队中）, RUNNING（生成中）, FAILED（失败）, SUCCESS（成功）四种状态，只有 SUCCESS 为成功状态。
            sub_task_progress(int):
                单任务图片生成进度，进度包含2种，0为未处理完，1为处理完成。
            sub_task_error_code(str):
                单风格任务错误码。0:正常；501:文本黄反拦截；201:模型生图失败。
            final_image_list(Text2ImageFinalImageList):
                单风格任务产出的最终图列表。
         """
    sub_task_status: str = proto.Field(
        proto.STRING,
        number=1,
    )
    sub_task_progress: int = proto.Field(
        proto.INT32,
        number=2,
    )
    sub_task_error_code: int = proto.Field(
        proto.INT32,
        number=3,
    )
    final_image_list: MutableSequence["Text2ImageFinalImageList"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="Text2ImageFinalImageList",
    )


class Text2ImageFinalImageList(proto.Message):
    r"""文生图单风格任务产出的最终图列表。
         参数:
            img_approve_conclusion(str):
                图片机审结果，"block"：输出图片违规；"review": 输出图片疑似违规；"pass": 输出图片未发现问题。
            img_url(str):
                图片所在 BOS http 地址，默认 1 小时失效。
            height(int):
                图片像素信息-高度。
            width(int):
                图片像素信息-宽度。
         """
    img_approve_conclusion: str = proto.Field(
        proto.STRING,
        number=1,
    )
    img_url: str = proto.Field(
        proto.STRING,
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


class Text2ImageInMessage(BaseModel):
    """ 文生图组件输入message.
        参数:
            prompt(str):
                生图的文本描述。仅支持中文、日常标点符号。不支持英文，特殊符号，限制 200 字。
    """
    prompt: str


class Text2ImageOutMessage(BaseModel):
    """ 文生图组件输出message.
        参数:
            img_urls(str):
                图片所在 BOS http 地址，默认 1 小时失效。
    """
    img_urls: List[str]
