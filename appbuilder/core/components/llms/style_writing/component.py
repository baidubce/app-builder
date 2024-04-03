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
import json

from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message

from appbuilder.core.component import ComponentArguments

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StyleQueryChoices(Enum):
    BILIBILI = "B站"
    XIAOHONGSHU = "小红书"
    GENERAL = "通用"

    def to_chinese(self):
        """
        将StyleQueryChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是StyleQueryChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            StyleQueryChoices.BILIBILI: "B站",
            StyleQueryChoices.XIAOHONGSHU: "小红书",
            StyleQueryChoices.GENERAL: "通用",
        }
        return descriptions[self]


class LengthChoices(Enum):
    SHORT = 100  # 短
    MEDIUM = 300  # 中
    LONG = 600  # 长

    def to_chinese(self):
        """
        将LengthChoices枚举对象转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            str: 转换后的中文描述，包括"短"、"中"和"长"。
        
        """
        descriptions = {
            LengthChoices.SHORT: "短",
            LengthChoices.MEDIUM: "中",
            LengthChoices.LONG: "长",
        }
        return descriptions[self]


class StyleWritingArgs(ComponentArguments):
    """风格写作配置"""
    message: Message = Field(...,
                             variable_name="query",
                             description="输入消息，用于模型的主要输入内容，例如'帮我生成一个介绍保温杯的话术'")
    style_query: StyleQueryChoices = Field(...,
                                           variable_name="style_query",
                                           description="风格查询选项，可选值为 'B站', '小红书', '通用'。")
    length: LengthChoices = Field(...,
                                  variable_name="length",
                                  description="输出长度，可选值为 '短' (100), '中' (300), '长' (600)。")


class StyleWriting(CompletionBaseComponent):
    """
    风格写作大模型组件， 基于生成式大模型进行风格写作，支持B站、小红书等多种风格，可用于文案、广告等多种场景。

    Examples:

        .. code-block:: python

            import os
            import appbuilder
            # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
            os.environ["APPBUILDER_TOKEN"] = '...'

            style_writing = appbuilder.StyleWriting(model="ERNIE Speed-AppBuilder")
            answer = style_writing(appbuilder.Message("帮我写一篇关于人体工学椅的文案"), style_query="小红书", length=100)

    """

    name = "style_writing"
    version = "v1"
    meta = StyleWritingArgs

    manifests = [
        {
            "name": "style_writing",
            "description": "能够根据用户的输入内容和风格要求，利用大语言模型的生成能力，自动生成符合特定风格的文案。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用于描述生成文案的主题和要求。"
                    },
                    "style": {
                        "type": "string",
                        "description": "用于定义文案生成的风格，包括通用、B站、小红书，默认为通用。",
                        "enum": ["通用", "B站", "小红书"]
                    },
                    "length": {
                        "type": "integer",
                        "description": "用于定义输出内容的长度。有效的选项包括 100（短）、300（中）、600（长），默认值为 100。",
                        "enum": [100, 300, 600]
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    def __init__(
            self,
            model=None,
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = False,
    ):
        """初始化StyleWriting模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
            StyleWritingArgs, model=model, secret_key=secret_key, gateway=gateway,
            lazy_certification=lazy_certification)

    def run(self, message, style_query="通用", length=100, stream=False, temperature=1e-10, top_p=0):
        """
        使用给定的输入运行模型并返回结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            style_query (str): 风格查询选项，用于指定写作风格。有效的选项包括 'B站', '小红书', '通用'。默认值为 '通用'。
            length (int): 输出内容的长度。有效的选项包括 100（短），300（中），600（长）。默认值为 100。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p(float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, style_query=style_query, length=length, stream=stream,
                           temperature=temperature, top_p=top_p)

    def tool_eval(self, name: str, streaming: bool = False, **kwargs):
        """
        tool_eval for function call
        """
        query = kwargs.get("query", None)
        if not query:
            raise ValueError("param `query` is required")
        msg = Message(query)
        style = kwargs.get("style", "通用")
        if style not in ["通用", "B站", "小红书"]:
            style = "通用"
        length = kwargs.get("length", 100)
        try:
            length = int(length)
            if length not in [100, 300, 600]:
                length = 100
        except:
            length = 100
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(message=msg, style_query=style, length=length, stream=False,
                              temperature=temperature, top_p=top_p)
        
        if streaming:
            yield str(message.content)
        else:
            return str(message.content)
