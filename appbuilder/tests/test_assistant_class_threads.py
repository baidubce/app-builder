import unittest
import os
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestThreadCreate(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_threads_create_v1(self):
        from appbuilder.core.assistant.type import thread_type
        thread = appbuilder.assistant.threads.create()
        self.assertIsInstance(thread, thread_type.ThreadCreateResponse)


    def test_threads_create_v2(self):
        from appbuilder.core.assistant.type import thread_type
        message = thread_type.AssistantMessage(
            content="hello world"
        )
        thread = appbuilder.assistant.threads.create([message])
        self.assertIsInstance(thread, thread_type.ThreadCreateResponse) 

    def test_threads_create_v3(self):
        from appbuilder.core.assistant.type import thread_type
        message = thread_type.AssistantMessage(
            content="hello world"
        )

        with self.assertRaises(ValueError):
            appbuilder.assistant.threads.create(message)

if __name__ == '__main__':
    unittest.main()