import os
import unittest
import appbuilder
import json


class TestRagBaiduSearch(unittest.TestCase):

    def setUp(self):
        """
        return rag_with_baidu_search class
        """
        # 设置环境变量和初始化TestMRCComponent实例
        self.model_name = "eb-turbo-appbuilder"
        self.rag_with_baidu_search = appbuilder.RAGWithBaiduSearch(model=self.model_name)

    def test_rag_with_baidu_search(self):
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        is_stream = False
        instruction = "你是问答助手，在回答问题前需要加上“很高兴为您解答："
        answer = self.rag_with_baidu_search(msg, refuse=True, clarification=True, emphasis=True,
                                            friendliness=True, reference=True, temperature=0.5, stream=is_stream,
                                            instruction=instruction)
        self.assertIsNotNone(answer)
        if not is_stream:
            print(answer)
        else:
            for a in answer:
                print(a)
