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

class PPTGenerationFromFileArgs(ComponentArguments):
    """论文生成PPT组件配置
    """
    file_url: str = Field(...,
                          valiable_name='file_url',
                          description='文件链接。')
    user_name: str = Field(default=None,
                           variable_name='user_name',
                           description='作者。')
    
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