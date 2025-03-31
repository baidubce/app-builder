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

from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core.components.llms.mrc.base import MrcArgs
from appbuilder.core.message import Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class MRC(CompletionBaseComponent):
    """
    阅读理解问答组件，基于大模型进行阅读理解问答，支持拒答、澄清、重点强调、友好性提升、溯源等多种功能，可用于回答用户提出的问题。

    Examples:

    .. code-block:: python

        import appbuilder
        import os

        # 设置环境变量
        os.environ["APPBUILDER_TOKEN"] = '...'

        # 创建MRC对象
        mrc_component = appbuilder.MRC()

        #初始化参数
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        context_list = appbuilder.Message(["如何办理残疾人通行证一、残疾人通行证办理条件：
        1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；2、持有准驾车型为C1（听力残疾）、
        C2（左下肢残疾、听力残疾", "3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，
        并有有效交强险凭证，C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
        北京市无障碍环境建设促进中心"])

        # 模拟运行MRC组件，开启拒答、澄清追问、重点强调、友好性提升和溯源能力五个功能
        result = mrc_component.run(msg, context_list, reject=True,
                                    clarify=True, highlight=True, friendly=True, cite=True)

        # 输出运行结果
        print(result)

    """
    name = "mrc"
    version = "v1"
    meta: MrcArgs

    manifests = [
        {
            "name": "mrc",
            "description": "对于输入的问题，基于大模型进行阅读理解问答，支持拒答、澄清、重点强调、友好性提升、溯源等多种功能，可用于回答用户提出的问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "输入用户query，例如'千帆平台都有哪些大模型？'"
                    },
                    "context_list": {
                        "type": "list",
                        "description": "用户输入检索片段list，例如[content1, content2, content3,...]，也可以为空, 即[]"
                    },
                    "reject": {
                        "type": "bool",
                        "description": "控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能"
                    },
                    "clarify": {
                        "type": "bool",
                        "description": "控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能"
                    },
                    "highlight": {
                        "type": "bool",
                        "description": "控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能"
                    },
                    "friendly": {
                        "type": "bool",
                        "description": "控制大模型友好对提升难过能力的开关，为true即为开启友好度提升功能，为false即为关闭友好度提升功能"
                    },
                    "cite": {
                        "type": "bool",
                        "description": "控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能。"
                    }
                },
                "required": [
                    "query",
                    "context_list"
                ]
            }
        }
    ]

    def __init__(
            self,
            model: str = "Qianfan-Agent-Speed-8K",
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = True,
            **kwargs
    ):
        """初始化MRC(阅读理解问答)模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
            MrcArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)

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

    @components_run_trace
    def run(self, message, context_list, reject=False, clarify=False,
            highlight=False, friendly=False, cite=False, stream=False, temperature=1e-10, top_p=0):
        """
        运行阅读理解问答模型并返回结果。
        
        Args:
            message (obj:`Message`): 输入消息，包含用户提出的问题。这是一个必需的参数。
            context_list (obj:`Message`): 用户输入的问题对应的段落文本列表。这是一个必需的参数。
            reject (bool, 可选): 拒答开关，如果为 True，则启用拒答能力。默认为 False。
            clarify (bool, 可选): 澄清开关，如果为 True，则启用澄清能力。默认为 False。
            highlight (bool, 可选): 重点强调开关，如果为 True，则启用重点强调能力。默认为 False。
            friendly (bool, 可选): 友好性提升开关，如果为 True，则启用友好性提升能力。默认为 False。
            cite (bool, 可选): 溯源开关，如果为 True，则启用溯源能力。默认为 False。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, 可选): 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
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
        model_config_inputs = ModelArgsConfig(**{"stream": stream, "temperature": temperature, "top_p": top_p})
        model_config = self.get_model_config(model_config_inputs)
        query = inputs["query"]
        response_mode = "streaming" if stream else "blocking"
        user_id = message.id

        request = self.gene_request(query, inputs, response_mode, user_id, model_config)
        response = self.completion(self.version, self.base_url, request)

        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        return response.to_message()

    @components_run_stream_trace
    def tool_eval(self,
                  query: str,
                  context_list: list,
                  reject: bool = False,
                  clarify: bool = False,
                  highlight: bool = False,
                  friendly: bool = False,
                  cite: bool = False,
                  **kwargs):
        """
        tool_eval for function call
        """
        if not query or not context_list:
            raise ValueError("param `query` and `context_list` are required")
        msg = Message(query)
        context_list_msg = Message(context_list)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get("temperature", 1e-10)
        top_p = model_configs.get("top_p", 0.0)
        message = super().run(
            message=msg, context_list=context_list_msg, reject=reject, clarify=clarify,
            highlight=highlight, friendly=friendly, cite=cite, stream=False, temperature=temperature,
            top_p=top_p
        )

        yield self.create_output(type="text", text=str(message.content), name="text", usage=message.token_usage)
