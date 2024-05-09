import unittest
import os
import appbuilder

from appbuilder.core._exception import AssistantServerException

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestFilesCreate(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]
        
    def test_create_files_v1(self):
        from appbuilder.core.assistant.type import assistant_type
        file_path = "./data/qa_doc_parser_extract_table_from_doc.png"
        file = appbuilder.assistant.assistants.files.create(file_path=file_path)
        self.assertIsInstance(file, assistant_type.AssistantFilesCreateResponse)
        
    def test_create_files_v2(self):
        from appbuilder.core.assistant.type import assistant_type
        file_path = "test"
        with self.assertRaises(ValueError):
            file = appbuilder.assistant.assistants.files.create(file_path=file_path)

    def test_files(self):
        from appbuilder.core.assistant.type import assistant_type
        file_path = "./data/qa_doc_parser_extract_table_from_doc.png"
        file = appbuilder.assistant.assistants.files.create(file_path=file_path)
        
        # test list
        files_list = appbuilder.assistant.assistants.files.list()
        self.assertIsInstance(files_list, assistant_type.AssistantFilesListResponse)
        
        # test query
        files_query = appbuilder.assistant.assistants.files.query(file_id=file.id)
        self.assertIsInstance(files_query, assistant_type.AssistantFilesQueryResponse)
        
        # test delete
        files_delete = appbuilder.assistant.assistants.files.delete(file_id=file.id)
        self.assertIsInstance(files_delete, assistant_type.AssistantFilesDeleteResponse)
        

if __name__ == '__main__':
    unittest.main()
        