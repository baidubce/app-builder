import unittest
import pydantic
import os
import appbuilder
from appbuilder import AssistantEventHandler
from appbuilder.core.assistant.type.thread_type import StreamRunMessage

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

@unittest.skip("QPS超限")
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


class TestFunctionCall(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_end_to_end(self):
        assistant = appbuilder.assistant.assistants.create(
            name="test_function",
            description="你是一个热心的朋友",
            instructions="请用友善的语气回答问题",
            tools=[
                {'type': 'function', 'function': check_tool}
            ]
        )
        
        thread = appbuilder.assistant.threads.create()

        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="今天北京的天气怎么样？",
        )

        with appbuilder.assistant.threads.runs.stream_run_with_handler(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=MyEventHandler(),
        ) as stream:
            for _ in stream:
                ...

if __name__ == "__main__":
    unittest.main()

