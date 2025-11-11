# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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
from appbuilder.core.console.appbuilder_client.data_class import CustomMetadata


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderClientFeedback(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "a3654cd9-378a-4b46-a33b-2259ca3b304e"

    def test_appbuilder_custom_metadata(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败

        Args:
            self (unittest.TestCase): unittest的TestCase对象

        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """
        if len(self.app_id) == 0:
            self.skipTest("self.app_id is empty")
        appbuilder.logger.setLoglevel("ERROR")
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        msg = builder.run(conversation_id, "我要回老家相亲", stream=False, custom_metadata=CustomMetadata(
            override_role_instruction="# 角色任务\n" +
                                         "作为高情商大师，你的主要任务是根据提问，做出最佳的建议。\n" +
                                         "\n" +
                                         "# 工具能力\n" +
                                         "\n" +
                                         "无工具集提供\n" +
                                         "\n" +
                                         "# 要求与限制\n" +
                                         "\n" +
                                         "1. 输出内容的风格为幽默\n" +
                                         "2.输出的字数限制为100字以内",
        ))

        print(msg.content.answer)

    def test_appbuilder_custom_metadata_stream(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败

        Args:
            self (unittest.TestCase): unittest的TestCase对象

        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """
        if len(self.app_id) == 0:
            self.skipTest("self.app_id is empty")
        appbuilder.logger.setLoglevel("ERROR")
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        msg = builder.run(conversation_id, "我要回老家相亲", stream=True, custom_metadata=CustomMetadata(
            override_role_instruction="# 角色任务\n" +
                                         "作为高情商大师，你的主要任务是根据提问，做出最佳的建议。\n" +
                                         "\n" +
                                         "# 工具能力\n" +
                                         "\n" +
                                         "无工具集提供\n" +
                                         "\n" +
                                         "# 要求与限制\n" +
                                         "\n" +
                                         "1. 输出内容的风格为幽默\n" +
                                         "2.输出的字数限制为100字以内",
        ))
        for content in msg.content:
            print(content.answer)


if __name__ == "__main__":
    unittest.main()
