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

r"""GBI nl2sql component.
"""
from typing import Dict, List
from pydantic import ValidationError

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core.components.gbi.basic import SessionRecord
from appbuilder.core.components.gbi.basic import SUPPORTED_MODEL_NAME
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import SelectTableArgs


class SelectTable(Component):
    """
    gbi 选表
    """

    def __init__(self, 
                 model_name: str, 
                 table_descriptions: Dict[str, str],
                 prompt_template: str = "",
                 **kwargs
                 ):
        """
        创建 GBI 选表对象
        
        Args:
            model_name: 支持的模型名字 ERNIE-Bot 4.0, ERNIE-Bot, ERNIE-Bot-turbo, Qianfan-Agent-Speed-8K
            table_descriptions: 表的描述是个字典，key: 是表的名字, value: 是表的描述，例如:
                                {
                                    "超市营收明细表": "超市营收明细表，包含超市各种信息等",
                                    "product_sales_info": "产品销售表"
                                }
            prompt_template: rompt 模版, 必须包含如下:
                              1. {num} - 表的数量， 注意 {num} 有两个地方出现
                              2. {table_desc} - 表的描述
                              3. {query} - query
                              参考下面的示例:

                            ```
                            你是一个专业的业务人员，下面有{num}张表，具体表名如下:
                            {table_desc}
                            请根据问题帮我选择上述1-{num}种的其中相关表并返回，可以为多表，也可以为单表,
                            返回多张表请用“,”隔开
                            返回格式请参考如下示例：
                            问题:有多少个审核通过的投运单？
                            回答: ```DWD_MAT_OPERATION```
                            请严格参考示例只不要返回无关内容，直接给出最终答案后面的内容，分析步骤不要输出
                            问题:{query}
                            回答:
                            ```
        """
        super().__init__(meta=SelectTableArgs)
        if model_name not in SUPPORTED_MODEL_NAME:
            raise ValueError(
                f"model_name mismatchhed, expected in {SUPPORTED_MODEL_NAME}, got {model_name}"
            )
        self.model_name = model_name
        self.server_sub_path = "/v1/ai_engine/gbi/v1/gbi_select_table"
        self.table_descriptions = table_descriptions
        self.prompt_template = prompt_template

    @components_run_trace
    def run(self,
            message: Message, timeout: int = 60, retry: int = 0) -> Message[List[str]]:
        """
        执行查询操作，返回识别的表名列表。
        
        Args:
            message (Message): 包含查询信息的消息对象。
                - message.content 字典包含以下 key:
                    1. query (str): 用户的问题输入。
                    2. session (list, optional): 对话历史，默认为空列表。
            timeout (int, optional): 超时时间，默认为 60 秒。
            retry (int, optional): 重试次数，默认为 0。
        
        Returns:
            Message[List[str]]: 包含识别出的表名列表的 Message 对象。
        
        Raises:
            ValueError: 如果输入的 message.content 不符合期望的格式，将抛出 ValueError 异常。
        
        """
        try:
            inputs = self.meta(**message.content)
        except ValidationError as e:
            raise ValueError(e)

        response = self._run_select_table(query=inputs.query, session=inputs.session,
                                          prompt_template=self.prompt_template,
                                          table_descriptions=self.table_descriptions,
                                          model_name=self.model_name,
                                          timeout=timeout,
                                          retry=retry)

        rsp_data = response.json()

        return Message(content=rsp_data)

    def _run_select_table(self, query: str, session: List[SessionRecord],
                          prompt_template,
                          table_descriptions: Dict[str, str],
                          model_name: str,
                          timeout: float = None, retry: int = 0):
        """
        使用给定的输入并返回语音识别的结果。

        参数:
            request (obj:`ShortSpeechRecognitionRequest`): 输入请求，这是一个必需的参数。
            timeout (float, 可选): 请求的超时时间。
            retry (int, 可选): 请求的重试次数。

        返回:
            obj:`ShortSpeechRecognitionResponse`: 接口返回的输出消息。
        """

        headers = self.http_client.auth_header()
        headers["Content_Type"] = "application/json"

        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry

        payload = {"query": query,
                   "table_descriptions": table_descriptions,
                   "session": [session_record.dict() for session_record in session],
                   "model_name": model_name,
                   "prompt_template": prompt_template}

        server_url = self.http_client.service_url(sub_path=self.server_sub_path)
        response = self.http_client.session.post(url=server_url, headers=headers,
                                                 json=payload, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)

        request_id = self.http_client.response_request_id(response)
        response.request_id = request_id
        return response
