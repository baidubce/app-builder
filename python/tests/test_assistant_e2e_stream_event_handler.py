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

class MyEventHandler(AssistantEventHandler):
    def get_cur_whether(self, location:str, unit:str):
        return "{} 的当前温度是30 {}".format(location, unit)
    
    def messages(self, messages_event: StreamRunMessage):
        info = messages_event.content[-1].text.value
        # 使用红色打印
        print("\n\033[1;31m","-> Assistant 回答: ", info, "\033[0m")
    
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


@unittest.skip("QPS超限")
class TestFunctionCall(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_end_to_end_trace(self):
        from appbuilder.utils.trace.tracer import AppBuilderTracer
        tracer=AppBuilderTracer(
            enable_phoenix = True,
            enable_console = False,
            )

        tracer.start_trace()
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
            stream.until_done()

        tracer.end_trace()  

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
            stream.until_done()

if __name__ == "__main__":
    unittest.main()

