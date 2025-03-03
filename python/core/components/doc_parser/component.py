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


# -*- coding: utf-8 -*-
"""
文档解析
"""
import os
import json
import base64
from typing import Dict, Any
import tempfile
from urllib.parse import urlparse
import requests
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component, Message
from appbuilder.utils.logger_util import logger
from appbuilder.core._client import HTTPClient
from appbuilder.core.components.doc_parser.base import ParserConfig, ParseResult
from appbuilder.utils.trace.tracer_wrapper import (
    components_run_trace, components_run_stream_trace
)


class DocParser(Component):
    """
    文档解析组件，用于对文档的内容进行解析。

    Examples:

    .. code-block:: python

        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'

        file_path = "./test.pdf" # 待解析的文件路径
        msg = Message(file_path)
        parser = appbuilder.DocParser()
        parse_result = parser(msg)

    """

    name: str = "doc_parser"
    tool_desc: Dict[str, Any] = {"description": "parse document content"}
    base_url: str = "/v1/bce/xmind/parser"
    config: ParserConfig = ParserConfig()

    manifests = [
        {
            "name": "doc_parser",
            "description": "提供文档解析功能，支持PDF、Word、Excel、PPT等文档的解析",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_names": {
                        "type": "array",
                        "description": "用户上传的文档的文件名，包含文件后缀，用于判断文件类型"
                    }
                },
                "required": ["file_names"]
            }
        }
    ]

    def set_config(self, config: ParserConfig):
        """
        设置解析配置
        
        Args:
            config (ParserConfig): 解析配置对象
        
        Returns:
            None
        """
        self.config = config

    def make_parse_result(self, response: Dict):
        """
        将解析结果的内容转化成ParseResult的结构
        
        Args:
            response (Dict): 解析后的响应字典，包含文件内容、目录等信息
        
        Returns:
            Dict: 转换后的ParseResult结构，包含段落节点树、页面内容和PDF数据
        
        """
        para_nodes = (
            response["para_nodes"] if response["para_nodes"] is not None else []
        )
        catalog = response["catalog"] if response["catalog"] is not None else []
        pdf_data = response["pdf_data"]
        title_node_ids = [title["node_id"] for title in catalog] if catalog else []
        page_contents = []
        for content in response["file_content"]:
            page_content = {
                "page_num": content["page_num"],
                "page_width": int(content["page_size"]["width"]),
                "page_height": int(content["page_size"]["height"]),
                "page_angle": int(content["page_angle"]),
                "page_type": content["page_content"]["type"],
                "page_layouts": [],
                "page_titles": [],
                "page_tables": [],
            }
            for layout_item in content["page_content"]["layout"]:
                if layout_item["node_id"] in title_node_ids:
                    continue
                if layout_item["type"] == "table":
                    page_content["page_tables"].append(layout_item)
                    if para_nodes:
                        para_nodes[layout_item["node_id"]]["table"] = layout_item
                        table_row = []
                        for i in range(len(layout_item["matrix"])):
                            cell_index = layout_item["matrix"][i]
                            row_markdown = (
                                "|"
                                + "|".join(
                                    [
                                        layout_item["children"][index]["text"]
                                        for index in set(cell_index)
                                    ]
                                )
                                + "|"
                            )
                            if i != len(layout_item["matrix"]) - 1:
                                row_markdown += "\n"
                            table_row.append(row_markdown)
                        para_nodes[layout_item["node_id"]]["text"] = "".join(table_row)
                else:
                    page_content["page_layouts"].append(layout_item)
            page_contents.append(page_content)

        for title in catalog:
            page_num = title["position"][0]["pageno"]
            page_contents[page_num]["page_titles"].append(
                {
                    "text": title["text"],
                    "type": title["level"],
                    "box": title["position"][0]["box"],
                    "node_id": title["node_id"],
                }
            )
        parse_result = {
            "para_node_tree": para_nodes,
            "page_contents": page_contents,
            "pdf_data": pdf_data,
        }
        # parse_result = ParseResult.parse_obj(parse_result)
        return parse_result

    @HTTPClient.check_param
    @components_run_trace
    def run(self, input_message: Message, return_raw=False) -> Message:
        """
        对传入的文件进行解析
        
        Args:
            input_message (Message[str]): 输入为文件的路径
            return_raw (bool, optional): 是否返回云端服务的原始结果。默认为False。
        
        Returns:
            Message[ParseResult]: 文件的解析结果。
        
        Raises:
            ValueError: 如果传入的文件路径不是字符串类型。
            AppBuilderServerException: 如果文件解析过程中出现异常，将抛出该异常。
        
        """
        file_path = input_message.content

        if not isinstance(file_path, str):
            raise ValueError("file_path should be str type")

        with open(file_path, "rb") as f:
            param = self.config.dict(by_alias=True)
            param["data"] = base64.b64encode(f.read()).decode()
            param["name"] = os.path.basename(file_path)
            payload = json.dumps({"file_list": [param]})
            headers = self.http_client.auth_header()
            headers["Content-Type"] = "application/json"
            response = self.http_client.session.post(
                url=self.http_client.service_url(self.base_url),
                headers=headers,
                data=payload,
            )
            self.http_client.check_response_header(response)
            self.http_client.check_response_json(response.json())
            request_id = self.http_client.response_request_id(response)
            response = response.json()
            if response["error_code"] != 0:
                logger.error(
                    "doc parser service log_id {} err {}".format(
                        response["log_id"], response["error_msg"]
                    )
                )
                raise AppBuilderServerException(
                    request_id=request_id,
                    service_err_code=response["error_code"],
                    service_err_message=response["error_msg"],
                )
            parse_result = self.make_parse_result(response["result"]["result_list"][0])
            if return_raw:
                parse_result["raw"] = response

        parse_result = ParseResult.parse_obj(parse_result)
        return Message(parse_result)

    @components_run_stream_trace
    def tool_eval(self, streaming: bool = False, **kwargs):
        """ tool eval
        """
        return_raw = kwargs.get("return_raw", False)
        file_names = kwargs.get("file_names", [])
        if not file_names:
            raise ValueError("缺少file_names参数")
        file_name = file_names[0]
        file_urls = kwargs.get("file_urls", {})
        if len(file_urls) == 0:
            raise ValueError("file_urls is empty")
        file_url = file_name if file_name.startswith("http") else file_urls.get(file_name, "")

        with tempfile.TemporaryDirectory() as tmp_dir:
            local_filename = os.path.join(tmp_dir, os.path.basename(urlparse(file_url).path))
            # 下载文件
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            input_message = Message(content=local_filename)
            parse_result = self.run(input_message, return_raw)

        result = json.dumps(parse_result.content.model_dump(), ensure_ascii=False)
        if streaming:
            yield result
        else:
            return result
