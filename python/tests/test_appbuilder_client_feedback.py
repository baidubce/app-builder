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

import unittest
import os
import appbuilder


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
        self.app_id = "fb64d96b-f828-4385-ba1d-835298d635a9"

    def test_appbuilder_feedback(self):
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
        msg = builder.run(conversation_id, "你能做什么", stream=False)
        message_id = msg.content.message_id
        builder.feedback(
            conversation_id=conversation_id,
            message_id=message_id,
            type="downvote",
            flag=["没有帮助"],
            reason="测试"
        )


if __name__ == "__main__":
    unittest.main()
