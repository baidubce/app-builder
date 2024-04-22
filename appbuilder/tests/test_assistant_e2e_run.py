import unittest
import pydantic
import os
import appbuilder

class TestAssistantTalk(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"
   
    def test_end_to_end(self):
        assistant = appbuilder.assistant.assistants.create(
            name="test_assistant",
            description="test assistant",
            instructions="每句话回复前都加上我是秦始皇"
        )
        thread = appbuilder.assistant.threads.create(
            [
                {'content': 'hello world'}
            ]
        )

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        self.assertIsInstance(run_result, appbuilder.assistant.type.RunResult)
        self.assertEqual(run_result.assistant_id, assistant.id)
        self.assertEqual(run_result.thread_id, thread.id)
        self.assertEqual(run_result.status, "completed")


if __name__ == "__main__":
    unittest.main()