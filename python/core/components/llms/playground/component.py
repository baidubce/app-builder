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
from typing import Optional
import re

from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core.message import Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace
from .base import PlaygroundArgs

class Playground(CompletionBaseComponent):
    """
    空模板， 支持用户自定义prompt模板，并进行执行

    Examples:

    .. code-block:: python

        import os
        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = "..."

        play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model="Qianfan-Agent-Speed-8K")
        play(appbuilder.Message({"name": "小明", "bot_name": "小红", "bot_type": "聊天机器人", "bot_function": "聊天", "bot_question": "你好吗？"}), stream=False)

    """

    name = "playground"
    version = "v1"
    meta = PlaygroundArgs
    prompt_template = ""
    variable_names = {}

    def __init__(
        self,
        prompt_template=None,
        model=None,
        secret_key: Optional[str] = None,
        gateway: str = "",
        lazy_certification: bool = False,
        **kwargs
    ):
        """初始化空模板配置模型。

        Args:
            prompt_template (str): 输入模板，用于指定prompt格式
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.

        Returns:
            None

        """
        super().__init__(
            PlaygroundArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

        if prompt_template is None:
            prompt_template = "{query}"
        self.prompt_template = prompt_template

        self.variable_names = self.__parse__(prompt_template)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10, top_p=0.0, max_output_tokens=1024, disable_search=True, response_format='text', stop=[], **kwargs):
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (obj:`Message`): 输入消息，用于模型的主要输入内容。这是一个必需的参数。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。
                取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, 可选): 影响输出文本的多样性，取值越大，生成文本的多样性越强。
                取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
            max_output_tokens (int, 可选): 指定生成的文本的最大长度，默认最大输出token数为1024, 最小为2，
                最大输出token与选择的模型有关。
            disable_search (bool, 可选): 是否强制关闭实时搜索功能，默认为 True，表示关闭。
            response_format (str, 可选): 指定返回的消息格式，默认为 'text'，以文本模式返回。
                可选 'json_object'，以 json 格式返回，但可能存在不满足效果的情况。
            stop (list[str], 可选): 生成停止标识，当模型生成结果以 stop 中某个元素结尾时，停止文本生成。
                每个元素长度不超过 20 字符，最多 4 个元素。
        
        Returns:
            obj:`Message`: 模型运行后的输出消息。
        """
        inputs = {}

        if isinstance(message.content, str):
            if len(self.variable_names) == 1:
                inputs[self.variable_names[0]] = message.content

        if isinstance(message.content, dict):
            inputs.update(message.content)

        for key in self.variable_names:
            if key not in inputs:
                raise ValueError(
                    f"Missing input variable {key} in message {message.content}")

        prompt = self.prompt_template.format(**inputs)
        query_message = Message(prompt)
        return super().run(message=query_message, stream=stream, temperature=temperature, top_p=top_p,
                           max_output_tokens=max_output_tokens, disable_search=disable_search, response_format=response_format, stop=stop, **kwargs)

    def __parse__(self, prompt_template):
        last_end = 0
        results = []
        for match in re.finditer(r"{([a-zA-Z_]\w*)}", prompt_template):
            field_name = match.group(1)
            start, end = match.span()

            literal_text = prompt_template[last_end:start]
            last_end = end

            results.append((literal_text, field_name, '', None))

        remaining_literal_text = prompt_template[last_end:]
        if remaining_literal_text:
            results.append((remaining_literal_text, None, None, None))

        input_variables = [v for _, v, _, _ in results if v is not None]

        return input_variables
