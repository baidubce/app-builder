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
import asyncio
import unittest
import copy
import time
from appbuilder.core.message import Message
from appbuilder import TreeMind

class TestCoreComponentsDoc(unittest.TestCase):
    def setUp(self):
        """
            初始化测试用例，设置环境变量和网关URL。
        如果没有设置CAR_EXPERT_TOKEN环境变量，则使用空字符串。
        Args:
            None.
        Returns:
            None.
        """
        # 从环境变量中提取CarExpert组件的TOKEN
        os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"
        os.environ["GATEWAY_URL"] = "http://10.138.138.29"
        
    def test_treemind_component_tool_eval(self):
        tm = TreeMind()
        query = "生成一份年度总结的思维导图"
        result = tm.tool_eval(query=query)
        for r in result:
            print(r)

    def test_treemind_component_a_tool_eval(self):
        async def inner(tm, query):
            async for item in tm.a_tool_eval(query=query):
                yield item
                
        tm = TreeMind()
        query = "生成一份年度总结的思维导图"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            gen = inner(tm, query)
            while True:
                try:
                    x = loop.run_until_complete(gen.__anext__())
                    print(x)
                except StopAsyncIteration:
                    break
        finally:
            loop.close()
            
    def test_treemind_component_non_stream_tool_eval(self):
        tm = TreeMind()
        query = "生成一份年度总结的思维导图"
        result = tm.non_stream_tool_eval(query=query)
        print(result)

    def test_treemind_component_run(self):
        tm = TreeMind()
        msg = Message(content = "生成一份年度总结的思维导图")
        result = tm.run(msg)
        print(result)

    def test_batch_and_abatch(self):
        tm = TreeMind()
        query1 = Message(content="生成一份年度总结的思维导图")
        query2 = Message(content="生成一份言情小说故事大纲思维导图")
        query3 = Message(content="请帮我按照时间顺序，生成一份2023年重要事件的思维导图")
        query4 = Message(content="生成一份春游攻略的思维导图")
        query5 = Message(content="我需要一份详细的思维导图，涵盖2023年的所有重要事件、成就和目标。")
        query6 = Message(content="我该如何通过思维导图来组织我的2023年年度总结？请提供一些关键点。")
        query7 = Message(content="为了更好地规划2024年，我想生成一份2023年的年度总结思维导图，包括关键里程碑和学习点。")
        query8 = Message(content="设想我是一家公司的CEO，我需要一份展示公司2023年发展的思维导图。")
        query9 = Message(content="我需要一份能够清晰展示2023年个人成长和职业发展的思维导图")
        query10 = Message(content="我想要一份能够唤起我对2023年美好回忆的思维导图。")
        query11 = Message(content="探索一种新颖的方式来呈现我的2023年年度总结，思维导图会是一个好的选择吗？")
        query12 = Message(content="我希望通过思维导图来反思2023年的得失，为新的一年做准备")
        query13 = Message(content="生成一份思维导图，对比2023年与前一年在各个方面的进展和变化。")
        query14 = Message(content="我想要一份视觉吸引力强的思维导图，能够直观展示2023年的关键数据和趋势。")
        query15 = Message(content="请根据我的个人兴趣和职业背景，定制一份2023年的年度总结思维导图。")
        query16 = Message(content="我需要一份综合评估2023年个人和职业生活的年度总结思维导图。")
        query17 = Message(content="如果我要生成一份年度总结的思维导图，我应该从哪些方面入手？")
        time0 = time.time()
        result = tm.batch(query1, query2, query3, query4, query5)
        print(result)
        sync_time = time.time() - time0
        time0 = time.time()
        result = asyncio.run(tm.abatch(query1, query2, query3, query4, query5))
        async_time = time.time() - time0
        print(result)
        print("sync_time: {}, async_time: {}".format(sync_time, async_time))
        assert async_time < sync_time

    def test_arun(self):
        tm = TreeMind()
        result = asyncio.run(tm.arun(Message(content="生成一份年度总结的思维导图")))
        print(result)
            
        
if __name__ == '__main__':
    unittest.main()