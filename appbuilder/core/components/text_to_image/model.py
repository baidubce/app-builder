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

from typing import Optional, Union
import proto
from pydantic import BaseModel, Field


class Text2ImageSubmitRequest(BaseModel):
    prompt: str = Field(default='')
    width: int = Field(default=1024)
    height: int = Field(default=1024)
    image_num: int = Field(default=1, ge=1, le=8)
    image: Optional[str] = Field(default="")
    url: Optional[str] = Field(default="")
    pdf_file: Optional[str] = Field(default="")
    pdf_file_num: Optional[str] = Field(default="")
    change_degree: Optional[int] = None
    text_content: Optional[str] = None
    task_time_out: Optional[int] = None
    text_check: Optional[int] = None


class Text2ImageSubmitErrorDetail(BaseModel):
    msg: Optional[str]
    word: Optional[object]


class Text2ImageSubmitResponseData(BaseModel):
    primary_task_id: Optional[int] = None
    task_id: Optional[str] = None

class Text2ImageSubmitResponse(BaseModel):
    log_id: Optional[int] = None
    data: Optional[Text2ImageSubmitResponseData] = Text2ImageSubmitResponseData()
    error_msg: Optional[str] = None
    error_detail: Optional[Text2ImageSubmitErrorDetail] = None
    error_code: Optional[int] = None


class Text2ImageQueryRequest(BaseModel):
    task_id: Optional[str]

class FinalImage(BaseModel):
    img_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    img_approve_conclusion: Optional[str] = None

class SubTaskResult(BaseModel):
    sub_task_status: Optional[str] = None
    sub_task_progress_detail: Union[int, float, None] = None
    sub_task_progress: Union[float, int, None] = None
    sub_task_error_code: Optional[int] = None
    final_image_list: Optional[list[FinalImage]] = None

class Text2ImageQueryResponseData(BaseModel):
    task_id: Optional[int] = None
    task_status: Optional[str] = None
    task_progress_detail: Union[float, int, None] = None
    task_progress: Union[float, int, None] = None
    sub_task_result_list: Optional[list[SubTaskResult]] = None
    
    


class Text2ImageQueryResponse(BaseModel):
    log_id: Union[str, int, None] = None
    data: Optional[Text2ImageQueryResponseData] = Text2ImageQueryResponseData()


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
            task_progress(float):
                图片生成总进度，0到1之间的浮点数表示进度，0为未处理完，1为处理完成。
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
    task_progress: float = proto.Field(
        proto.FLOAT,
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
            sub_task_progress(float):
                单任务图片生成进度，0到1之间的浮点数表示进度，0为未处理完，1为处理完成。
            sub_task_error_code(str):
                单风格任务错误码。0:正常；501:文本黄反拦截；201:模型生图失败。
            final_image_list(Text2ImageFinalImageList):
                单风格任务产出的最终图列表。
         """
    sub_task_status: str = proto.Field(
        proto.STRING,
        number=1,
    )
    sub_task_progress: float = proto.Field(
        proto.FLOAT,
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
