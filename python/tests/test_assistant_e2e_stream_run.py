import unittest
import pydantic
import os
import time
import appbuilder

@unittest.skip("QPS超限")
class TestAssistantStreamTalk(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_end_to_end(self):
        begin_time = time.time()
        last_time = time.time()
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
        
        run_result = appbuilder.assistant.threads.runs.stream_run(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        for run_step in run_result:
            current_time = time.time()
            print(run_step)
            print("cur step use_time: {} s\n".format(current_time - last_time))
            last_time = current_time

        self.assertIsInstance(run_step, appbuilder.assistant.type.StreamRunStatus)
        self.assertEqual(run_step.status, 'completed')
        end_time = time.time()
        print("total use_time: {} s".format(end_time - begin_time))


if __name__ == "__main__":
    unittest.main()