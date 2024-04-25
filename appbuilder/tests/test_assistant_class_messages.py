import unittest
import os
import appbuilder

class TestMessageCreate(unittest.TestCase):
    def test_messages_create_v1(self):
        from appbuilder.core.assistant.type import thread_type
        thread = appbuilder.assistant.threads.create()
        message = appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world"
        )
        
        self.assertIsInstance(message, thread_type.AssistantMessageCreateResponse) 
        self.assertEqual(message.thread_id, thread.id)


    def test_messages_create_v2(self):
        from appbuilder.core.assistant.type import thread_type
        thread = appbuilder.assistant.threads.create()
        try:
            appbuilder.assistant.threads.messages.create(
                thread_id=thread.id,
                content="hello world",
                role='custom',
                file_ids=["file_id"]*11
            )
        except Exception as e:
            self.assertEqual(e.error_count(), 2)

if __name__ == '__main__':
    unittest.main()