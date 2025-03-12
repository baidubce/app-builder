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
from appbuilder.core.component import ComponentArguments
from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.message import Message
from pydantic import Field
from typing import Optional
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

from .model import RAGWithBaiduSearchArgs


class RAGWithBaiduSearch(CompletionBaseComponent):
    name = "rag_with_baidu_search"
    version = "v1"
    meta: RAGWithBaiduSearchArgs

    def __init__(
        self, 
        model, 
        secret_key: Optional[str] = None, 
        gateway: str = "",
        lazy_certification: bool = False,
        instruction: Optional[Message] = None, 
        reject: Optional[bool] = False, 
        clarify: Optional[bool] = False, 
        highlight: Optional[bool] = False, 
        friendly: Optional[bool] = False, 
        cite: Optional[bool] = False, 
        **kwargs
    ):
        """初始化RAG with BaiduSearch组件

        Args:
            model (str): 模型名称，用于指定要使用的千帆模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
            instruction (Message, 可选): 人设指令，默认为空
            reject (bool, 可选): 是否开启拒绝回答开关，默认为False
            clarify (bool, 可选): 是否开启澄清开关，默认为False
            highlight (bool, 可选): 是否开启高亮开关，默认为False
            friendly (bool, 可选): 是否开启礼貌回答开关，默认为False
            cite (bool, 可选): 是否开启溯源开关，默认为False

        Returns:
            None

        """
        super().__init__(
                RAGWithBaiduSearchArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)
        self.instruction = instruction
        self.reject = reject
        self.clarify = clarify
        self.highlight = highlight
        self.friendly = friendly
        self.cite = cite

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

    def _get_search_input(self, text):
        """
        获取检索query

        BaiduSearch接口对query有长度要求，需要utf8编码不超过72字节
        """
        max_bytes = 72
        encoded = text.encode('utf-8')
        if len(encoded) <= max_bytes:
            return text

        while max_bytes > 0:
            try:
                return encoded[:max_bytes].decode('utf-8')
            except UnicodeDecodeError:
                max_bytes -= 1
        return ""

    @components_run_trace
    def run(
        self, 
        message, 
        instruction=None, 
        reject=None,
        clarify=None,
        highlight=None,
        friendly=None,
        cite=None,
        stream=False, 
        temperature=1e-10, 
        top_p=1e-10,
    ):
        """
        执行模型推理
        
        Args:
            message (Message): 用户输入的消息对象
            instruction (Instruction, optional): 用户提供的指令信息，默认为None。如果未提供，则使用默认的指令信息。
            reject (bool, optional): 是否拒绝执行，默认为None。如果未提供，则使用默认设置。
            clarify (bool, optional): 是否需要澄清，默认为None。如果未提供，则使用默认设置。
            highlight (bool, optional): 是否高亮显示，默认为None。如果未提供，则使用默认设置。
            friendly (bool, optional): 是否以友好的方式回答，默认为None。如果未提供，则使用默认设置。
            cite (bool, optional): 是否引用原始信息，默认为None。如果未提供，则使用默认设置。
            stream (bool, optional): 是否以流式方式返回结果，默认为False。
            temperature (float, optional): 温度参数，用于控制生成文本的多样性，默认为1e-10。
            top_p (float, optional): 截断概率阈值，用于控制生成文本的多样性，默认为1e-10。
        
        Returns:
            Message: 推理结果消息对象
        
        Raises:
            AppBuilderServerException: 如果输入消息内容过长（超过72个字符）或推理结果中存在错误，则抛出异常。
        """
        instruction_set = self.__get_instruction_set()

        # query 长度限制不能超过 72
        if len(message.content) > 72:
            raise AppBuilderServerException(service_err_message="query is too long, expected <= 72, got {}".format(len(message.content)))
        
        instruction = instruction if instruction is not None else self.instruction
        reject = reject if reject is not None else self.reject
        clarify = clarify if clarify is not None else self.clarify
        highlight = highlight if highlight is not None else self.highlight
        friendly = friendly if friendly is not None else self.friendly
        cite = cite if cite is not None else self.cite

        inputs = {
            "reject": instruction_set["reject"] if reject else None,
            "clarify": instruction_set["clarify"] if clarify else None,
            "highlight": instruction_set["highlight"] if highlight else None,
            "friendly": instruction_set["friendly"] if friendly else None,
            "cite": instruction_set["cite"] if cite else None,
            "instruction": instruction.content if instruction else None,
            "search_input": self._get_search_input(message.content),
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
