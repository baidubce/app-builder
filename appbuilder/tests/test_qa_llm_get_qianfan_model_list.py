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

@unittest.skip("Open api request limit reached")
class TestGetQianfanModelList(unittest.TestCase):
    @parameterized.expand([
        param("", [], False),
        param(os.environ["APPBUILDER_TOKEN"], [], False),

        param("", ["chat"], False),
        param("", ["completions"], False),
        param("", ["embeddings"], False),
        param("", ["text2image"], False),

        param("", ["chat", "completions"], False),
        param("", ["completions", "embeddings"], False),
        param("", ["embeddings", "text2image"], False),
        param("", ["chat", "embeddings"], False),
        param("", ["chat", "text2image"], False),
        param("", ["completions", "text2image"], False),
        param("", ["chat", "completions", "embeddings"], False),
        param("", ["completions", "embeddings", "text2image"], False),
        param("", ["chat", "completions", "embeddings", "text2image"], False),

        param("", ["chat", "completions", "embeddings", "text2image"], True),
        param("", [], True),
    ])
    def test_normal_case(self, secret_key, api_type_filter, is_available):
        """
        正常用例
        """
        models = appbuilder.get_model_list(secret_key=secret_key, api_type_filter=api_type_filter,
                                           is_available=is_available)
        assert len(models)
        time.sleep(0.5)

    def test_chat_models(self):
        """
        正常用例
        """
        secret_key = os.environ["APPBUILDER_TOKEN"]
        api_type_filter = ["chat"]
        is_available = True
        models = appbuilder.get_model_list(secret_key=secret_key, api_type_filter=api_type_filter,
                                           is_available=is_available)
        print(models)
        if models:
            print(len(models))
            assert len(models)

            text = ("用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快"
                    "再见")

            for model_name in models:
                if model_name not in ["Yi-34B-Chat", "ChatLaw", "BLOOMZ-7B", "Qianfan-BLOOMZ-7B-compressed"]:
                    # 前两个不支持，后两个不符合预期
                    print(model_name)
                    builder = appbuilder.DialogSummary(model=model_name)
                    msg = Message(content=text)
                    input_params = {}
                    res = builder(msg, **input_params)
                    content = res.content
                    print("{}：{}".format(model_name, content))
                    assert "诉求" in content
                    assert "回应" in content
                    assert "解决情况" in content
                elif model_name in ["BLOOMZ-7B", "Qianfan-BLOOMZ-7B-compressed"]:
                    print(model_name)
                    builder = appbuilder.DialogSummary(model=model_name)
                    msg = Message(content=text)
                    input_params = {}
                    res = builder(msg, **input_params)
                    content = res.content
                    print("{}：{}".format(model_name, content))
                break
    def test_completions_models(self):
        """
        正常用例
        """
        secret_key = os.environ["APPBUILDER_TOKEN"]
        api_type_filter = ["completions"]
        is_available = True
        # is_available = False
        models = appbuilder.get_model_list(secret_key=secret_key, api_type_filter=api_type_filter,
                                           is_available=is_available)
        print(models)

        if models:
            print(len(models))
            assert len(models)

            text = ("用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快"
                    "再见")

            # models = ["EB-turbo-Pro"]

            for model_name in models:
                print(model_name)
                builder = appbuilder.DialogSummary(model=model_name)
                msg = Message(content=text)
                input_params = {}

                res = builder(msg, **input_params)
                content = res.content
                assert "诉求" in content
                assert "回应" in content
                assert "解决情况" in content
                break

    def test_embeddings_models(self):
        """
        正常用例，embbeding类模型只支持embedding-V1。
        """
        secret_key = os.environ["APPBUILDER_TOKEN"]
        api_type_filter = ["embeddings"]
        is_available = True
        models = appbuilder.get_model_list(secret_key=secret_key, api_type_filter=api_type_filter,
                                           is_available=is_available)
        assert len(models)

        query = "合同中展期利率与罚息利率分别是什么？"
        contexts = ["借款展期部分的利率为年化利率（单利），并按下列方式确定：借款展期期限加上原借款期限达到新的利率期限档次的，从展期之日"
                    "起，借款利息按新的期限档次利率计收，年利率执行2%。",
                    "乙方未按照本协议的约定按期偿还展期借款本息的，甲方有权在展期利率基础上加收1%作为罚息利率，对乙方逾期借款自应还款之日"
                    "（含）起按罚息利率计收利息，并对未按时支付的利息（含罚息）按罚息利率计收复利。",
                    "担保人承诺按照原担保合同的约定继续对借款人在原借款合同和本借款展期协议项下的全部义务承担担保责任。担保人提供的担保为"
                    "保证担保的，保证期间变更为自本协议约定的借款展期到期之日起三年。"]

        for model_name in models:
            if model_name == "Embedding-V1":
                embedding = appbuilder.Embedding(model=model_name)
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
                break
            
    def test_text2image_models(self):
        """
        正常用例
        """
        secret_key = os.environ["APPBUILDER_TOKEN"]
        api_type_filter = ["text2image"]
        is_available = True
        models = appbuilder.get_model_list(secret_key=secret_key, api_type_filter=api_type_filter,
                                           is_available=is_available)
        if models:
            assert len(models)

            text = ("用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快"
                    "再见")

            # models = ["EB-turbo-Pro"]

            for model_name in models:
                builder = appbuilder.DialogSummary(model=model_name)
                msg = Message(content=text)
                input_params = {}
                res = builder(msg, **input_params)
                content = res.content
                assert "诉求" in content
                assert "回应" in content
                assert "解决情况" in content
                break
            time.sleep(1)

    @parameterized.expand([
        # timeout为0
        param("error", [], False),
    ])
    def test_abnormal_case(self, secret_key, api_type_filter, is_available):
        """
        异常用例
        """
        try:
            models = appbuilder.get_model_list(secret_key=secret_key, api_type_filter=api_type_filter,
                                               is_available=is_available)
            print(models)
            assert False, "未捕获到错误信息"
        except Exception as e:
            print(e)
            # assert isinstance(e, eval('ValueError')), "捕获的异常不是预期的类型 实际:{}, 预期:{}".format(e, 'ValueError')
            assert "Authentication error: ( Bearer token invalid )" in str(e)

    
if __name__ == '__main__':
    unittest.main()