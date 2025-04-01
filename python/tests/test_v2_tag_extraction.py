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
# limitations under the License.import unittest import os

import appbuilder
import os
import unittest
from appbuilder.core.components.v2 import TagExtraction


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestTagExtractionComponent(unittest.TestCase):
    def setUp(self):
        """ 设置环境变量。
        Args:
                无参数，默认值为空。
        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.model_name = "ERNIE-3.5-8K"
        self.tag_extraction = TagExtraction(model=self.model_name)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数"""
        query = "本实用新型公开了一种可利用热能的太阳能光伏光热一体化组件，包括太阳能电池，还包括有吸热板，太阳能电池粘附在吸热板顶面，吸热板内嵌入有热电材料制成的内芯，吸热板底面设置有蛇形管。本实用新型结构紧凑，安装方便，能充分利用太阳能电池散发的热能，具有较高的热能利用率。"
        msg = appbuilder.Message(query)
        answer = self.tag_extraction(msg)
        self.assertIsNotNone(answer)

    def test_run_with_stream_and_temperature(self):
        """测试不同的 stream 和 temperature 参数值"""
        msg = appbuilder.Message(
            "本实用新型公开了一种可利用热能的太阳能光伏光热一体化组件，包括太阳能电池，还包括有吸热板，太阳能电池粘附在吸热板顶面，吸热板内嵌入有热电材料制成的内芯，吸热板底面设置有蛇形管。本实用新型结构紧凑，安装方便，能充分利用太阳能电池散发的热能，具有较高的热能利用率。")
        answer = self.tag_extraction(msg, stream=False, temperature=0.5)
        self.assertIsNotNone(answer)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        query = "本实用新型公开了一种可利用热能的太阳能光伏光热一体化组件，包括太阳能电池，还包括有吸热板，太阳能电池粘附在吸热板顶面，吸热板内嵌入有热电材料制成的内芯，吸热板底面设置有蛇形管。本实用新型结构紧凑，安装方便，能充分利用太阳能电池散发的热能，具有较高的热能利用率。"
        result = self.tag_extraction.tool_eval(query=query)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)
        result = self.tag_extraction.tool_eval(query=query)
        res = [item for item in result]

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        with self.assertRaises(ValueError):
            result = self.tag_extraction.tool_eval(query=None)
            next(result)


if __name__ == '__main__':
    unittest.main()
