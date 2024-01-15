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

""" dialog_summary
"""
from pydantic import BaseModel, Field

from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments


class DialogSummaryArgs(ComponentArguments):
    """会话小结生成配置
    """
    message: Message = Field(...,
                             variable_name='query',
                             description='输入对话文本，用于生成小结')


class DialogSummary(CompletionBaseComponent):
    """
    会话小结大模型组件， 基于生成式大模型对一段用户与坐席的对话生成总结，结果按{"诉求": "", "回应": "", "解决情况": ""}格式输出。

    Examples:

        .. code-block:: python

            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            dialog_summary = appbuilder.DialogSummary(model="eb-4")
            text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
            answer = dialog_summary(appbuilder.Message(text))

    """
    name = "dialog_summary"
    version = "v1"
    meta = DialogSummaryArgs

    def __init__(self, model=None):
        """初始化DialogSummary模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
        
        Returns:
            None
        
        """
        super().__init__(DialogSummaryArgs, model=model)

    def run(self, message, stream=False, temperature=1e-10):
        """
        使用给定的输入运行模型并返回结果。
        
        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, optional): 指定是否以流式形式返回响应。默认为 False。
            temperature(float, optional): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
        
        返回:
            obj:`Message`: 模型运行后的输出消息。
        
        """

        return super().run(message=message, stream=stream, temperature=temperature)
