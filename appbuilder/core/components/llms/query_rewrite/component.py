"""QueryRewrite"""
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


"""
多轮改写
"""
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import appbuilder

class RewriteTypeChoices(Enum):
    """"""
    user_assistant_user = "带机器人回复"
    user_user = "仅用户查询"

    def to_chinese(self):
        """
        将RewriteTypeChoices枚举类中的值转换为中文描述。
        
        Args:
            无参数
        
        Returns:
            返回一个字典，键是RewriteTypeChoices枚举类的成员，值为对应的中文描述字符串。
        
        """
        descriptions = {
            RewriteTypeChoices.user_assistant_user: "带机器人回复",
            RewriteTypeChoices.user_user: "仅用户查询",
        }
        return descriptions[self]


class QueryRewriteArgs(ComponentArguments):
    """多轮改写配置"""
    message: Message = Field(..., 
                             variable_name="query",
                             description="输入消息，用于模型的主要输入内容，例如'['我应该怎么办理护照？', '您可以查询官网或人工咨询', \
                                         '我需要准备哪些材料？', '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', '在哪里办']'")
    rewrite_type: RewriteTypeChoices = Field(...,  
                                             variable_name="rewrite_type",
                                             description="改写类型选项，可选值为 '带机器人回复'(改写时参考user查询历史和assistant回复历史)，\
                                                         '仅用户查询'(改写时参考user查询历史)。 默认是'带机器人回复'. ")


class QueryRewrite(CompletionBaseComponent):
    """
    多轮改写大模型组件， 基于生成式大模型进行多轮对话query改写的组件。它主要用于理解和优化用户与机器人的交互过程，进行指代消解及省略补全。该组件支持不同的改写类型，可根据对话历史生成更准确的用户查询。

    Examples:

        .. code-block:: python

            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            query_rewrite = appbuilder.QueryRewrite(model="ERNIE Speed-AppBuilder")
            answer = query_rewrite(appbuilder.Message(['我应该怎么办理护照？', 
                                                     '您可以查询官网或人工咨询', 
                                                     '我需要准备哪些材料？', 
                                                     '身份证、免冠照片一张以及填写完整的《中国公民因私出国（境）申请表》', 
                                                     '在哪里办']), 
                                                     rewrite_type="带机器人回复")
                        
    """

    name = "query_rewrite"
    version = "v1"
    meta = QueryRewriteArgs

    def __init__(
        self, 
        model=None,
        secret_key: Optional[str] = None, 
        gateway: str = "",
        lazy_certification: bool = False,
    ):
        """QueryRewrite模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
                QueryRewriteArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

    def run(self, message, rewrite_type="带机器人回复", stream=False, temperature=1e-10, top_p=0):
        """
        使用给定的输入运行模型并返回结果。输入列表长度不超过10，字符总长度不超过5000.
        
        变量:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            rewrite_type (str, optional): 改写类型选项，可选值为 '带机器人回复'(改写时参考user查询历史和assistant回复历史)，
                                         '仅用户查询'(改写时参考user查询历史)。 默认是"带机器人回复。
            stream (bool, optional): 指定是否以流式形式返回响应。默认为 False。
            temperature(float, optional): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p(float, optional): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        
        """


        if message is None:
            raise ValueError("input message is required")

        sum_len = sum(len(item) for item in message.content)
        if len(message.content) > 10 or len(message.content) % 2 == 0:
            raise ValueError(f"illegal input，expected len(message.content) in {1,3,5,9}, got {len(message.content)}")
        if sum_len > 4000:
            raise ValueError(f"illegal input, expected length <= 4000, got {sum_len}")
        if rewrite_type == "带机器人回复":
            converted_input = ''.join([f"{'User:' if i % 2 == 0 else 'Assistant:'}\
                                       {message.content[i]}\n" for i in range(len(message.content))])
        else:
            converted_input = ''.join([f"User1: {message.content[i]}\n" for i in range(0, len(message.content), 2)])
        message.content = converted_input

        return super().run(message=message, rewrite_type=rewrite_type, stream=stream, temperature=temperature, top_p=top_p)
