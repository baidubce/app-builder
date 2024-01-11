import json
import logging

from appbuilder.core.component import ComponentArguments
from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.message import Message
from pydantic import Field


class RAGWithBaiduSearchArgs(ComponentArguments):
    """
    RAG with Baidusearch提示词配置
    """
    message: Message = Field(...,
                             variable_name="message",
                             description="输入用户query，例如'千帆平台都有哪些大模型？'")
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

    __system__: Message = Field(...,
                                variable_name="instruction",
                                description="系统人设")


class RAGWithBaiduSearch(CompletionBaseComponent):
    name = "rag_with_baidu_search"
    version = "v1"
    meta: RAGWithBaiduSearchArgs

    def __init__(self, model=None):
        """初始化RAG with BaiduSearch组件

        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。

        Returns:
            None

        """
        super().__init__(RAGWithBaiduSearch, model=model)

    @staticmethod
    def __get_instruction_set():
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
                        "其中方括号中的数字是搜索结果序号。引用标记只能出现在句尾标点符号前。"
                }

    def run(self, message, reject=False, clarify=False,
            highlight=False, friendly=False, cite=False, stream=False, temperature=1e-10, top_p=1e-10, instruction=None):
        instruction_set = self.__get_instruction_set()

        inputs = {
            "reject": instruction_set["reject"] if reject else None,
            "clarify": instruction_set["clarify"] if clarify else None,
            "highlight": instruction_set["highlight"] if highlight else None,
            "friendly": instruction_set["friendly"] if friendly else None,
            "cite": instruction_set["cite"] if cite else None,
            "__system__": instruction.content if instruction else None
        }
        model_config_inputs = ModelArgsConfig(**{"stream": stream, "temperature": temperature, "top_p": top_p})
        model_config = self.get_model_config(model_config_inputs)
        response_mode = "streaming" if stream else "blocking"
        user_id = message.id

        request = self.gene_request(message.content, inputs, response_mode, user_id, model_config)

        response = self.completion(self.version, self.base_url, request)
        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        return response.to_message()
