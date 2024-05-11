import unittest
import os
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
def get_cur_whether(location:str, unit:str):
    return "{} 的当前温度是30 {}".format(location, unit)


class TestFunctionCall(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_run_create_v1(self):
        from appbuilder.core.assistant.type import thread_type
        assistant = appbuilder.assistant.assistants.create(
            name="test_assistant",
            description="test assistant",
            instructions="每句话回复前都加上我是秦始皇"
        )

        file = appbuilder.assistant.assistants.files.create(
            "./data/qa_doc_parser_extract_table_from_doc.png"
        )

        self.assertIsInstance(file, appbuilder.assistant.type.AssistantFilesCreateResponse)

        thread = appbuilder.assistant.threads.create()
        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world",
            file_ids=[file.id]
        )

        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        self.assertIsInstance(run_result, thread_type.RunResult)
        self.assertEqual(run_result.assistant_id, assistant.id)
        self.assertEqual(run_result.thread_id, thread.id)
        self.assertEqual(run_result.status, "completed")
        self.assertIn("秦始皇", run_result.final_answer.message.content.text.value)

    def test_run_create_v2(self):
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

        with self.assertRaises(ValueError):
            appbuilder.assistant.threads.runs.run(
                assistant_id=assistant.id,
            )

    def test_threads_run_raise(self):
        run=appbuilder.core.assistant.threads.runs.runs.Runs()
        with self.assertRaises(ValueError):
            run._stream(assistant_id='')

if __name__ == '__main__':
    unittest.main()
