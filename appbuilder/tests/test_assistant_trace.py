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
import appbuilder
import os

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderTrace(unittest.TestCase):
    def setUp(self):
        from appbuilder.trace import create_tracer_provider, AppbuilderInstrumentor
        os.environ["APPBUILDER_SDK_TRACER_CONSOLE"] = "True"
        tracer_provider = create_tracer_provider()
        instrumentor=AppbuilderInstrumentor()
        instrumentor.instrument(tracer_provider=tracer_provider)
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_assistant_create_trace(self):
        assistant = appbuilder.assistant.assistants.create(
            model = "ERNIE-4.0-8K",
            name="Abc-_123",
            description="test",
        )
        self.assertEqual(assistant.name, "Abc-_123")
        self.assertEqual(assistant.description, "test")

    def test_file_download_trace(self):
        file_path = "./data/qa_doc_parser_extract_table_from_doc.png"
        file = appbuilder.assistant.assistants.files.create(file_path=file_path)

        appbuilder.assistant.assistants.files.download(file_id=file.id, file_path="./data/")

if __name__ == "__main__":
    unittest.main()
