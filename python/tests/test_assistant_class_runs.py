import unittest
import os
import appbuilder
# from tests.pytest_utils import Utils

import random
import string
import os

class Utils(object):
    """
    utils 方法父类
    """
    @staticmethod
    def get_random_string(str_len, prefix=None):
        """
        生成随机字符串，可指定前缀
        """
        gen_name = ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
        )
        if prefix:
            name = str(prefix) + gen_name
        else:
            name = gen_name
        return name

    @staticmethod
    def get_data_file(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_file_path = os.path.join(current_dir, "data", filename)
        return full_file_path

def get_cur_whether(location:str, unit:str):
    return "{} 的当前温度是30 {}".format(location, unit)

@unittest.skip("QPS超限")
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

        file_path = Utils.get_data_file("qa_doc_parser_extract_table_from_doc.png")
        file = appbuilder.assistant.assistants.files.create(file_path)

        self.assertIsInstance(file, appbuilder.assistant.type.AssistantFilesCreateResponse)

        thread = appbuilder.assistant.threads.create()
        appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world",
            file_ids=[file.id]
        )

        model_parameters = appbuilder.assistant.public_type.AssistantModelParameters(
            chat_parameters = appbuilder.assistant.public_type.AssistantChatParameters(
                temperature = 0.8,
                top_p = 0.8,
                penalty_score = 1.0
                ),
            thought_parameters = appbuilder.assistant.public_type.AssistantThoughtParameters(
                temperature = 0.01,
                top_p = 0.0,
                penalty_score = 1.0
            )
        )
        run_result = appbuilder.assistant.threads.runs.run(
            thread_id=thread.id,
            assistant_id=assistant.id,
            model_parameters=model_parameters
        )

        self.assertIsInstance(run_result, thread_type.RunResult)
        self.assertEqual(run_result.assistant_id, assistant.id)
        self.assertEqual(run_result.thread_id, thread.id)
        self.assertEqual(run_result.status, "completed")
        self.assertIn("我是秦始皇", run_result.final_answer.message.content[0].text.value)

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

    def test_threads_run_model_raise(self):
        run=appbuilder.core.assistant.threads.runs.runs.Runs()
        model_parameters = appbuilder.assistant.public_type.AssistantModelParameters(
            chat_parameters = appbuilder.assistant.public_type.AssistantChatParameters(
                temperature = 0.8,
                top_p = 0.8,
                penalty_score = 1.0
                ),
            thought_parameters = appbuilder.assistant.public_type.AssistantThoughtParameters(
                temperature = 0.01,
                top_p = 0.0,
                penalty_score = 1.0
            )
        )
        with self.assertRaises(ValueError):
            model_parameters.chat_parameters.temperature = 10
            run.run(assistant_id='test', thread_id = 'thread_id', model_parameters = model_parameters)
        with self.assertRaises(ValueError):
            run._stream(assistant_id='test',thread_id = 'thread_id', model_parameters = model_parameters)
        model_parameters.chat_parameters.temperature = 0.8
        with self.assertRaises(ValueError):
            model_parameters.chat_parameters.top_p = 10
            run.run(assistant_id='test', thread_id = 'thread_id', model_parameters = model_parameters)
        with self.assertRaises(ValueError):
            run._stream(assistant_id='test', thread_id = 'thread_id', model_parameters = model_parameters)
        model_parameters.chat_parameters.top_p = 0.8
        with self.assertRaises(ValueError):
            model_parameters.chat_parameters.penalty_score = 10
            run.run(assistant_id='test', thread_id = 'thread_id', model_parameters = model_parameters)
        with self.assertRaises(ValueError):
            run._stream(assistant_id='test',thread_id = 'thread_id', model_parameters = model_parameters)

if __name__ == '__main__':
    unittest.main()
