# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pydantic import Field
from appbuilder.core.component import ComponentArguments



class HallucinationDetectionArgs(ComponentArguments):
    """
    幻觉检测配置

    Attributes:
        query: str
            用户查询。
        context: str
            根据query得到的检索结果。
        answer: str
            基于context生成的query的答案。
    """
    query: str = Field(...,
                       valiable_name='query',
                       description='用户查询。')
    context: str = Field(...,
                         valiable_name='context',
                         description='根据query得到的检索结果。')
    answer: str = Field(...,
                        valiable_name='answer',
                        description='基于context生成的query的答案。')