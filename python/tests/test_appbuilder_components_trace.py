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
import requests
import appbuilder
import os

from appbuilder import AppBuilderTracer

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

class TestAppBuilderComponentsTrace(unittest.TestCase):
    def setUp(self):
        """
        初始化函数，用于设置测试所需的变量和对象。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        self.image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?"\
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6"\
            "064079145ff4698856f477b820147768fc2187d3"
        self.table_ocr = appbuilder.TableOCR()
        self.play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model="ERNIE-3.5-8K")
        model_name = "ERNIE-3.5-8K"
        secret_key = os.getenv('SECRET_KEY', None)
        self.hallucination_detection = appbuilder.HallucinationDetection(model=model_name, secret_key=secret_key)
        
    def test_trace(self):
        """
        测试追踪功能，包括ASR运行、工具评估、playground运行和幻觉检测工具评估。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        tracer=AppBuilderTracer(
            enable_phoenix = True,
            enable_console = True,
        )

        tracer.start_trace()

        # test asr run and tool_eval
        out = self.table_ocr.run(appbuilder.Message(content={"url": self.image_url}))
        print(out)
        result = self.table_ocr.tool_eval(name="asr", streaming=True, file_names=[self.image_url])
        for res in result:
            print(res)

        # test playground run
        msg = appbuilder.Message({
            "name": "小明",
            "bot_name": "机器人",
            "bot_type": "聊天机器人",
            "bot_function": "聊天",
            "bot_question": "你好吗？"
        })

        answer = self.play.run(message=msg, stream=False, temperature=1)

        
        # test hallucination_detection tool_eval
        query = TEST_QUERY
        context = TEST_CONTEXT
        answer = TEST_ANSWER
        model_configs = {'temperature': 0.5, 'top_p': 0.5}
        answer = self.hallucination_detection.tool_eval(name='',
                                                stream=True,
                                                query=query,
                                                context=context,
                                                answer=answer,
                                                model_configs=model_configs)
        for res in answer:
            print(res)
            
        tracer.end_trace()
        
if __name__ == '__main__':
    unittest.main()