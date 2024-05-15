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
excel2figure component
"""
import os
import uuid
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError, AnyUrl
import tempfile
import requests
import logging
import pandas as pd
from appbuilder.core._exception import AppBuilderServerException, ModelNotSupportedException
from appbuilder.core.component import Component, ComponentArguments
from appbuilder.core.message import Message
from appbuilder.core.utils import ModelInfo, ttl_lru_cache


class Excel2FigureArgs(ComponentArguments):
    """
    excel2figure 的参数
    """
    query: str = Field(..., description="用户的 query 输入", max_length=400)
    excel_file_url: AnyUrl = Field(..., description="用户的 excel 文件地址，需要是一个可被公网下载的 URL 地址")


class Excel2Figure(Component):
    meta = Excel2FigureArgs
    model_type: str = "chat"
    excluded_models: List[str] = ["Yi-34B-Chat", "ChatLaw"]
    model_info: ModelInfo = None
    manifests = [
        {
            "name": "excel_to_figure",
            "description": "Excel转图表工具，当用户需要根据Excel图表的数据进行数据分析并绘制图表（柱状图、折线图、雷达图等），使用该工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要根据Excel图表的数据进行数据分析并绘制图表的请求描述。"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    def __init__(
        self, 
        model: str,
        secret_key: Optional[str] = None,
        gateway: str = "",
        lazy_certification: bool = False,
    ):
        super().__init__(
            meta=Excel2FigureArgs, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)
        self.model = model
        if not lazy_certification:
            self._check_model_and_get_model_url(self.model, self.model_type)
        self.server_sub_path = "/v1/ai_engine/copilot_engine/v1/api/agent/excel2figure"

    @ttl_lru_cache(seconds_to_live=1 * 60 * 60) # 1h 
    def set_secret_key_and_gateway(self, secret_key: Optional[str] = None, gateway: str = ""):
        super(Excel2Figure, self).set_secret_key_and_gateway(
                secret_key=secret_key, gateway=gateway)
        self.__class__.model_info = ModelInfo(client=self.http_client)

    @ttl_lru_cache(seconds_to_live=1 * 60 * 60) # 1h 
    def _check_model_and_get_model_url(self, model, model_type):
        if model and model in self.excluded_models:
            raise ModelNotSupportedException(f"Model {model} not supported, expected in {self.excluded_models}")
        if not model:
            raise ValueError("model must be provided")
        if self.__class__.model_info is None:
            self.set_secret_key_and_gateway()
        m_type = self.model_info.get_model_type(model)
        if m_type != model_type:
            raise ModelNotSupportedException(
                f"Model {model} with type [{m_type}] not supported, only support {model_type} type")

        model_url = self.model_info.get_model_url(model)
        return model_url

    def run(self, message: Message) -> Message:
        """
        执行 excel2figure
        Args:
            message: message.content 是字典包含, key 如下:
                1. query: 用户问题
                2. excel_file_url: 用户的 excel 文件地址
        Returns:
            message
        """

        try:
            inputs = self.meta(**message.content)
        except ValidationError as e:
            raise ValueError(e)

        result_msg = self._run_excel2figure(
                query=inputs.query, excel_file_url=inputs.excel_file_url, model=self.model)
        return result_msg

    def _run_excel2figure(self, query: str, excel_file_url: str, model: str, excel_file_name: str = None):
        """
        运行
        Args:
            query: query
            excel_file_url: 用户的 excel 文件地址
            model: 模型名字

        Returns:
            message
        """
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        with tempfile.TemporaryDirectory() as tmpdir:
            # download excel file
            try:
                if excel_file_name:
                    file_name = excel_file_name
                else:
                    file_name = str(uuid.uuid4()) + ".xlsx"
                local_filename = os.path.join(tmpdir, file_name)
                with requests.get(excel_file_url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
            except Exception as e:
                logging.error(f"download file error: {excel_file_url}")
                raise e

            # read file
            df = pd.read_excel(local_filename)
            file_contents = ["打印每一列的名称如下: "]
            file_contents.extend(df.columns)
            file_contents.append("展示每一列的数据样例: ")
            for column in df.columns:
                file_contents.append(column + ": " + ", ".join([str(x) for x in df[column].iloc[:2]]))
            file_contents.append("")
            file_content = "\n".join(file_contents)

            model_url = self._check_model_and_get_model_url(self.model, self.model_type)
            payload = {
                "query": query,
                "response_mode": "blocking",
                "user": str(uuid.uuid4()),
                "inputs": {
                    "code_interpreter.files": [{
                        "url": str(excel_file_url),
                        "name": file_name,
                    }],
                    "code_interpreter.doc_content": file_content,
                },
                "model_configs": {
                    "first_code_gen.url": model_url,
                    "followup_code_gen.url": model_url,
                }
            }

        server_url = self.http_client.service_url(prefix="", sub_path=self.server_sub_path)
        response = self.http_client.session.post(
                url=server_url, headers=headers, json=payload)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)

        figure_url = ""
        try:
            figure_url = data["result"]["content"][-1]["text"][0]
        except Exception as e:
            logging.warning(
                    f"failed to generate figure for query={query}, excel_file_url={excel_file_url}")
        return Message(figure_url)

    def tool_eval(
        self,
        streaming: bool,
        origin_query: str,
		file_urls: dict,
        **kwargs,
    ):
        """
        tool eval
        """
        query = kwargs.get("query", "")
        if not query:
            query = origin_query
        try:
            if len(file_urls) != 1:
                raise ValueError(f"file_urls mismatched, expectd len(file_urls)==1，got {len(file_urls)}") 
            excel_file_name, excel_file_url = list(file_urls.items())[0]
            result_msg = self._run_excel2figure(
            	query=query, 
				excel_file_url=excel_file_url, 
				model=self.model,
				excel_file_name=excel_file_name)
            
            if not result_msg.content:
                raise RuntimeError(f"excel to figure failed, retry after modify query")

            result = {
                'event': 'excel_to_figure',
                'type': 'files',
                'text': [result_msg.content],
            }
        except Exception as e:
            raise RuntimeError(f'excel to figure error：{e}')
            
        if streaming:
            yield result
        else:
            return result
