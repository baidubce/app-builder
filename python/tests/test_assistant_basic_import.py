import unittest
import os
import appbuilder

@unittest.skip("QPS超限")
class TestAssistantImport(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_assistants_beta_import(self):
        from appbuilder import assistant
        from appbuilder.core.assistant.base import BetaAssistant
        obj = assistant
        self.assertIsInstance(obj, BetaAssistant)

        obj_dir = obj.__dir__()
        self.assertIn("assistants", obj_dir)
        self.assertIn("threads", obj_dir)
    

    def test_assistants_obj_import(self):
        from appbuilder import assistant
        obj = assistant.assistants

        from appbuilder.core.assistant.assistants import Assistants
        self.assertIsInstance(obj, Assistants)

        obj_dir = obj.__dir__()
        self.assertIn("create", obj_dir)

    def test_threads_obj_import(self):
        from appbuilder import assistant
        obj = assistant.threads

        from appbuilder.core.assistant.threads import Threads
        self.assertIsInstance(obj, Threads)

        obj_dir = obj.__dir__()
        self.assertIn("create", obj_dir)

    def test_messages_obj_import(self):
        from appbuilder import assistant
        obj = assistant.threads.messages

        from appbuilder.core.assistant.threads.messages import Messages
        self.assertIsInstance(obj, Messages)
        obj_dir = obj.__dir__()
        self.assertIn("create", obj_dir)

    def test_runs_obj_import(self):
        from appbuilder import assistant
        obj = assistant.threads.runs

        from appbuilder.core.assistant.threads.runs import Runs
        self.assertIsInstance(obj, Runs)

        obj_dir = obj.__dir__()
        self.assertIn("run", obj_dir)
        self.assertIn("stream_run", obj_dir)
        self.assertIn("submit_tool_outputs", obj_dir)
        self.assertIn("cancel", obj_dir)

    def test_type_obj_import(self):
        from appbuilder import assistant
        type_folder = assistant.type
        assistant_type = assistant.assistant_type
        thread_type = assistant.thread_type
        public_type = assistant.public_type

        
if __name__ == '__main__':
    unittest.main()