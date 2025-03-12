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
from appbuilder.core.components.gbi.basic import ColumnItem
from appbuilder.core.components.gbi.basic import NL2SqlResult
from appbuilder.core.components.gbi.basic import SUPPORTED_MODEL_NAME
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import NL2SqlArgs

class NL2Sql(Component):
    """
    gib nl2sql
    """
    meta = NL2SqlArgs

    def __init__(self, 
                 model_name: str, 
                 table_schemas: List[str], 
                 knowledge: Dict = None,
                 prompt_template: str = "",
                 **kwargs
                 ):
        """
        创建 gbi nl2sql 对象
        
        Args:
            model_name:  支持的模型名字 ERNIE-Bot 4.0, ERNIE-Bot, ERNIE-Bot-turbo, Qianfan-Agent-Speed-8K
            table_schemas: 表的 schema 列表，例如: ```
                            CREATE TABLE `mytable` (
                            `d_year` COMMENT '年度,2019,2020..2022..',
                            `industry` COMMENT '行业',
                            `project_name` COMMENT '项目名称',
                            `customer_name` COMMENT '客户名称')
                            ```"
            knowledge: 用于提供一些知识, 比如 {"毛利率": "毛收入-毛成本/毛成本"}
            prompt_template: prompt 模版, 必须包含的格式如下:
                  ***你的描述
                  {schema}
                  ***你的描述
                  {column_instrument}
                  ***你的描述
                  {kg}
                  ***你的描述
                  当前时间：{date}
                  ***你的描述
                  {history_instrument}
                  ***你的描述
                  当前问题：{query}
                  回答：
        """
        super().__init__(meta=NL2SqlArgs)

        if model_name not in SUPPORTED_MODEL_NAME:
            raise ValueError(f"model_name mismatchhed, expected in {SUPPORTED_MODEL_NAME}, got {model_name}")
        self.model_name = model_name
        self.server_sub_path = "/v1/ai_engine/gbi/v1/gbi_nl2sql"
        self.table_schemas = table_schemas
        self.knowledge = knowledge or dict()
        self.prompt_template = prompt_template

    @components_run_trace
    def run(self,
            message: Message, timeout: float = 60, retry: int = 0) -> Message[NL2SqlResult]:
        """
        执行自然语言转SQL操作。
        
        Args:
            message (Message): 包含用户问题和会话历史的消息对象。
                - message.content 是一个字典，包含以下关键字：
                    1. query: 用户问题
                    2. session: 会话历史列表，参考 SessionRecord
                    3. column_constraint: 列选约束，参考 ColumnItem 具体定义
            timeout (float): 超时时间，默认为60秒。
            retry (int): 重试次数，默认为0次。
        
        Returns:
            Message[NL2SqlResult]: 转换结果以Message对象形式返回，其中content属性包含NL2SqlResult对象。
        
        """
        try:
            inputs = self.meta(**message.content)
        except ValidationError as e:
            raise ValueError(e)

        response = self._run_nl2sql(query=inputs.query, session=inputs.session, table_schemas=self.table_schemas,
                                    column_constraint=inputs.column_constraint, knowledge=self.knowledge,
                                    prompt_template=self.prompt_template,
                                    model_name=self.model_name,
                                    timeout=timeout,
                                    retry=retry)

        rsp_data = response.json()
        nl2sql_result = NL2SqlResult(llm_result=rsp_data["llm_result"],
                                     sql=rsp_data["sql"])
        return Message(content=nl2sql_result)

    def _run_nl2sql(self, query: str, session: List[SessionRecord], table_schemas: List[str], knowledge: Dict[str, str],
                    prompt_template: str,
                    column_constraint: List[ColumnItem],
                    model_name: str,
                    timeout: float = None, retry: int = 0):
        """
        运行
        Args:
            query: query
            session: gbi session 的历史 列表
            table_schemas: 表的 schema 列表
            knowledge: 知识
            prompt_template: prompt 模版
            column_constraint: 列的限制
            model_name: 模型名字
            timeout: 超时时间
            retry:

        Returns:

        """

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry

        payload = {"query": query,
                   "table_schemas": table_schemas,
                   "session": [session_record.dict() for session_record in session],
                   "column_constraint": [column_item.dict() for column_item in column_constraint],
                   "model_name": model_name,
                   "knowledge": knowledge,
                   "prompt_template": prompt_template}

        server_url = self.http_client.service_url(prefix="", sub_path=self.server_sub_path)
        response = self.http_client.session.post(url=server_url, headers=headers,
                                                 json=payload, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)

        request_id = self.http_client.response_request_id(response)
        response.request_id = request_id
        return response
