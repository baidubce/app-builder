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
from typing import List
from pydantic import Field

from appbuilder.core.component import ComponentArguments
from appbuilder.core.components.gbi.basic import SessionRecord
from appbuilder.core.components.gbi.basic import ColumnItem


class NL2SqlArgs(ComponentArguments):
    """
    nl2sql 的参数

    Attributes:
        query: 用户的 query 输入
        session: gbi session 的历史 列表
        column_constraint: 列选的限制条件
    """
    query: str = Field(..., description="用户的 query 输入")
    session: List[SessionRecord] = Field(default=list(), description="gbi session 的历史 列表")
    column_constraint: List[ColumnItem] = Field(default=list(), description="列选的限制条件")