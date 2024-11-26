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
import unittest
import appbuilder
from appbuilder.core.console.appbuilder_client.event_handler import (
    AppBuilderEventHandler,
)


class MyEventHandler(AppBuilderEventHandler):
    def __init__(self):
        super().__init__()
        self.interrupt_ids = []

    def handle_content_type(self, run_context, run_response):
        interrupt_event_id = None
        event = run_response.events[-1]
        if event.content_type == "chatflow_interrupt":
            interrupt_event_id = event.detail.get("interrupt_event_id")
        if interrupt_event_id is not None:
            self.interrupt_ids.append(interrupt_event_id)

    def _create_action(self):
        if len(self.interrupt_ids) == 0:
            return None
        event_id = self.interrupt_ids.pop()
        return {
            "action_type": "resume",
            "parameters": {"interrupt_event": {"id": event_id, "type": "chat"}},
        }

    def run(self, query=None):
        super().new_dialog(
            query=query,
            action=self._create_action(),
        )


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

    def test_appbuilder_client_run_with_handler_stream(self):
        if len(self.app_id) == 0:
            self.skipTest("self.app_id is empty")
        appbuilder.logger.setLevel("ERROR")
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()

        event_handler = MyEventHandler()
        event_handler.init(appbuilder_client=builder,
                           conversation_id=conversation_id, stream=True, query="查天气")
        for data in event_handler:
            pass
        event_handler.run(
            query="查航班",
        )
        for data in event_handler:
            pass
        event_handler.run(
            query="CA1234",
        )
        for data in event_handler:
            pass
        event_handler.run(
            query="北京的",
        )
        for data in event_handler:
            pass

    def test_appbuilder_client_run_with_handler(self):
        if len(self.app_id) == 0:
            self.skipTest("self.app_id is empty")
        appbuilder.logger.setLevel("ERROR")
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()

        event_handler = MyEventHandler()
        event_handler.init(
            appbuilder_client=builder,
            conversation_id=conversation_id,
            stream=False,
            query="查天气",
        )
        for data in event_handler:
            pass
        event_handler.run(
            query="查航班",
        )
        for data in event_handler:
            pass
        event_handler.run(
            query="CA1234",
        )
        for data in event_handler:
            pass
        event_handler.run(
            query="北京的",
        )
        for data in event_handler:
            pass


if __name__ == "__main__":
    unittest.main()
