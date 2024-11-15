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
import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
from appbuilder.core.console.appbuilder_client.event_handler import (
    AppBuilderEventHandler,
)


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderClientChatflow(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "4403205e-fb83-4fac-96d8-943bdb63796f"

    def test_appbuilder_run_chatflow(self):
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
        appbuilder.logger.setLevel("ERROR")
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        msg = builder.run(conversation_id, "查天气", stream=True)

        interrupt_event_id = None
        for ans in msg.content:
            for event in ans.events:
                if event.content_type == "chatflow_interrupt":
                    assert event.event_type == "chatflow"
                    interrupt_event_id = event.detail.get("interrupt_event_id")

        self.assertIsNotNone(interrupt_event_id)
        msg2 = builder.run(conversation_id=conversation_id,
                           query="我先查个航班动态", stream=True,
                           action=data_class.Action.create_resume_action(interrupt_event_id))
        publish_message = None
        for ans2 in msg2.content:
            for event in ans2.events:
                if event.content_type == "publish_message":
                    publish_message = event.detail.get("message")
        self.assertIsNotNone(publish_message)

    def test_appbuilder_client_run_with_handler(self):
        if len(self.app_id) == 0:
            self.skipTest("self.app_id is empty")
        appbuilder.logger.setLevel("ERROR")
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()

        builder.run_with_handler(
            conversation_id,
            "查天气",
            stream=True,
            event_handler=AppBuilderEventHandler(),
        )

        res2 = builder.run_with_handler(
            conversation_id,
            "我先查个航班动态",
            stream=True,
            event_handler=AppBuilderEventHandler(),
            action_func=data_class.Action.create_resume_action,
        )

        publish_message = None
        for data in res2:
            for event in data.events:
                if event.content_type == "publish_message":
                    publish_message = event.detail.get("message")
        self.assertIsNotNone(publish_message)


if __name__ == "__main__":
    unittest.main()
