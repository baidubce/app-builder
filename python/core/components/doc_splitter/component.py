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
对文档进行段落切分
"""
import os
from typing import Dict, Any

from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.doc_parser.base import ParseResult
from appbuilder.core.component import Component, Message, ComponentArguments
from appbuilder.core.components.doc_parser.base import DocSegment
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class DocSplitter(Component):
    """
    文档段落切分组件

    Attributes:
        name (str): 组件名称。
        meta (ComponentArguments): 组件元数据。
    """
    name: str = "doc_to_parapraphs"
    meta: ComponentArguments = ComponentArguments(tool_desc={
        "description": "split data to segments in doc",
    })

    def __init__(self, splitter_type, max_segment_length=800, overlap=200,
                 separators=["。", "！", "？", ".", "!", "?", "……", "|\n"],
                 join_symbol="", **kwargs):
        """
        文档段落切分实例化
        
        Args:
            splitter_type (str): 切分器的类型，目前支持split_by_chunk和split_by_title，为split_by_title时，后续参数无效
            max_segment_length (int, optional): 切分后每个段落的最大长度，默认为800。
            overlap (int, optional): 每个段落和其前后相邻块，首尾重叠两部分的长度，默认为200。
            separators (list, optional): 段落按照最大字符数切分时，字符数超限时，边界用分隔符截断，默认为["。", "！", "？", ".", "!", "?", "……"]。
            join_symbol (str, optional): 文本块拼接时，作为连接符的字符，默认为""。
            **kwargs (Any, optional): 关键字参数。
        
        Returns:
            无
        """
        self.splitter_type = splitter_type

        self.max_segment_length = max_segment_length
        self.overlap = overlap
        self.separators = separators
        self.join_symbol = join_symbol

        super(DocSplitter, self). __init__(meta=self.meta, **kwargs)

    @components_run_trace
    def run(self, message: Message):
        """
        运行函数，根据splitter_type将文档分割成多个部分
        
        Args:
            message (Message): 包含文档内容的消息对象
        
        Returns:
            list: 分割后的文档列表
        
        Raises:
            ValueError: 如果message.content不是ParseResult类型，抛出异常
            ValueError: 如果splitter_type为空，抛出异常
            ValueError: 如果ParseResult不包含原始值，抛出异常
            ValueError: 如果splitter_type不是split_by_chunk或split_by_title，抛出异常
        
        """
        parse_result = message.content
        if not isinstance(parse_result, ParseResult):
            raise ValueError("message.content type must be a ParseResult")

        if not self.splitter_type:
            raise ValueError("splitter_type must be a value")

        if not parse_result.raw:
            raise ValueError("The exceptional purpose:Z to determine whether the ParseResult contains a raw value.\n"
                             "The current value: maybe the value of return_raw is False.\n"
                             "The expected value: the value of return_raw is True.")

        if self.splitter_type == "split_by_chunk":
            xmind_output = parse_result.raw
            # 文档原始的解析结果，作为输入，按照块最大长度，分隔文档
            chunk_splitter = ChunkSplitter(self.max_segment_length, self.overlap, self.separators, self.join_symbol)
            result = chunk_splitter(message)

            return result
        elif self.splitter_type == "split_by_title":
            # 文档原始的解析结果，作为输入，按照标题叶子层级，分隔文档
            title_splitter = TitleSplitter()
            result = title_splitter(message)

            return result
        else:
            raise ValueError("splitter_type must be split_by_chunk or split_by_title")


class ChunkSplitter(Component):
    """
    文档按照块大小切分段落
    
    Examples:

    原始文档：
        贷款资金不得用于从事股本权益性投资，不得用于购买股票、有价证券、期货、理财产品等金融产品。
        不得用于从事房地产经营，不得用于借贷牟取非法收入。不得用于个人或其控制的企业生产经营。
        不得套取现金。不得用于其他违反国家法律、政策规定的领域，不得用于监管机构禁止银行贷款进入的领域。

    切分结果：
        ["贷款资金不得用于从事股本权益性投资，不得用于购买股票、有价证券、期货、理财产品等金融产品。不得用于从事房地产经营，
        不得用于借贷牟取非法收入。不得用于个",
        "不得用于个人或其控制的企业生产经营。不得套取现金。不得用于其他违反国家法律、政策规定的领域，
        不得用于监管机构禁止银行贷款进入的领域。"]
    """

    name: str = "doc_to_chunk"
    meta: ComponentArguments = ComponentArguments(tool_desc={
        "description": "split data to chunks with max size in doc",
    })

    def __init__(self, max_segment_length=800, overlap=200,
                 separators=["。", "！", "？", ".", "!", "?", "……", "|\n"],
                 join_symbol="", **kwargs):
        """
        文档段落切分实例化
        
        Args:
            max_segment_length (int, optional): 切分后每个段落的最大长度，默认为800。
            overlap (int, optional): 每个段落和其前后相邻块，首尾重叠两部分的长度，默认为200。
            separators (list of str, optional): 按照段落最大字符数切分超限时，边界用分隔符截断，默认为["。", "！", "？", ".", "!", "?", "……", "|\n"]。
            join_symbol (str, optional): 文本块拼接时，作为连接符的字符，默认为""。
            **kwargs (Any, optional): 关键字参数。
        
        Returns:
            None
        
        """
        self.base_url = kwargs.get(
            "base_url",
            "/rpc/2.0/cloud_hub/v1/ai_engine/copilot_engine/v1/api/doc_search_tools/xmind_paragraph_splitter")
        kwargs.pop("base_url", "")

        self.max_segment_length = max_segment_length
        self.overlap = overlap
        self.separators = separators
        self.join_symbol = join_symbol

        super(ChunkSplitter, self). __init__(meta=self.meta, **kwargs)

    @components_run_trace
    def run(self, message: Message):
        """
        对输入的解析文档结果，按照最大段落块大小、结尾分隔符等，处理为多个段落结果

        Args:
            message (obj:Message): 上游docparser的文档解析结果

        Returns:
            obj:Message: 文档分隔后的段落结果

        Raises:
            ValueError: 如果 message.content 的类型不是 ParseResult，则抛出 ValueError 异常

        Examples:

        .. code-block:: python

            import os
            from appbuilder import DocParser
            from appbuilder.core.components.doc_splitter.component import DocSplitter, ChunkSplitter
            from appbuilder.core.message import Message

            # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
            os.environ["APPBUILDER_TOKEN"] = "..."

            # 先解析
            msg = Message("./test.pdf")
            parser = DocParser()
            parse_result = parser(msg, return_raw=True)

            # 基于parser的结果切分段落
            splitter = ChunkSplitter()
            res_paras = splitter(parse_result)

            # 打印结果
            print(res_paras.content)
        """
        paser_res = message.content
        if not isinstance(paser_res, ParseResult):
            raise ValueError("message.content type must be a ParseResult")

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        chunk_splitter_remote_params = {"xmind_res": paser_res.raw, "max_segment_length": self.max_segment_length,
                                        "overlap": self.overlap, "separators": self.separators,
                                        "join_symbol": self.join_symbol}

        response = self.http_client.session.post(url=self.http_client.service_url(prefix=self.base_url, sub_path=""),
                                                 headers=headers, json=chunk_splitter_remote_params, stream=False)
        self.http_client.check_response_header(response)
        self.http_client.check_response_json(response.json())
        doc_chunk_splitter_res = response.json()

        return Message(doc_chunk_splitter_res["result"])


class TitleSplitter(Component):
    """ 
    文档按照标题层级切分段落
        
    Examples:

        原始文档：
            一、简介
            叠贷业务是指借款人家庭为满足购房、购车、装修、教育、医疗、旅游、日常消费等符合国家法律法规规定的消费用途。
            二、申请条件
            （一）基本条件
            1、年满18周岁的自然人，具有完全民事行为能力，能提供有效身份证明或居留证明；
            2、有稳定职业和收入，有偿还贷款本息的能力；
            （二）抵押房产所有人的要求
            1、抵押房产的所有人应为借款人本人
            2、抵押房产如有共同所有人，借款人必须为之一，且其他共同所有人必须同意以该房产办理最高额抵押登记，并提供同意抵押的合法有效的书面文件。

        切分结果：
            ["一、简介  叠贷业务是指借款人家庭为满足购房、购车、装修、教育、医疗、旅游、日常消费等符合国家法律法规规定的消费用途。",
            "二、申请条件 （一）基本条件  1、年满18周岁的自然人，具有完全民事行为能力，能提供有效身份证明或居留证明； 2、有稳定职业和收入，
            有偿还贷款本息的能力；"，
            "二、申请条件 （二）抵押房产所有人的要求  1、抵押房产的所有人应为借款人本人。 2、抵押房产如有共同所有人，借款人必须为之一，
            且其他共同所有人必须同意以该房产办理最高额抵押登记，并提供同意抵押的合法有效的书面文件。"】
    """

    name: str = "doc_to_title_level"
    tool_desc: Dict[str, Any] = {"description": "split document content by titles"}

    def _get_title(self, nodes, parent_id, titles):
        """
        获取段落各层级的标题

        参数:
            nodes: 文档的节点树
            parent_id: 当前节点的父节点
            titles: 当前节点的标题, 递归过程中，记录各层级的标题

        返回:
            titles: 当前节点的标题
        """
        def inner_get_titles(nodes, parent_id, titles):
            if parent_id:
                titles.append(nodes[parent_id].text)
                inner_get_titles(nodes, nodes[parent_id].parent, titles)
        inner_get_titles(nodes, parent_id, titles)
        return titles[::-1]

    #  按照标题层级进行切分
    @components_run_trace
    def run(self, input_message: Message) -> Message:
        """
        对输入的解析文档结果，按照各标题层级，处理为多个段落结果
        
        Args:
            input_message (obj:Message): 上游docparser的文档解析结果
        
        Returns:
            obj:Message: 文档分隔后的段落结果
        
        Raises:
            ValueError: 如果message.content的类型不是ParseResult，则抛出异常
        
        Examples:

        .. code-block:: python
        
            import os
            from appbuilder.core.components.doc_parser.doc_parser import DocParser
            from appbuilder.core.components.doc_splitter.doc_splitter import DocSplitter, TitleSplitter
            from appbuilder.core.message import Message

            # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
            os.environ["APPBUILDER_TOKEN"] = "..."

            # 先解析
            msg = Message("./title_splitter.docx")
            parser = DocParser()
            parse_result = parser(msg, return_raw=True)

            # 基于parser的结果切分段落
            splitter = TitleSplitter()
            res_paras = splitter(parse_result)

            # 打印结果
            print(res_paras.content)
        
        """
        parse_result = input_message.content
        if not isinstance(parse_result, ParseResult):
            raise ValueError("message.content type must be a ParseResult")

        para_node_tree = parse_result.para_node_tree
        doc_segments = []
        paragraphs = []
        segment = DocSegment()
        for i in range(1, len(para_node_tree)):
            node = para_node_tree[i]
            #  去掉页眉页脚
            if node.para_type == "head_tail":
                continue

            if node.para_type[:5] != "title":
                segment.content += " " + node.text
                # 下一个node是title或当前node是最后一个node，代表当前的标题层级segment结束
                if i < len(para_node_tree) - 1 and para_node_tree[i + 1].para_type[:5] == "title" or i == len(
                        para_node_tree) - 1:
                    segment.title = self._get_title(para_node_tree, node.parent, [])
                    doc_segments.append(segment)
                    paragraphs_text = " ".join(segment.title) + " " + segment.content
                    paragraphs.append({"text": paragraphs_text, "node_id": i})
                    segment = DocSegment()

        if segment.content:
            segment.title = self._get_title(para_node_tree, node.parent, [])
            doc_segments.append(segment)
            paragraphs_text = " ".join(segment.title) + " " + segment.content
            paragraphs.append({"text": paragraphs_text, "node_id": i})

        return Message({"doc_segments": doc_segments, "paragraphs": paragraphs})
