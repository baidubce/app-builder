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

""" is complex query
"""
from pydantic import Field

from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments
from appbuilder.core.components.llms.base import CompletionBaseComponent


class IsComplexQueryMeta(ComponentArguments):
    """ IsComplexQueryMeta
    """
    message: Message = Field(..., 
                             variable_name="query", 
                             description="输入消息，用于模型的输入，一般为问题。")


class IsComplexQuery(CompletionBaseComponent):
    """ 基于输入的问题, 对问题进行初步的分类，方便下游使用不同类型的流程来处理当前的简单问题/复杂问题。广泛用于知识问答场景。
    
    Examples:

        .. code-block:: python
            import os
            import appbuilder

            # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
            os.environ["APPBUILDER_TOKEN"] = "..."

            is_complex_query = appbuilder.IsComplexQuery(model="eb-turbo-appbuilder")

            msg = "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？"
            msg = appbuilder.Message(msg)
            answer = is_complex_query(msg)

            print("Answer: \n{}".format(answer.content))
    """
    name = "is_complex_query"
    version = "v1"
    meta = IsComplexQueryMeta

    def __init__(self, model=None):
        """初始化IsComplexQueryMeta任务。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
        
        Returns:
            None
        
        """
        super().__init__(IsComplexQueryMeta, model=model)

    def run(self, message, stream=False, temperature=1e-10):
        """
        给定输入（message）到模型运行，同时指定运行参数，并返回结果。

        参数:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        return super().run(message=message, stream=stream, temperature=temperature)
