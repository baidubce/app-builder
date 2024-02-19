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

from appbuilder.core.component import Component, ComponentArguments
from appbuilder.core.message import Message
from appbuilder.core.utils import ModelInfo


class Excel2FigureArgs(ComponentArguments):
    """
    excel2figure 的参数
    """
    query: str = Field(..., description="用户的 query 输入")
    excel_file_url: AnyUrl = Field(..., description="用户的 excel 文件地址，需要是一个可被公网下载的 URL 地址")


class Excel2Figure(Component):
    meta = Excel2FigureArgs

    def __init__(self, model_name: str):
        super().__init__(meta=Excel2FigureArgs)
        self.model_name = model_name
        self.model_info = ModelInfo(client=self.http_client)
        self.server_sub_path = "/v1/ai_engine/copilot_engine/v1/api/agent/excel2figure"

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
                query=inputs.query, excel_file_url=inputs.excel_file_url, model_name=self.model_name)
        return result_msg

    def _run_excel2figure(self, query: str, excel_file_url: str, model_name: str):
        """
        运行
        Args:
            query: query
            excel_file_url: 用户的 excel 文件地址
            model_name: 模型名字

        Returns:
            message
        """
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        with tempfile.TemporaryDirectory() as tmpdir:
            # download excel file
            try:
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

            model_url = self.model_info.get_model_url(model_name)
            payload = {
                "query": query,
                "response_mode": "blocking",
                "user": str(uuid.uuid4()),
                "inputs": {
                    "code_interpreter.files": [{
                        "url": excel_file_url,
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
        print(server_url)
        response = self.http_client.session.post(
                url=server_url, headers=headers, json=payload)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)

        figure_url = ""
        try:
            figure_url = data["result"]["content"][-1]["text"]["extra"]["files"][0]
        except Exception as e:
            logging.warning(
                    f"failed to generate figure for query={query}, excel_file_url={excel_file_url}")
        return Message(figure_url)
