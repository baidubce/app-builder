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


# -*- coding: utf-8 -*-
"""
文档解析
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


#  定义Parser解析结果的结构
class Position(BaseModel):
    """
    position结构
    """
    page_num: int = Field(alias="pageno")
    box: List[int]


class Layout(BaseModel):
    """
    layout结构
    """
    type: str
    text: str
    box: List[int]
    node_id: int


class Table(BaseModel):
    """
    表格结构
    """
    box: List[int]
    cells: List[Layout] = Field(alias="children")
    matrix: List[List[int]]
    node_id: int


class ParaNode(BaseModel):
    """
    文档内容层级树结构
    """
    node_id: int
    text: str
    para_type: str
    parent: Optional[int]
    children: List[int]
    position: List[Position]
    table: Optional[Table] = None


class PageContent(BaseModel):
    """
    单页文档内容结构
    """
    page_num: int
    page_width: int
    page_height: int
    page_angle: int
    page_type: str
    page_layouts: List[Layout]
    titles: Optional[List[Layout]] = []
    tables: Optional[List[Table]] = []


class ParseResult(BaseModel):
    """
    解析结果整体结构
    """
    para_node_tree: Optional[List[ParaNode]] = []
    page_contents: Optional[List[PageContent]] = []
    pdf_data: Optional[str] = ""
    raw: Optional[Dict] = {}


class ParserConfig(BaseModel):
    """
    DocParser解析配置
    """
    convert_file_to_pdf: bool = Field(alias="need_pdffile_data", default=False)
    page_filter: List[int] = Field(alias="page_filter", default=None)
    return_para_node_tree: bool = Field(alias="return_para_nodes", default=True)
    erase_watermark: bool = Field(alias="erase_watermark", default=False)


#  文档内容切分结构
class DocSegment(BaseModel):
    """
    自定义文档内容切分的结构
    """
    content: Optional[str] = ""
    title: Optional[List[str]] = []
