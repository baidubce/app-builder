import unittest
import os
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAssistant(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]

    def test_assistants_create_v1(self):
        from appbuilder.core.assistant.type import assistant_type

        assistant = appbuilder.assistant.assistants.create(
            model = "ERNIE-4.0-8K",
            name="Abc-_123",
            description="test",
        )

        self.assertIsInstance(assistant, assistant_type.AssistantCreateResponse)
        self.assertEqual(assistant.name, "Abc-_123")
        self.assertEqual(assistant.description, "test")


    def test_assistants_create_v2(self):
        try:
            appbuilder.assistant.assistants.create(
                model = "ERNIE-4.0-8K",
                name="Abc-_123@",
                description="test"*512,
                response_format="other",
                instructions="test"*4096,
                thought_instructions="test"*4096,
                chat_instructions="test"*4096,
                file_ids=["test"]*11,
            )
        except Exception as e:
            self.assertEqual(e.error_count(), 7)

    def test_assistants_create_v3(self):
        try:
            appbuilder.assistant.assistants.create(
                model = "ERNIE-4.0-8K",
                name="Abc-_123",
                description="test",
                metadata={
                    "key" * 64 : "value" * 512
                }
            )
        except Exception as e:
            self.assertIn("metadata", e.description)

            
    def test_Assistant(self):
        from appbuilder.core.assistant.type import assistant_type
        assistant = appbuilder.assistant.assistants.create(
            model = "ERNIE-4.0-8K",
            name="Abc-_123",
            description="test",
        )
        
        # test assistant update
        assistant_update = appbuilder.assistant.assistants.update(
            assistant_id = assistant.id,
            model="ERNIE-4.0-8K",
            name="Test_Name",
            description = "test"
        )
        self.assertIsInstance(assistant_update, assistant_type.AssistantUpdateResponse)
        
        # test assistant list
        assistant_list = appbuilder.assistant.assistants.list()
        self.assertIsInstance(assistant_list, assistant_type.AssistantListResponse)
        
        # test assistant query
        assistant_query = appbuilder.assistant.assistants.query(
            assistant_id = assistant.id,
        )
        self.assertIsInstance(assistant_query, assistant_type.AssistantQueryResponse)
        
        # test assistant mount_files
        # create file
        file_path = "./data/qa_doc_parser_extract_table_from_doc.png"
        file = appbuilder.assistant.assistants.files.create(file_path=file_path)

        assistant_mount = appbuilder.assistant.assistants.mount_files(
            assistant_id = assistant.id,
            file_id = file.id,
        )
        self.assertIsInstance(assistant_mount, assistant_type.AssistantFilesResponse)
        
        # test assistant files list
        assistant_files_list = appbuilder.assistant.assistants.mounted_files_list(
            assistant_id = assistant.id,
        )
        self.assertIsInstance(assistant_files_list, assistant_type.AssistantMountedFilesListResponse)
        self.assertEqual(len(assistant_files_list.data), 1)
        
        # test assistant unmount_files
        assistant_files_delete = appbuilder.assistant.assistants.unmount_files(
            assistant_id = assistant.id,
            file_id = file.id,
        )
        self.assertIsInstance(assistant_files_delete, assistant_type.AssistantFilesDeleteResponse)
        
        # test assistant delete
        assistant_delete = appbuilder.assistant.assistants.delete(
            assistant_id = assistant.id,
        )
        self.assertIsInstance(assistant_delete, assistant_type.AssistantDeleteResponse)
            

if __name__ == '__main__':
    unittest.main()