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
文档表格转换
"""
import os
import json

from appbuilder.core.component import Component, Message, ComponentArguments
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class ExtractTableFromDoc(Component):
    """ 文档表格抽取
    
    Examples:

        .. code-block:: python
        
            import os
            import json

            from appbuilder.utils.logger_util import logger
            from appbuilder import Message, ExtractTableFromDoc, DocParser

            # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
            os.environ["APPBUILDER_TOKEN"] = "..."

            # 测试文档解析器使用默认配置，xxx为待解析的文档路径。
            msg = Message("xxx")
            parser = DocParser()
            # ExtractTableFromDoc输入为文档原始解析结果，此处需要带上原始结果，return_raw=True.
            doc = parser(msg, return_raw=True).content.raw

            # 抽取文档中的表格
            parser = ExtractTableFromDoc()
            result = parser.run(Message(doc))

            logger.info("Tables: {}".format(
                json.dumps(result.content, ensure_ascii=False)))
    """
    name: str = "extract_table_from_doc"
    #TODO: 隐藏base_url，@tangwei12统一修改
    base_url = "/rpc/2.0/cloud_hub/v1/ai_engine/copilot_engine/v1/api/doc_search_tools/doc_table_to_markdown_parser"
    meta: ComponentArguments = ComponentArguments(tool_desc={
        "description": "Extract table from doc, table format is markdown",
    })

    def _input_check(self, message: Message, table_max_size, doc_node_num_before_table):
        """ para_check
        """
        if table_max_size < 30:
            raise ValueError("table_max_size mismached, expected table_max_size >= 30, got {}".format(table_max_size))
        if doc_node_num_before_table < 1 or doc_node_num_before_table > 10:
            raise ValueError("doc_node_num_before_table mismatched, expected [1, 10], got {}".format(doc_node_num_before_table))
        obj = message.content.get("result", {}).get("result_list", [])
        if len(obj) < 1:
            raise ValueError("Input check failed, expected raw_doc_parser output.")

    def _post_process(self, resp):
        """ pass
        """
        resp = resp["result"] 
        data = []
        for table in resp.get("mdtables", []):
            tmp = []
            for sub_table in table:
                # print(sub_table["para"])
                sub_table = sub_table.get("para", "").split("表：\n|")
                if len(sub_table) < 2:
                    context = sub_table[0]
                    tmp.append({"para": context[:self.table_max_size]})
                else:
                    context, table_str = sub_table
                    table_str = "|" + table_str
                    remain_len = self.table_max_size - len(table_str)
                    if remain_len < 1:
                        table_str = table_str[:self.table_max_size]
                    else:
                        table_str = context[-remain_len:] + table_str
                    tmp.append({"para": table_str})
            data.append(tmp)
        return data

    @components_run_trace
    def run(self, message: Message, table_max_size: int = 800, doc_node_num_before_table: int = 1):
        """
        将文档原始解析结果，请求云端进行表格抽取，返回表格列表。
        
        Args:
            message (Message): 文档原始解析结果。
            table_max_size (int): 单个表格的长度的最大值(包含上文)，按字符数即len(table_str)统计，默认为800。如果表格超长，则会被拆\
            分成多个子表格，拆分的最小粒度为表格的行。若单行就超长，则会强制按table_max_size截断。截断时会优先截断上文，尽量保留表格内容。
            doc_node_num_before_table (int): 表格前附加的上文DocParser Node的数量，默认为1。范围：1~10。
        
        Returns:
            Message: 返回解析后的消息实体对象
                Message.content (list): 解析出来的文档表格，list(二维)。解析出来的文档表格，如果元素长度为1，则对应原文档中格式化后的\
                长度不超过`table_max_size`的表格；如果元素长度>1，则是对应原文档中一个大表格，该表格被拆分成的多个子表格，以满足设置\
                大小。输出结果数据结构样例：`[[{table1}], [{table2-part1}, {table2-part2}]]`
        
        Raises:
            ValueError: 当输入参数不为文档原始解析结果时，或值不合法时，抛出异常。
        """
        self._input_check(message, table_max_size, doc_node_num_before_table)
        self.table_max_size = table_max_size
        params = {
            "xmind_res": message.content,
            "single_table_size": self.table_max_size,
            "field_before_table_cnt": doc_node_num_before_table
        }
        url = self.http_client.service_url(sub_path="", prefix=self.base_url)
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        resp = self.http_client.session.post(url=url, data=json.dumps(params), headers=headers)

        self.http_client.check_response_header(resp)
        resp = resp.json()
        self.http_client.check_response_json(resp)
        resp = self._post_process(resp)
        return Message(resp)
