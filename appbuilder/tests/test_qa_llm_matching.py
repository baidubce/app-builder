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

import unittest
import os
import time
import appbuilder
import requests
from parameterized import parameterized, param
import appbuilder
from appbuilder import Message

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

query = "合同中展期利率与罚息利率分别是什么？"
contexts=["借款展期部分的利率为年化利率（单利），并按下列方式确定：借款展期期限加上原借款期限达到新的利率期限档次的，从展期之日起，借款利息"
          "按新的期限档次利率计收，年利率执行2%。",
          "乙方未按照本协议的约定按期偿还展期借款本息的，甲方有权在展期利率基础上加收1%作为罚息利率，对乙方逾期借款自应还款之日（含）起按罚"
          "息利率计收利息，并对未按时支付的利息（含罚息）按罚息利率计收复利。",
          "担保人承诺按照原担保合同的约定继续对借款人在原借款合同和本借款展期协议项下的全部义务承担担保责任。担保人提供的担保为保证担保的，"
          "保证期间变更为自本协议约定的借款展期到期之日起三年。"]

models = appbuilder.get_model_list("", ["chat"], True)

@unittest.skip("Open api request limit reached")
class TestSemanticRankComponent(unittest.TestCase):
    @parameterized.expand([param(model, query, contexts) for model in models if model not in ["Yi-34B-Chat", "ChatLaw",
                                                                                   "BLOOMZ-7B",
                                                                                   "Qianfan-BLOOMZ-7B-compressed"]])
    def test_normal_case(self, model_name, query, contexts):
        """
        正常用例
        """
        embedding = appbuilder.Embedding()
        builder = appbuilder.Matching(embedding)
        # 初始化
        query = Message(content=query)
        contexts = Message(content=contexts)
        # 基于query和文本之间的相似度进行排序
        contexts_ranked = builder(query, contexts)
        log.info(contexts_ranked)
        assert len(contexts_ranked.content) == 3
        # 对query和文本计算相似度
        query_embedding = embedding(query)
        context_embedding = embedding.batch(contexts)
        semantics = builder.semantics(query_embedding, context_embedding)
        log.info(semantics.content)
        assert len(semantics.content) == 3
        for i in range(len(semantics.content)):
            assert semantics.content[i] > 0 and semantics.content[i] < 1
        time.sleep(1)

    @parameterized.expand([
        param(
            "ernie-bot-apaas", 123, contexts, "Invalid"
        ),
        param(
            "ernie-bot-apaas", query, 123, "int"
        ),
    ])
    def test_abnormal_case(self, model_name, query, contexts, err_msg):
        """
        异常用例
        """
        try:
            embedding = appbuilder.Embedding()
            builder = appbuilder.Matching(embedding)
            # 初始化
            query = Message(content=query)
            contexts = Message(content=contexts)
            # 基于query和文本之间的相似度进行排序
            contexts_ranked = builder(query, contexts)
            log.info(contexts_ranked)
            # assert len(contexts_ranked.content) == 3
            # 对query和文本计算相似度
            query_embedding = embedding(query)
            context_embedding = embedding.batch(contexts)
            semantics = builder.semantics(query_embedding, context_embedding)
            log.info(semantics.content)
            # assert len(semantics.content) == 3
            # for i in range(len(semantics.content)):
            #     assert semantics.content[i] > 0 and semantics.content[i] < 1
            assert False, "未捕获到错误信息"
        except Exception as e:
            print(e)
            assert err_msg in str(e), "捕获的异常消息不正确"

    
if __name__ == '__main__':
    unittest.main()