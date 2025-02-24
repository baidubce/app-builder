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
        interrupt_ids = []
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        msg = builder.run(conversation_id, "查天气", stream=True)

        interrupt_event_id = None
        for ans in msg.content:
            for event in ans.events:
                if event.content_type == "chatflow_interrupt":
                    assert event.event_type == "chatflow"
                    interrupt_event_id = event.detail.get("interrupt_event_id")
                    break
        self.assertIsNotNone(interrupt_event_id)
        interrupt_ids.append(interrupt_event_id)

        msg = builder.run(
            conversation_id,
            "查航班",
            stream=True,
            action=data_class.Action.create_resume_action(interrupt_event_id),
        )
        interrupt_event_id = None
        for ans in msg.content:
            for event in ans.events:
                if event.content_type == "chatflow_interrupt":
                    assert event.event_type == "chatflow"
                    interrupt_event_id = event.detail.get("interrupt_event_id")
                    break
        self.assertIsNotNone(interrupt_event_id)
        interrupt_ids.append(interrupt_event_id)

        msg2 = builder.run(conversation_id=conversation_id,
                           query="CA1234", stream=True,
                           action=data_class.Action.create_resume_action(interrupt_ids.pop()))
        interrupt_event_id = None
        for ans in msg2.content:
            for event in ans.events:
                if event.content_type == "chatflow_interrupt":
                    assert event.event_type == "chatflow"
                    interrupt_event_id = event.detail.get("interrupt_event_id")
                    interrupt_ids.append(interrupt_event_id)
                    break

        msg2 = builder.run(conversation_id=conversation_id,
                           query="北京的", stream=True,
                           action=data_class.Action.create_resume_action(interrupt_ids.pop()))
        has_multiple_dialog_event = False
        for ans in msg2.content:
            for event in ans.events:
                if event.content_type == "multiple_dialog_event":
                    assert event.event_type == "chatflow"
                    has_multiple_dialog_event = True
                    break
        self.assertTrue(has_multiple_dialog_event)


if __name__ == "__main__":
    unittest.main()
