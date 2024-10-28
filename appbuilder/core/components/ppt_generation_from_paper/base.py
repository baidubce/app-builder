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

class StyleChoices(Enum):
    technology = '科技'
    business = '商务'
    fresh = '小清新'
    cute_cartoon = '可爱卡通'
    chinese_style = '中国风'
    minimalist = '极简'
    party_politics = '党政'


class ColorChoices(Enum):
    purple = '紫色'
    red = '红色'
    orange = '橙色'
    yellow = '黄色'
    green = '绿色'
    cyan = '青色'
    blue = '蓝色'
    pink = '粉色'


class FontNameChoices(Enum):
    HeiTi = '黑体'
    SongTi = '宋体'
    FangSong = '仿宋'
    YouYuan = '幼圆'
    KaiTi = '楷体'
    LiShu = '隶书'


class PPTGenerationFromPaperArgs(ComponentArguments):
    """论文生成PPT组件配置
    """
    file_key: str = Field(...,
                          valiable_name='file_key',
                          description='论文链接。')
    style: StyleChoices = Field(default=None,
                                valiable_name='style',
                                description='PPT风格，可选：科技、商务、小清新、可爱卡通、中国风、极简、党政。')
    color: ColorChoices = Field(default=None,
                                variable_name='color',
                                description='PPT主色调。可选：紫色、红色、橙色、黄色、绿色、青色、蓝色、粉色。')
    title: str = Field(default=None,
                       variable_name='title',
                       description='自定义标题。优先使用自定义标题，如果为空则使用解析结果中的标题。')
    pleader: str = Field(default=None,
                         variable_name='pleader',
                         description='汇报人。')
    advisor: str = Field(default=None,
                         variable_name='advisor',
                         description='指导教师。')
    school: str = Field(default=None,
                        variable_name='school',
                        description='学校名称。')
    school_logo: str = Field(default=None,
                             variable_name='school_logo',
                             description='学校logo图片链接。')
    school_picture: str = Field(default=None,
                                variable_name='school_picture',
                                description='学校图片链接。')
    
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