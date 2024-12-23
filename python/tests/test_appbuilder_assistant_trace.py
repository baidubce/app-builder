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
from appbuilder import AssistantEventHandler
from tests.pytest_utils import Utils

check_tool = {
    "name": "get_cur_whether",
    "description": "这是一个获得指定地点天气的工具",
    "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "省，市名，例如：河北省"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "摄氏度",
                        "华氏度"
                    ]
                }
            },
        "required": [
                "location"
            ]
    }
}

class MyEventHandler(AssistantEventHandler):
    def get_cur_whether(self, location:str, unit:str):
        return "{} 的当前温度是30 {}".format(location, unit)
    
    def run_begin(self, status_event):
        run_id = self.stream_run_context.current_run_id
        thread_id = self.stream_run_context.current_thread_id
        print("Run_id: {}, Thread_id: {}".format(run_id, thread_id))

    def run_end(self, status_event):
        print("\n", status_event)
        
    def tool_step_begin(self, status_event):
        step_id = self.stream_run_context.current_run_step_id
        print("Step_id: {}".format(step_id))
    
    def tool_calls(self, status_event):
        current_tool_calls = self.stream_run_context.current_tool_calls
        for tool_call in current_tool_calls:
            name = tool_call.function.name
            
            if name == "get_cur_whether":
                arguments = tool_call.function.arguments
                func_res = self.get_cur_whether(**eval(arguments))
                submit_res = appbuilder.assistant.threads.runs.submit_tool_outputs(
                    run_id=self.stream_run_context.current_run_id,
                    thread_id=self.stream_run_context.current_thread_id,
                    tool_outputs=[
                        {"tool_call_id": tool_call.id,
                            "output": func_res,}
                    ]
                )

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

        file_path = Utils.get_data_file("qa_doc_parser_extract_table_from_doc.png")
        file = appbuilder.assistant.assistants.files.create(file_path)

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


        tracer.end_trace()

    def test_appbuilder_assistant_stream_run(self):
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

        file_path = Utils.get_data_file("qa_doc_parser_extract_table_from_doc.png")
        file = appbuilder.assistant.assistants.files.create(file_path)

        thread = appbuilder.assistant.threads.create()
        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world",
            file_ids=[file.id]
        )
        generator = appbuilder.assistant.threads.runs.stream_run(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        for run_step in generator:
            print(run_step)
        
        tracer.end_trace()
            

if __name__ == "__main__":
    unittest.main()