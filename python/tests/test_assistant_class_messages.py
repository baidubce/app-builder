import unittest
import os
import appbuilder

from appbuilder.core._exception import AssistantServerException

@unittest.skip("QPS超限")
class TestMessageCreate(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

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

        
    def test_messages(self):
        from appbuilder.core.assistant.type import thread_type
        thread = appbuilder.assistant.threads.create()
        msg = appbuilder.assistant.threads.messages.create(
            thread_id=thread.id,
            content="hello world?"
        )

        # test list
        msg_list = appbuilder.assistant.threads.messages.list(
            thread_id=msg.thread_id,
            limit=1
        ) 
        self.assertIsInstance(msg_list, thread_type.AssistantMessageListResponse)  
        
        # test query
        msg_query = appbuilder.assistant.threads.messages.query(
            thread_id=msg.thread_id,
            message_id=msg.id
        )
        self.assertIsInstance(msg_query, thread_type.AssistantMessageQueryResponse)  
            
        # test update
        msg_update= appbuilder.assistant.threads.messages.update(
            thread_id=msg.thread_id,
            message_id=msg.id,
            content='你好'
        )
        self.assertIsInstance(msg_update, thread_type.AssistantMessageUpdateResponse)  
            
        # test file
        msg_files = appbuilder.assistant.threads.messages.files(
            thread_id=msg_update.thread_id,
            message_id=msg_update.id,
            limit=1
        )
        self.assertIsInstance(msg_files, thread_type.AssistantMessageFilesResponse)  


if __name__ == '__main__':
    unittest.main()