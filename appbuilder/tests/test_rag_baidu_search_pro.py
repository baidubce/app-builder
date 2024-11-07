# -*- coding: utf-8 -*-
"""
@time :    24.5.24  PM3:44
@File:     test_rag_baidu_search_pro
@Author :  baiyuchen
@Version:  python3.8
"""
import os
import unittest
import appbuilder

from appbuilder.core._exception import AppBuilderServerException


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestRagBaiduSearch(unittest.TestCase):

    def setUp(self):
        """
        return rag_with_baidu_search class
        """
        self.model_name = "ERNIE-3.5-8K"
        self.rag_with_baidu_search_pro = appbuilder.RagWithBaiduSearchPro(model=self.model_name)

    def test_rag_with_baidu_search_pro_block(self):
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        is_stream = False
        instruction = "你是问答助手，在回答问题前需要加上“很高兴为您解答：”"
        instruction = appbuilder.Message(instruction)

        answer = self.rag_with_baidu_search_pro(message=msg, stream=is_stream, instruction=instruction)

        self.assertIsNotNone(answer)
        self.assertIsNotNone(answer.content)
        self.assertIsInstance(answer.content, str)
        self.assertTrue(answer.content != "")

        search_baidu = answer.extra.get("search_baidu")
        ref_content = search_baidu[0]["content"]
        self.assertIsNotNone(ref_content)
        self.assertIsInstance(ref_content, str)
        self.assertTrue(ref_content != "")

    def test_rag_with_baidu_search_pro_stream(self):
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        is_stream = True
        instruction = "你是问答助手，在回答问题前需要加上“很高兴为您解答：”"
        instruction = appbuilder.Message(instruction)

        answer = self.rag_with_baidu_search_pro(message=msg, stream=is_stream, instruction=instruction)
        self.assertIsNotNone(answer)

        flag_content = False
        flag_ref_content = False
        for content in answer.content:
            self.assertIsNotNone(content)
            self.assertIsNotNone(answer.extra)

            self.assertIsInstance(content, str)

            if content != "":
                flag_content = True

            search_baidu = answer.extra.get("search_baidu")
            if search_baidu:
                ref_content = search_baidu[0]["content"]
                self.assertIsInstance(ref_content, str)
                if ref_content != "":
                    flag_ref_content = True

        self.assertTrue(flag_content and flag_ref_content)


    def test_rag_with_baidu_search_component_RAGWithBaiduSearch(self):
        rwbs=appbuilder.RAGWithBaiduSearch(model='ERNIE-Bot 4.0')

        # test_get_search_input
        text='text'
        res_text=rwbs._get_search_input(text)
        self.assertEqual(res_text, 'text')
        text='UTF-8是一种变长字节表示的Unicode字符集编码方式，它可以使用1到4个字节来表示一个字符。'
        res_text=rwbs._get_search_input(text)
        self.assertEqual(res_text, 'UTF-8是一种变长字节表示的Unicode字符集编码方式，它可')

        # test run
        message=appbuilder.Message()
        message.content="""
        appbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilder
        appbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilderappbuilder
        """
        with self.assertRaises(AppBuilderServerException):
            rwbs.run(message=message)

if __name__ == '__main__':
    unittest.main()
