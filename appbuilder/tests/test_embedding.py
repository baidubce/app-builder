"""
test ernie bot embedding
"""
import os
import sys
sys.path.append('../..')

import unittest
import asyncio

import appbuilder

import numpy as np

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self.embedding = appbuilder.Embedding()

    def test_run(self):
        embedding_1 = self.embedding("hello world!")
        embedding_2 = self.embedding(appbuilder.Message("hello world!"))
        np.testing.assert_array_almost_equal(embedding_1.content, embedding_1.content, decimal=4)

    def test_batch(self):
        embeddings_1 = self.embedding.batch(
            ["hello", "world", "!"],
        )
        self.assertEqual(len(embeddings_1.content), 3)

        embeddings_2 = self.embedding.batch(
            appbuilder.Message(["hello", "world", "!"])
        )
        np.testing.assert_array_almost_equal(embeddings_1.content, embeddings_2.content, decimal=4)

        embeddings_3 = self.embedding.batch(
            appbuilder.Message([]),
        )
        self.assertListEqual(embeddings_3.content, [])

    def test_arun(self):
        embedding_1 = asyncio.run(self.embedding.arun("hello world!"))
        print(embedding_1.content)

    def test_not_support_model(self):
        try:
            embedding = appbuilder.Embedding(model="foo")
        except Exception as e:
            from appbuilder.core._exception import ModelNotSupportedException
            assert isinstance(e, ModelNotSupportedException)
            msg = str(e)
            assert "Model foo not supported" in msg

if __name__ == '__main__':
    unittest.main()
