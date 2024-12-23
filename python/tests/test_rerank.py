"""
test rerank
"""
import os
import time

import unittest

import appbuilder


class TestReranker(unittest.TestCase):

    def setUp(self):
        self.reranker = appbuilder.Reranker()

    def test_run(self):
        ranked_1 = self.reranker("你好", ["他好", "hello?"])
        time.sleep(1)
        ranked_2 = self.reranker(appbuilder.Message("你好"), appbuilder.Message(["他好", "hello?"]))

        self.assertEqual(ranked_1.content[0]["relevance_score"], ranked_2.content[0]["relevance_score"])
        self.assertEqual(ranked_1.content[1]["relevance_score"], ranked_2.content[1]["relevance_score"])

    def test_not_support_model(self):
        try:
            _ = appbuilder.Reranker(model="foo")
        except Exception as e:
            from appbuilder.core._exception import ModelNotSupportedException
            assert isinstance(e, ModelNotSupportedException)
            msg = str(e)
            assert "Model foo not supported" in msg


if __name__ == '__main__':
    unittest.main()
