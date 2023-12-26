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

from typing import Dict, List


class NL2SqlResult(object):
    """
    gbi_nl2sql 返回的结果
    """

    def __init__(self, llm_result: str, sql: str):
        """
        初始化
        Args:
            llm_result: 大模型返回的结果
            sql: 从 llm_result 中抽取的 sql 语句
        """
        self.llm_result = llm_result
        self.sql = sql

    def to_json(self) -> Dict:
        """
        转换成 字典
        Returns:

        """
        return self.__dict__


class GBISessionRecord(object):
    """
    gbi session record
    """

    def __init__(self, query: str, answer: NL2SqlResult):
        """
        GBI Session 的记录
        Args:
            query: 用户的问题
            answer: gbi_nl2sql 返回的结果
        """
        self.query = query
        self.answer = answer

    def to_json(self) -> Dict:
        return {"query": self.query,
                "answer": self.answer.to_json()}


class ColumnItem(object):
    """
    column item
    """

    def __init__(self, ori_value: str, column_name: str, column_value: str, table_name: str,
                 is_like: bool = False):
        """
        用于标识 query 中的词 应该对应到数据库中的某个列值以及列名，用于提升 sql 生成效果
        Args:
            ori_value: query 中的 词语, 比如: "北京去年收入",  分词后: "北京, 去年, 收入", ori_value 是分词中某一个，比如: ori_value = "北京"
            column_name: 对应数据库中的列名称, city
            column_value: 对应数据库中的列值, 北京市
            table_name: 该列所属的表名称
            is_like: 与 ori_value 的匹配是包含 还是 等于，包含: True; 等于: False
        """
        self.column_name = column_name
        self.column_value = column_value
        self.ori_value = ori_value
        self.table_name = table_name
        self.is_like = is_like

    def to_json(self) -> Dict:
        """
        转换成 json
        Returns:

        """
        return self.__dict__


SUPPORTED_MODEL_NAME = {
    "ERNIE-Bot 4.0", "ERNIE-Bot-8K", "ERNIE-Bot", "ERNIE-Bot-turbo", "EB-turbo-AppBuilder"
}
