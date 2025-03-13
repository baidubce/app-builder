import unittest
import pydantic
import os
import appbuilder

def get_cur_whether(location:str, unit:str):
    return "{} 的当前温度是30 {}".format(location, unit)

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

        run_result = appbuilder.assistant.threads.runs.stream_run(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        run_id = ""
        for run_step in run_result:
            print("\nRun result: {}\n".format(run_step))
            if run_step.status == 'queued':
                run_obj = run_step.details.run_object
                run_id = run_obj.id
            elif run_step.status == 'requires_action':
                detail = run_step.details
                tool_call = detail.tool_calls[0]
                func_res = get_cur_whether(**eval(tool_call.function.arguments))
                submit_res = appbuilder.assistant.threads.runs.submit_tool_outputs(
                    run_id=run_id,
                    thread_id=thread.id,
                    tool_outputs=[
                        {"tool_call_id": tool_call.id,
                            "output": func_res,}
                    ]
                )
                self.assertIsInstance(submit_res, appbuilder.assistant.type.RunResult)

        self.assertIsInstance(run_step, appbuilder.assistant.type.StreamRunStatus)
        self.assertEqual(run_step.status, 'completed')
        self.assertEqual(run_step.event_type, 'run_end')

if __name__ == "__main__":
    unittest.main()

