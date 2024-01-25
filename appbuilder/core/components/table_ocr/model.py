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

"""table ocr model."""
import proto

from typing import List, Dict
from pydantic import BaseModel


class TableOCRRequest(proto.Message):
    r"""表格文字识别请求体参数.
            属性:
                image (str):
                    可选。图像内容的base64编码。
                url (str):
                    可选。图像的URL地址，经过base64编码。
                    图像大小必须小于4MB，图像的最短边长大于15像素，最长边长大于4096像素。
                cell_contents (str):
                    是否输出单元格文字位置信息，可选值包括：
                    - false： 默认值，仅输出单元格行列信息及四角点坐标，不输出单元格内文字位置信息
                    - true： 输出单元格内文字的外接四边形四角点坐标，若文字折行，则分行分别输出
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
    cell_contents: str = proto.Field(
        proto.STRING,
        number=3,
    )


class TableOCRResponse(proto.Message):
    """表格文字识别响应消息

        属性:
            request_id (str): 请求ID。
            log_id (int): 用于问题识别的唯一日志ID。
            table_num (int): 检测到的表格数量。
            result (List[TableRes]): 表格文字识别结果列表。
    """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    log_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    table_num: int = proto.Field(
        proto.INT64,
        number=3,
    )
    tables_result: 'TableRes' = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message='TableRes',
    )


class TableRes(proto.Message):
    """表格文字识别结果

        属性:
            table_location (List[Location]): 单个表格的四角点x,y坐标。
            header (List[Header]): 表头信息。
            body (List[Body]): 单元格信息。
            footer (List[Footer]): 表尾信息。
    """
    table_location: 'Location' = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Location"
    )
    header: 'Header' = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Header"
    )
    body: 'Body' = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="Body"
    )
    footer: 'Footer' = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="Footer"
    )


class Header(proto.Message):
    """表头信息

        属性:
            location (List[Location]): 表头位置，四角点 x,y 坐标。
            words (str): 表头文字内容，按行拆分。
    """
    location: 'Location' = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Location"
    )
    words: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Body(proto.Message):
    """单元格信息

        属性:
            cell_location (List[Location]): 表头位置，四角点 x,y 坐标。
            row_start (str): 单元格行起始编号，横线编号从0开始。
            row_end (str): 单元格行终止编号。
            col_start (str): 单元格列起始编号，竖线编号从0开始。
            col_end (str): 单元格列终止编号。
            words (str): 单元格文字内容。
            contents (str): 单元格内文字内容，分行显示，当请求参数 cell_contents = true 时返回。
    """
    cell_location: 'Location' = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Location"
    )
    row_start: int = proto.Field(
        proto.INT32,
        number=2,
    )
    row_end: int = proto.Field(
        proto.INT32,
        number=3,
    )
    col_start: int = proto.Field(
        proto.INT32,
        number=4,
    )
    col_end: int = proto.Field(
        proto.INT32,
        number=5,
    )
    words: str = proto.Field(
        proto.STRING,
        number=6,
    )
    contents: str = proto.Field(
        proto.STRING,
        number=7,
    )


class Footer(proto.Message):
    """表尾信息

        属性:
            location (List[Location]): 表头位置，四角点 x,y 坐标。
            words (str): 表头文字内容，按行拆分。
    """
    location: 'Location' = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Location"
    )
    words: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Location(proto.Message):
    """四角点坐标。

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


class TableOCRInMsg(BaseModel):
    """ 表格文字识别输入消息

        属性:
            raw_image(bytes): 图像原始内容
            url(str): 图像下载链接
    """
    raw_image: bytes = b''
    url: str = ""


class PyHeader(BaseModel):
    """表头信息

        属性:
            location (List[Dict[str, int]]): 表头位置，四角点 x,y 坐标。
            words (str): 表头文字内容，按行拆分。
    """
    location: List[Dict[str, int]]
    words: str


class PyBody(BaseModel):
    """单元格信息

        属性:
            cell_location (List[Location]): 表头位置，四角点 x,y 坐标。
            row_start (str): 单元格行起始编号，横线编号从0开始。
            row_end (str): 单元格行终止编号。
            col_start (str): 单元格列起始编号，竖线编号从0开始。
            col_end (str): 单元格列终止编号。
            words (str): 单元格文字内容。
    """
    cell_location: List[Dict[str, int]]
    row_start: int
    row_end: int
    col_start: int
    col_end: int
    words: str


class PyFooter(BaseModel):
    """表尾信息

        属性:
            location (List[Dict[str, int]]): 表头位置，四角点 x,y 坐标。
            words (str): 表头文字内容，按行拆分。
    """
    location: List[Dict[str, int]]
    words: str


class TableOCRRes(BaseModel):
    """表格文字识别对象信息
        属性:
            table_location (List[Dict[str, int]]): 单个表格的四角点x,y坐标
            header (List[PyHeader]): 表头信息
            body (List[PyBody]): 单元格信息
            footer (List[PyFooter]): 表尾信息
    """
    table_location: List[Dict[str, int]]
    header: List[PyHeader]
    body: List[PyBody]
    footer: List[PyFooter]


class TableOCROutMsg(BaseModel):
    r"""识别结果列表"""
    tables_result: List[TableOCRRes]  # 结果列表
