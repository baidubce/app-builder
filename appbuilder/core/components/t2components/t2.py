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

r"""Text2Image component.
"""
import time
import json
import math

from typing import Optional
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, RiskInputException
from appbuilder.core.components.text_to_image.model import Text2ImageSubmitRequest, Text2ImageQueryRequest, \
    Text2ImageQueryResponse, Text2ImageSubmitResponse, Text2ImageOutMessage, Text2ImageInMessage
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class T2components(Component):
    r"""
    文生图组件，即对于输入的文本，输出生成的图片url。

    Examples:

    .. code-block:: python

        import appbuilder
        text_to_image = appbuilder.Text2Image()
        os.environ["APPBUILDER_TOKEN"] = '...'
        content_data = {"prompt": "上海的经典风景", "width": 1024, "height": 1024, "image_num": 1}
        msg = appbuilder.Message(content_data)
        out = text_to_image.run(inp)
        # 打印生成结果
        print(out.content) # eg: {"img_urls": ["xxx"]}
    """

    manifests = [
        {
            "name": "text_to_image",
            "description": "文生图，该组件只用于图片创作。当用户需要进行场景、人物、海报等内容的绘制时，使用该画图组件。如果用户需要生成图表（柱状图、折线图、雷达图等），则必须使用代码解释器。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "文生图用的query。特别注意，这个字段只能由中文字符组成，不能含有任何英语描述。"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    def tool_eval():
        pass
