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

from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core.message import Message
from appbuilder.core.component import ComponentArguments
from pydantic import Field


class MrcArgs(ComponentArguments):
    """阅读理解问答配置"""
    message: Message = Field(...,
                         variable_name="query",
                         description="输入用户query，例如'千帆平台都有哪些大模型？'")
    context_out_list: list = Field(...,
                                   variable_name="context_out_list",
                                   description="用户输入检索片段list，"
                                               "例如[content1, content2, content3,...]，也可以为空, 即[]")
    reject: bool = Field(...,
                         variable_name="reject",
                         description="控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能")
    clarify: bool = Field(...,
                          variable_name="clarify",
                          description="控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能")
    highlight: bool = Field(...,
                            variable_name="highlight",
                            description="控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能")
    friendly: bool = Field(...,
                           variable_name="friendly",
                           description="控制大模型友好对提升难过能力的开关，"
                                       "为true即为开启友好度提升功能，为false即为关闭友好度提升功能")
    cite: bool = Field(...,
                       variable_name="cite",
                       description="控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能")


class MRC(CompletionBaseComponent):
    """
    阅读理解问答组件，基于大模型进行阅读理解问答，支持拒答、澄清、重点强调、友好性提升、溯源等多种功能，可用于回答用户提出的问题。

    Examples:

        .. code-block:: python

            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            mrc_component = appbuilder.MRC()

            # 获取功能说明
            instructions = mrc_component.get_instruction_set()

            # 输出功能说明
            for key, value in instructions.items():
                print(f"{key}: {value}")

            # 模拟运行MRC组件，开启澄清和友好性提升功能
            result = mrc_component.run(appbuilder.Message("什么是人工智能？"), clarify=True, friendly=True)

            # 输出运行结果
            print(result)

    """
    name = "mrc"
    version = "v1"
    meta: MrcArgs

    def __init__(self, model=None):
        """初始化MRC(阅读理解问答)模型。

        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。

        Returns:
            None

        """
        super().__init__(MrcArgs, model=model)

    def __get_instruction_set(self):
        """
        return: json格式的instruction_set
        """
        return {"reject": "如果答案不在搜索结果中得到，则在答案开头说明："
                          "“当前文档库找不到对应的答案，我可以尝试用我的常识来回答你”，"
                          "并基于你的常识给出答案。",
                "clarify": "当问题比较模糊，而检索结果包含多种可能的答案时，反向提问用户想问的具体内容，"
                           "让用户补充关键信息后以完整的query重新发问。",
                "highlight": "可以对答案中的核心部分进行markdown加粗（**加粗内容**）。",
                "friendly": "答案尽量用礼貌用语开头，涉及到条目列举的内容需要在前面加序号并做分点描述，"
                            "必要时可在每一点前面做小标题的汇总，并可以用总-分-总的形式展示分点式答案内容，使得答案内容可读性更强。",
                "cite": "使用引用标记来标注回答内容参考的搜索结果序号，例如^[1]^ (引用单个搜索结果）,^[1][2]^（引用多个搜索结果），"
                        "其中方括号中的数字是搜索结果序号。引用标记只能出现在句尾标点符号前。"}

    def run(self, message, context_list, reject=False, clarify=False,
            highlight=False, friendly=False, cite=False, stream=False, temperature=1e-10):
        """
        运行阅读理解问答模型并返回结果。

        参数:
            msg (obj:`Message`): 输入消息，包含用户提出的问题。这是一个必需的参数。
            context_list (obj:`Message`):用户输入的问题对应的段落文本列表。这是一个必需的参数
            reject (bool, 可选): 拒答开关，如果为 True，则启用拒答能力。默认为 False。
            clarify (bool, 可选): 澄清开关，如果为 True，则启用澄清能力。默认为 False。
            highlight (bool, 可选): 重点强调开关，如果为 True，则启用重点强调能力。默认为 False。
            friendly (bool, 可选): 友好性提升开关，如果为 True，则启用友好性提升能力。默认为 False。
            cite (bool, 可选): 溯源开关，如果为 True，则启用溯源能力。默认为 False。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

        返回:
            obj:`Message`: 模型运行后的输出消息。
        """
        instruction_set = self.__get_instruction_set()
        context_list = context_list.content
        inputs = {
            "query": message.content,
            "context_out": "\n\n".join(f"[{i + 1}] {s}" for i, s in enumerate(context_list)),
            "reject": instruction_set["reject"] if reject else None,
            "clarify": instruction_set["clarify"] if clarify else None,
            "highlight": instruction_set["highlight"] if highlight else None,
            "friendly": instruction_set["friendly"] if friendly else None,
            "cite": instruction_set["cite"] if cite else None,
        }
        model_config_inputs = ModelArgsConfig(**{"stream": stream, "temperature": temperature})
        model_config = self.get_model_config(model_config_inputs)
        query = inputs["query"]
        response_mode = "streaming" if stream else "blocking"
        user_id = message.id

        request = self.gene_request(query, inputs, response_mode, user_id, model_config)
        response = self.completion(self.version, self.base_url, request)

        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        return response.to_message()

