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
from appbuilder import AppBuilderTracer

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderTrace(unittest.TestCase):
    def setUp(self):
        """
        设置测试环境所需的变量。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_appbuilder_assistant_trace(self):
        """
        测试AppBuilder Assistant的追踪功能。
        
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

        assistant = appbuilder.assistant.assistants.create(
            name="test_assistant",
            description="test assistant",
            instructions="每句话回复前都加上我是秦始皇"
        )

        file = appbuilder.assistant.assistants.files.create(
            "./data/qa_doc_parser_extract_table_from_doc.png"
        )

        thread = appbuilder.assistant.threads.create()
        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world",
            file_ids=[file.id]
        )

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        generator = appbuilder.assistant.threads.runs.stream_run(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        tracer.end_trace()

if __name__ == "__main__":
    unittest.main()