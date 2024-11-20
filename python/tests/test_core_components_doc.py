# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import os
import unittest
import copy

from appbuilder.core.components.doc_crop_enhance.component import DocCropEnhance
from appbuilder.core.components.doc_splitter.component import DocSplitter, ChunkSplitter, TitleSplitter
from appbuilder.core.message import Message
from appbuilder.core.components.doc_parser.base import ParseResult, ParaNode,Position
from appbuilder.core.components.doc_format_converter.component import DocFormatConverter

from appbuilder.core._exception import InvalidRequestArgumentError

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreComponentsDoc(unittest.TestCase):
    def test_doc_crop_enhance_component(self):
        message=Message()
        dce=DocCropEnhance()
        with self.assertRaises(InvalidRequestArgumentError):
            dce.run(message=message,enhance_type=10)
            
    def test_doc_splitter_doc_splitter_DocSplitter(self):
        # test_if not self.splitter_type
        ds=DocSplitter(splitter_type='')
        dr=ParseResult()
        message=Message()
        message.content=dr
        with self.assertRaises(ValueError):
            ds.run(message=message)
        
        #test_splitter_type must be split_by_chunk or split_by_title
        ds=DocSplitter(splitter_type='test')
        with self.assertRaises(ValueError):
            ds.run(message=message)
        
    def test_doc_splitter_doc_splitter_ChunkSplitter(self):
        # test if not isinstance(paser_res, ParseResult)
        cs=ChunkSplitter()
        message=Message()
        with self.assertRaises(ValueError):
            cs.run(message=message)
    
    def test_doc_splitter_doc_splitter_TitleSplitter_run(self):
        # test if not isinstance(paser_res, ParseResult)
        ts=TitleSplitter()
        message=Message()
        with self.assertRaises(ValueError):
            ts.run(input_message=message)
            
    def test_doc_splitter_doc_splitter_TitleSplitter(self):
        pos = Position(
            pageno=1,
            box=[10, 20, 30, 40]
        )
        node=ParaNode(
            node_id=1,
            text='test',
            para_type= 'test',
            parent=None,
            children=[] ,
            position=[pos],
            table =None 
        )
        # test if node.para_type == "head_tail" and test segment.content
        node_head_tail=copy.deepcopy(node)
        node_head_tail.para_type='head_tail'
        message=Message()
        pr=ParseResult(
            para_node_tree=[node,node,node_head_tail]
        )
        message.content=pr
        ts=TitleSplitter()
        ts.run(input_message=message)
        
    def test_doc_format_converter_component_tool_eval(self):
        dfc=DocFormatConverter()
        result=dfc.tool_eval(streaming=False,origin_query='origin_query',page_num='str page')
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)
        result=dfc.tool_eval(streaming=False,origin_query='origin_query',page_num=1)
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)
        result=dfc.tool_eval(streaming=False,origin_query='origin_query',page_num=1,file_name='test')
        with self.assertRaises(InvalidRequestArgumentError):
            next(result)    

            
        
if __name__ == '__main__':
    unittest.main()