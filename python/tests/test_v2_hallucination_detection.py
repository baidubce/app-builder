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
import os
import unittest
import appbuilder

from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.v2 import HallucinationDetection


TEST_QUERY = '澳门新麻蒲烤肉店每天开门吗？'
TEST_CONTEXT = \
('澳门美食： 澳门新麻蒲韩国烤肉店\n'
'在澳门一年四季之中除了火锅，烤肉也相当受欢迎。提到韩烧，有一间令我印象最深刻，就是号称韩国第一的烤肉店－新麻蒲韩国烤肉店，光是韩国的分店便多'
'达四百多间，海外分店更是遍布世界各地，2016年便落户澳门筷子基区，在原本已经食肆林立的地方一起百花齐放！店内的装修跟韩国分店还完度几乎没差，让'
'食客彷如置身于韩国的感觉，还要大赞其抽风系统不俗，离开时身上都不会沾上烤肉味耶！\n'
'时间：周一至周日 下午5:00 - 上午3:00\n'
'电话：＋853 2823 4012\n'
'地址：澳门筷子基船澳街海擎天第三座地下O号铺96号\n'
'必食推介:\n'
'护心肉二人套餐\n'
'来新麻蒲必试的有两样东西，现在差不多每间烤肉店都有炉边烤蛋，但大家知道吗？原来新麻蒲就是炉边烤蛋的开创者，既然是始祖，这已经是个非吃不可的理'
'由！还有一款必试的就是护心肉，即是猪的横隔膜与肝中间的部分，每头猪也只有200克这种肉，非常珍贵，其味道吃起来有种独特的肉香味，跟牛护心肉一样'
'精彩！\n'
'秘制猪皮\n'
'很多怕胖的女生看到猪皮就怕怕，但其实猪皮含有大量胶原蛋白，营养价值很高呢！这里红通通的猪皮还经过韩国秘制酱汁处理过，会有一点点辣味。烤猪皮的'
'时候也需特别注意火侯，这样吃起来才会有外脆内Q的口感！')
TEST_ANSWER = '澳门新麻蒲烤肉店并不是每天开门，周日休息。'


class TestHallucinationDetectionComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """

        self.hallucination_detection = HallucinationDetection(model="ERNIE-3.5-8K")
    
    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数
        """
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        msg = appbuilder.Message({'query': query, 'context': context, 'answer': answer})
        answer = self.hallucination_detection(msg)
        # print(answer)
        self.assertIsNotNone(answer)
        print(f'\n[result]\n{answer.content}\n')

    def test_run_with_stream_and_temperature(self):
        """测试不同的 stream 和 temperature 参数值
        """
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        msg = appbuilder.Message({'query': query, 'context': context, 'answer': answer})
        answer = self.hallucination_detection(msg, stream=False, temperature=0.5)
        # print(answer)
        self.assertIsNotNone(answer)
        print(f'\n[result]\n{answer.content}\n')

    def test_tool_eval_with_default_params(self):
        """测试 tool_eval 方法使用默认参数
        """
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        answer = self.hallucination_detection.tool_eval(query=query, context=context, answer=answer)
        print(answer)
        self.assertIsNotNone(answer)
        print(f'\n[result]\n{answer}\n')

    def test_tool_eval_with_model_configs(self):
        """测试 tool_eval 方法使用不同temperature和top_p参数值。
        """
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        model_configs = {'temperature': 0.5, 'top_p': 0.5}
        answer = self.hallucination_detection.tool_eval(query=query,
                                                        context=context,
                                                        answer=answer,
                                                        model_configs=model_configs)
        print(answer)
        self.assertIsNotNone(answer)
        print(f'\n[result]\n')
        for ans in answer:
            print(ans)

    def test_tool_eval_with_default_params(self):
        """测试 tool_eval 方法使用默认参数
        """
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        answer = self.hallucination_detection.tool_eval(query=query, context=context, answer=answer)
        print(answer)
        self.assertIsNotNone(answer)
        print(f'\n[result]\n{answer}\n')

    def test_tool_eval_with_model_configs(self):
        """测试 tool_eval 方法使用不同temperature和top_p参数值。
        """
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        model_configs = {'temperature': 0.5, 'top_p': 0.5}
        answer = self.hallucination_detection.tool_eval(query=query,
                                                        context=context,
                                                        answer=answer,
                                                        model_configs=model_configs)
        # print(answer)
        self.assertIsNotNone(answer)
        print(f'\n[result]\n')
        for ans in answer:
            print(ans)


if __name__ == '__main__':
    unittest.main()