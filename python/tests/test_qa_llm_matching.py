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
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestSemanticRankComponent(unittest.TestCase):
    def test_normal_case(self):
        query = "合同中展期利率与罚息利率分别是什么？"
        contexts = [
            "借款展期部分的利率为年化利率（单利），并按下列方式确定：借款展期期限加上原借款期限达到新的利率期限档次的，从展期之日起，借款利息"
            "按新的期限档次利率计收，年利率执行2%。",
            "乙方未按照本协议的约定按期偿还展期借款本息的，甲方有权在展期利率基础上加收1%作为罚息利率，对乙方逾期借款自应还款之日（含）起按罚"
            "息利率计收利息，并对未按时支付的利息（含罚息）按罚息利率计收复利。",
            "担保人承诺按照原担保合同的约定继续对借款人在原借款合同和本借款展期协议项下的全部义务承担担保责任。担保人提供的担保为保证担保的，"
            "保证期间变更为自本协议约定的借款展期到期之日起三年。"
        ]

        query_message = appbuilder.Message(content=query)
        contexts_message = appbuilder.Message(content=contexts)

        embedding = appbuilder.Embedding()
        matching = appbuilder.Matching(embedding)
        out_matching = matching(query_message, contexts_message)
        
        query_embedding = embedding(query_message)
        context_embeddings = embedding.batch(contexts_message)
        out_semantics = matching.semantics(query_embedding, context_embeddings)

        self.assertEqual(len(out_matching.content), 3)
        self.assertEqual(len(out_semantics.content), 3)
        for score in out_semantics.content:
            self.assertGreater(score, 0)
            self.assertLess(score, 1)


if __name__ == '__main__':
    unittest.main()
