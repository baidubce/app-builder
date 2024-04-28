# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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

"""doc converter model."""
import proto
from datetime import date, datetime

from typing import List, Dict
from pydantic import BaseModel


class DocFormatConverterInMessage(BaseModel):
    """ 文档格式转换输入message
        属性:
            file_path: 文件路径
            pdf_file_num(str): 需要转换的PDF文件的对应页码, 从1开始
    """
    file_path: str = None
    page_num: str = None


class DocFormatConverterOutMessage(BaseModel):
    """ 文档格式转换输出message
        属性:
            word_url(str): 转换后的word路径
            excel_url(str): 转换后的excel路径
    """
    word_url: str
    excel_url: str


class DocFormatConverterSubmitRequest(proto.Message):
    """
    文档格式转换提交请求类。
    用于构建和提交文档格式转换任务所需的参数。
    """
    image: bytes = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    pdf_file: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    pdf_file_num: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


class DocFormatConverterSubmitResponse(proto.Message):
    """文档格式转换提交响应类"""
    class Result(proto.Message):
        """Result"""
        task_id: str = proto.Field(proto.STRING, number=1)

    success: bool = proto.Field(proto.BOOL, number=1)
    log_id: int = proto.Field(proto.UINT64, number=2)
    error_code: int = proto.Field(proto.INT32, number=3)
    code: int = proto.Field(proto.INT32, number=4)
    error_msg: str = proto.Field(proto.STRING, number=5)
    message: str = proto.Field(proto.STRING, number=6)
    result: Result = proto.Field(proto.MESSAGE, number=7, message=Result)




class DocFormatConverterQueryRequest(proto.Message):
    """
    文档格式转换查询请求类。
    用于查询文档格式转换任务所需的参数
    """
    task_id = proto.Field(
        proto.STRING,
        number=1,
    )


class DocFormatConverterQueryResponse(proto.Message):
    """文档格式转换查询响应类"""
    class Result(proto.Message):
        """Result"""
        class ResultData(proto.Message):
            """ResultData"""
            word: str = proto.Field(proto.STRING, number=1)
            excel: str = proto.Field(proto.STRING, number=2)

        task_id: str = proto.Field(proto.STRING, number=1)
        ret_code: int = proto.Field(proto.INT32, number=2)
        ret_msg: str = proto.Field(proto.STRING, number=3)
        percent: int = proto.Field(proto.INT32, number=4)
        result_data: ResultData = proto.Field(proto.MESSAGE, number=5, message=ResultData)
        create_time: datetime = proto.Field(proto.STRING, number=6)
        start_time: datetime = proto.Field(proto.STRING, number=7)
        end_time: datetime = proto.Field(proto.STRING, number=8)

    success: bool = proto.Field(proto.BOOL, number=1)
    log_id: int = proto.Field(proto.INT64, number=2)
    result: Result = proto.Field(proto.MESSAGE, number=3, message=Result)
    code: int = proto.Field(proto.INT64, number=4)
    message: str = proto.Field(proto.STRING, number=5)


