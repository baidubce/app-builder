"""
test mathcing
"""

import sys

sys.path.append('../..')

import unittest
import os
import appbuilder

class TestMatching(unittest.TestCase):

    def test_example(self):
        # 初始化所需要的组件
        embedding = appbuilder.Embedding()
        matching = appbuilder.Matching(embedding)

        # 定义输入query和文本列表
        query = appbuilder.Message("你好")
        contexts = appbuilder.Message(["世界", "你好"])

        # 根据query，对文本列表做相似度排序
        contexts_matched = matching(query, contexts)
        self.assertListEqual(contexts_matched.content, ['你好', '世界'])

    def test_run(self):
        embedding = appbuilder.Embedding()
        matching = appbuilder.Matching(embedding)

        query = appbuilder.Message("你好")
        contexts = appbuilder.Message(["世界", "你好"])

        contexts_matched = matching(query, contexts)

        self.assertListEqual(
            contexts_matched.content,
            ['你好', '世界']
        )

    def test_return_score(self):
        embedding = appbuilder.Embedding()
        matching = appbuilder.Matching(embedding)

        query = appbuilder.Message("你好")
        contexts = appbuilder.Message(["世界", "你好"])

        contexts_matched = matching(query, contexts, return_score=True)

        scores = [i[0] for i in contexts_matched.content]
        contexts = [i[1] for i in contexts_matched.content]

        self.assertListEqual(
            contexts,
            ['你好', '世界']
        )
        self.assertGreater(scores[0], scores[1])

    def test_semantics(self):
        embedding = appbuilder.Embedding()
        matching = appbuilder.Matching(embedding)

        query = appbuilder.Message("你好")
        query_embedding = embedding(query)

        contexts = appbuilder.Message(["世界", "你好"])
        context_embedding = embedding.batch(contexts)

        semantics = matching.semantics(query_embedding, context_embedding)

        self.assertEqual(len(semantics.content), 2)


if __name__ == '__main__':
    unittest.main()
