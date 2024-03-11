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


from pydantic import BaseModel, Field
from typing import Optional

from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments


class OralQueryGenerationArgs(ComponentArguments):
    """口语化Query生成配置
    """
    """
    message: Message = Field(..., 
                             valiable_name='query', 
                             description='输入文本，用于生成Query')
    """
    query: str = Field(...,
                       valiable_name='query',
                       description='输入文本，用于生成Query')


class OralQueryGeneration(CompletionBaseComponent):
    """
    口语化Query生成，可用于问答场景下对文档增强索引。

    Examples:

        .. code-block:: python

            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = '...'

            text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
                    '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
                    '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
                    '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
                    '，实时视频分享您的生活。')
            oral_query_generation = appbuilder.OralQueryGeneration(model='ERNIE Speed-AppBuilder')
            answer = oral_query_generation(appbuilder.Message(text))
            print(answer.content)
    """
    name = 'oral_query_generation'
    version = 'v1'
    meta = OralQueryGenerationArgs

    def __init__(
        self, 
        model=None,
        secret_key: Optional[str] = None, 
        gateway: str = "",
        lazy_certification: bool = False,
    ):
        """初始化口语化Query生成模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
                OralQueryGenerationArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

    def run(self, message, stream=False, temperature=1e-10, top_p=0.0):
        """
        使用给定的输入运行模型并返回结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p(float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(query=message.content, stream=stream, temperature=temperature, top_p=top_p)
