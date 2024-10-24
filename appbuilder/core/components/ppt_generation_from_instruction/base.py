"""
Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from pydantic import Field
from enum import Enum

from appbuilder.core.component import ComponentArguments


DEFAULT_AUTHOR = '百度千帆AppBuilder'

class ComplexChoices(Enum):
    easy = 1
    medium = 2
    complex = 3


class FontNameChoices(Enum):
    HeiTi = '黑体'
    SongTi = '宋体'
    FangSong = '仿宋'
    YouYuan = '幼圆'
    KaiTi = '楷体'
    LiShu = '隶书'


class PPTGenerationFromInstructionArgs(ComponentArguments):
    """PPT生成组件配置
    """
    text: str = Field(...,
                      valiable_name='text',
                      description='请求生成PPT的query。')
    custom_data: dict = Field(...,
                              valiable_name='custom_data',
                              description='自定义参数，可指定标题、副标题等信息。')
    complex: ComplexChoices = Field(default=None,
                                    variable_name='complex',
                                    description='生成PPT的复杂度，可选：1、2、3，分别对应简单、中等、复杂。默认是1。')
    font_name: FontNameChoices = Field(default=None,
                                       variable_name='font_name',
                                       description='字体，可选：黑体、宋体、仿宋、幼圆、楷体、隶书。')
    user_name: str = Field(default=None,
                           variable_name='user_name',
                           description='PPT作者名。')

    def convert_params_to_dict(self):
        """输出参数字典
        """
        output_dict = {}
        for k, v in self.model_dump().items():
            if k in self.model_fields and \
                    self.model_fields[k].json_schema_extra and \
                    v is not None:
                if isinstance(v, Enum):
                    output_dict[k] = v.value
                else:
                    output_dict[k] = v
        return output_dict