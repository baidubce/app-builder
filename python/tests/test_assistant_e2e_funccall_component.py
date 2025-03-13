import unittest
import os
import appbuilder


@unittest.skip("QPS超限")
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
                {'type': 'function', 'function': appbuilder.AnimalRecognition().manifests[0]}
            ]
        )
        
        thread = appbuilder.assistant.threads.create()

        image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"

        origin_query = "我有一张图片，url是: {}, 麻烦帮我看看这是什么动物".format(image_url)

        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content=origin_query,
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
        self.assertEqual(tool_call.function.name, "animal_rec")

        print(tool_call.function.arguments)

        func_res = appbuilder.AnimalRecognition().tool_eval(
            name="animal_rec",
            streaming=True,
            origin_query=origin_query,
            **eval(tool_call.function.arguments))
        
        func_message = ""
        for res in func_res:
            func_message += res
        print("\nFunction result: {}\n".format(func_message))

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
            tool_output={
                "tool_call_id":tool_call.id,
                "output": func_message,
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
