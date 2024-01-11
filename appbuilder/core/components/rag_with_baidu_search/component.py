import json
import logging

from appbuilder.core.component import ComponentArguments
from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.message import Message
from pydantic import Field


class BaiduSearchArgs(ComponentArguments):
    """
    百度search提示词配置
    """
    message: Message = Field(...,
                             variable_name="message",
                             description="输入用户query，例如'千帆平台都有哪些大模型？'")
    context_out: str = Field(...,
                             variable_name="context_out",
                             description="搜索结果"
                                         "例如：大语言模型（LLM"
                                         "）是基于海量文本数据训练的深度学习模型。它不仅能够生成自然语言文本，还能够深入理解文本含义，"
                                         "处理各种自然语言任务，如文本摘要、问答、翻译等。")
    refuse: bool = Field(...,
                         variable_name="refuse",
                         description="控制大模型拒答能力的开关，为true即为开启拒答功能，为false即为关闭拒答功能")
    clarification: bool = Field(...,
                                variable_name="clarification",
                                description="控制大模型澄清能力的开关，为true即为开启澄清反问功能，为false即为关闭澄清反问功能")
    emphasis: bool = Field(...,
                           variable_name="emphasis",
                           description="控制大模型重点强调能力的开关，为true即为开启重点强调功能，为false即为关闭重点强调功能")
    friendliness: bool = Field(...,
                               variable_name="friendliness",
                               description="控制大模型友好对提升难过能力的开关，"
                                           "为true即为开启友好度提升功能，为false即为关闭友好度提升功能")
    reference: bool = Field(...,
                            variable_name="reference",
                            description="控制大模型溯源能力的开关，为true即为开启溯源功能，为false即为关闭溯源功能")

    __system__: str = Field(...,
                            variable_name="instruction",
                            description="系统人设")


class RAGWithBaiduSearch(CompletionBaseComponent):
    name = "rag_with_baidu_search"
    version = "v1"
    meta: BaiduSearchArgs

    def __init__(self, model=None):
        """初始化MRC(阅读理解问答)模型。

        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。

        Returns:
            None

        """
        super().__init__(BaiduSearchArgs, model=model)

    @staticmethod
    def __get_instruction_set():
        """
        return: json格式的instruction_set
        """
        return {"refuse": "如果答案不在搜索结果中得到，则在答案开头说明："
                          "“当前文档库找不到对应的答案，我可以尝试用我的常识来回答你”，"
                          "并基于你的常识给出答案。",
                "clarification": "当问题比较模糊，而检索结果包含多种可能的答案时，反向提问用户想问的具体内容，"
                                 "让用户补充关键信息后以完整的query重新发问。",
                "emphasis": "可以对答案中的核心部分进行markdown加粗（**加粗内容**）。",
                "friendliness": "答案尽量用礼貌用语开头，涉及到条目列举的内容需要在前面加序号并做分点描述，"
                                "必要时可在每一点前面做小标题的汇总，并可以用总-分-总的形式展示分点式答案内容，使得答案内容可读性更强。",
                "reference": "使用引用标记来标注回答内容参考的搜索结果序号，例如^[1]^ (引用单个搜索结果）,^[1][2]^（引用多个搜索结果），"
                             "其中方括号中的数字是搜索结果序号。引用标记只能出现在句尾标点符号前。",
                "__system__": "你是问答助手，在回答问题前需要加上“很高兴为您解答：”"
                }

    def run(self, message, refuse=False, clarification=False,
            emphasis=False, friendliness=False, reference=False, stream=False, temperature=1e-10, instruction=None):
        instruction_set = self.__get_instruction_set()

        inputs = {
            "refuse": instruction_set["refuse"] if refuse else None,
            "clarification": instruction_set["clarification"] if clarification else None,
            "emphasis": instruction_set["emphasis"] if emphasis else None,
            "friendliness": instruction_set["friendliness"] if friendliness else None,
            "reference": instruction_set["reference"] if reference else None,
            "__system__": instruction
        }
        model_config_inputs = ModelArgsConfig(**{"stream": stream, "temperature": temperature})
        model_config = self.get_model_config(model_config_inputs)
        response_mode = "streaming" if stream else "blocking"
        user_id = message.id

        request = self.gene_request(message.content, inputs, response_mode, user_id, model_config)

        response = self.completion(self.version, self.base_url, request, rag_baidu_search=True)
        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        return response.to_message()
