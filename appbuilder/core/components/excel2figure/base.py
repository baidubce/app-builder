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
from pydantic import Field, AnyUrl
from appbuilder.core.component import Component, ComponentArguments

class Excel2FigureArgs(ComponentArguments):
    """
    excel2figure 的参数

    Attributes:
        query: str
        excel_file_url: AnyUrl
    """
    query: str = Field(..., description="用户的 query 输入", max_length=400)
    excel_file_url: AnyUrl = Field(..., description="用户的 excel 文件地址，需要是一个可被公网下载的 URL 地址")