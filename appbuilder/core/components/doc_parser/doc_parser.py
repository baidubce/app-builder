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
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.component import Component, Message
from appbuilder.utils.logger_util import logger
from appbuilder.core._client import HTTPClient
from appbuilder.core.components.doc_parser.base import ParserConfig, ParseResult


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

    def set_config(self, config: ParserConfig):
        """
        设置解析配置
        """
        self.config = config

    def make_parse_result(self, response: Dict):
        """
        将解析结果的内容转化成ParseResult的结构
        """
        para_nodes = response["para_nodes"] if response["para_nodes"] is not None else []
        catalog = response["catalog"] if response["catalog"] is not None else []
        pdf_data = response["pdf_data"]
        title_node_ids = [title["node_id"] for title in catalog] if catalog else []
        page_contents = []
        for content in response["file_content"]:
            page_content = {"page_num": content["page_num"], "page_width": int(content["page_size"]["width"]),
                            "page_height": int(content["page_size"]["height"]), "page_angle": int(content["page_angle"]),
                            "page_type": content["page_content"]["type"], "page_layouts": [], "page_titles": [],
                            "page_tables": []}
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
                            row_markdown = "|" + "|".join(
                                [layout_item["children"][index]["text"] for index in set(cell_index)]) + "|"
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
                {"text": title["text"], "type": title["level"], "box": title["position"][0]["box"],
                 "node_id": title["node_id"]})
        parse_result = {"para_node_tree": para_nodes, "page_contents": page_contents, "pdf_data": pdf_data}
        # parse_result = ParseResult.parse_obj(parse_result)
        return parse_result

    @HTTPClient.check_param
    def run(self, input_message: Message, return_raw=False) -> Message:
        """
        对传入的文件进行解析
        参数:
            input_message (Message[str]): 输入为文件的路径
            return_raw (bool): 是否返回云端服务的原始结果
        返回:
            parse_result (Message[ParseResult]): 文件的解析结果。
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
            response = self.http_client.session.post(url=self.http_client.service_url(self.base_url), headers=headers, data=payload)
            self.http_client.check_response_header(response)
            self.http_client.check_response_json(response.json())
            response = response.json()
            if response["error_code"] != 0:
                logger.error("doc parser service log_id {} err {}".format(response["log_id"], response["error_msg"]))
                raise AppBuilderServerException(response["error_msg"])
            parse_result = self.make_parse_result(response["result"]["result_list"][0])
            if return_raw:
                parse_result["raw"] = response

        parse_result = ParseResult.parse_obj(parse_result)
        return Message(parse_result)
