#!/usr/bin/env python 3
# -*- coding: utf-8 -*-
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

r"""GBI nl2sql component.
"""

from pydantic import BaseModel, Field
from typing import Dict, List


class NL2SqlResult(BaseModel):
    """
    gbi_nl2sql 返回的结果
    """

    llm_result: str = Field(..., description="大模型返回的结果")
    sql: str = Field(..., description="从大模型中抽取的 sql 语句")

class SessionRecord(BaseModel):
    """
    gbi session record
    """
    query: str = Field(..., description="用户的问题")
    answer: NL2SqlResult = Field(..., description="nl2sql 返回的结果")

class ColumnItem(BaseModel):
    """
    列信息
    """
    ori_value: str = Field(..., description="query 中的 词语, 比如: 北京去年收入,  "
                                            "分词后: 北京, 去年, 收入, ori_value 是分词中某一个，比如: ori_value = 北京")
    column_name: str = Field(..., description="对应数据库中的列名称, 比如: city")
    column_value: str = Field(..., description="对应数据库中的列值, 比如: 北京市")

    table_name: str = Field(..., description="该列所在表的名字")
    is_like: bool = Field(default=False, description="与 ori_value 的匹配是包含 还是 等于，包含: True; 等于: False")


SUPPORTED_MODEL_NAME = {
    "ERNIE-Bot 4.0", "ERNIE-Bot", "ERNIE-Bot-turbo"
}
