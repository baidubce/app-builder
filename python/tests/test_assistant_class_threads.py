import unittest
import os
import appbuilder

@unittest.skip("QPS超限")
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
            
    def test_threads_query_delete(self):
        from appbuilder.core.assistant.type import thread_type
        message = thread_type.AssistantMessage(
            content="hello world"
        )
        thread = appbuilder.assistant.threads.create([message])
        
        # test query
        thr_query = appbuilder.assistant.threads.query(thread_id=thread.id)
        self.assertIsInstance(thr_query, thread_type.ThreadQueryResponse)
        
        # test update
        with self.assertRaises(TypeError):
            appbuilder.assistant.threads.update(thread_id=thread.id,metadata=123)
        with self.assertRaises(ValueError):
            appbuilder.assistant.threads.update(thread_id=thread.id,metadata={'finish_reason'*10:'513value'})
        with self.assertRaises(ValueError):
            appbuilder.assistant.threads.update(thread_id=thread.id,metadata={'finish_reason':'513value'*64+'A'})
        thr_update = appbuilder.assistant.threads.update(thread_id=thread.id)
        self.assertIsInstance(thr_update, thread_type.ThreadUpdateResponse)
        
        # test delete
        thr_delete = appbuilder.assistant.threads.delete(thread_id=thread.id)
        self.assertIsInstance(thr_delete, thread_type.ThreadDeleteResponse)


if __name__ == '__main__':
    unittest.main()