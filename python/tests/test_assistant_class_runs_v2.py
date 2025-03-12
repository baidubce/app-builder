import unittest
import os
import appbuilder


def get_cur_whether(location:str, unit:str):
    return "{} 的当前温度是30 {}".format(location, unit)


@unittest.skip("QPS超限")
class TestFunctionCall(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]
        from appbuilder.core.assistant.type import thread_type
        assistant = appbuilder.assistant.assistants.create(
            name="test_assistant",
            description="test assistant",
            instructions="每句话回复前都加上我是秦始皇"
        )

        thread = appbuilder.assistant.threads.create()
        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world",
        )

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        self.thread_id = thread.id
        self.run_id = run_result.id

    def test_run_list_v1(self):
        run_list = appbuilder.assistant.threads.runs.list(
            thread_id=self.thread_id,
            limit=5
        )
        self.assertEqual(len(run_list.data), 1)

    def test_run_query_v1(self):
        run = appbuilder.assistant.threads.runs.query(
            thread_id=self.thread_id,
            run_id=self.run_id
        )
        self.assertEqual(run.status, "completed")
        
    def test_run_step_list_v1(self):
        step_list = appbuilder.assistant.threads.runs.steps.list(
            thread_id=self.thread_id,
            run_id=self.run_id,
        )
        self.assertEqual(len(step_list.data), 1)

        last_step = step_list.data[-1]
        last_step_id = last_step.id

        step = appbuilder.assistant.threads.runs.steps.query(
            thread_id=self.thread_id,
            run_id=self.run_id,
            step_id=last_step_id,
        )
        self.assertEqual(step.id, last_step_id)
        

if __name__ == '__main__':
    unittest.main()
