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

@unittest.skip(reason="暂时跳过")
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

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        print("\nFirst run result: {}\n".format(run_result))

        self.assertEqual(run_result.status, "requires_action")
        self.assertEqual(run_result.required_action.type, "submit_tool_outputs")
        self.assertEqual(len(run_result.required_action.submit_tool_outputs.tool_calls), 1)
        
        tool_call = run_result.required_action.submit_tool_outputs.tool_calls[0]
        
        self.assertEqual(tool_call.type, "function")
        self.assertEqual(tool_call.function.name, "get_cur_whether")
        self.assertEqual(tool_call.function.arguments, '{"location":"北京","unit":"摄氏度"}')

        func_res = get_cur_whether(**eval(tool_call.function.arguments))
        print("\nFunction result: {}\n".format(func_res))

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
            tool_output={
                "tool_call_id":tool_call.id,
                "output": func_res,
                "run_id": run_result.id
            },
        )
        print("\nFinal run result: {}\n".format(run_result))
        self.assertEqual(run_result.status, "completed")
        self.assertEqual(run_result.required_action, None)
        self.assertEqual(run_result.assistant_id, assistant.id)
        self.assertEqual(run_result.thread_id, thread.id)

if __name__ == "__main__":
    unittest.main()
