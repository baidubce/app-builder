import unittest
import os
import appbuilder

from appbuilder.core._exception import AssistantServerException
from tests.pytest_utils import Utils

@unittest.skip("QPS超限")
class TestFilesCreate(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = os.environ["APPBUILDER_TOKEN_V2"]
        
    def test_create_files_v1(self):
        from appbuilder.core.assistant.type import assistant_type
        file_path = Utils.get_data_file("qa_doc_parser_extract_table_from_doc.png")
        file = appbuilder.assistant.assistants.files.create(file_path=file_path)
        self.assertIsInstance(file, assistant_type.AssistantFilesCreateResponse)
        
    def test_create_files_v2(self):
        from appbuilder.core.assistant.type import assistant_type
        file_path = "test"
        with self.assertRaises(ValueError):
            file = appbuilder.assistant.assistants.files.create(file_path=file_path)

    def test_files(self):
        from appbuilder.core.assistant.type import assistant_type

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        file_path = os.path.join(data_dir, "qa_doc_parser_extract_table_from_doc.png")
        file = appbuilder.assistant.assistants.files.create(file_path=file_path)
        self.assertIsInstance(file, assistant_type.AssistantFilesCreateResponse)
        
        # test list
        files_list = appbuilder.assistant.assistants.files.list()
        self.assertIsInstance(files_list, assistant_type.AssistantFilesListResponse)
        
        # test query
        with self.assertRaises(TypeError):
            appbuilder.assistant.assistants.files.query(file_id=123)
        with self.assertRaises(ValueError):
            appbuilder.assistant.assistants.files.query(file_id="test")
        files_query = appbuilder.assistant.assistants.files.query(file_id=file.id)
        self.assertIsInstance(files_query, assistant_type.AssistantFilesQueryResponse)
        
        # test content
        with self.assertRaises(TypeError):
            appbuilder.assistant.assistants.files.content(file_id=123)
        with self.assertRaises(FileNotFoundError):
            appbuilder.assistant.assistants.files.content(file_id='test_not_exist')
        files_content=appbuilder.assistant.assistants.files.content(file_id=file.id)
        self.assertIsInstance(files_content, assistant_type.AssistantFilesContentResponse)
        self.assertIsInstance(files_content.content, bytes)
        
        # test download
        with self.assertRaises(TypeError):
            appbuilder.assistant.assistants.files.download(file_id='test', file_path=123)
        with self.assertRaises(TypeError):
            appbuilder.assistant.assistants.files.download(file_id=123, file_path=data_dir)
        with self.assertRaises(FileNotFoundError):
            appbuilder.assistant.assistants.files.download(file_id='test_not_exist', file_path=data_dir)
        with self.assertRaises(ValueError):
            appbuilder.assistant.assistants.files.download(file_id='', file_path=data_dir)
        with self.assertRaises(FileNotFoundError):
            appbuilder.assistant.assistants.files.download(file_id=file.id, file_path=os.path.join(data_dir, 'data/'))
        with self.assertRaises(ValueError):
            try:
                with open(os.path.join(data_dir, 'test'), 'wb') as f:
                    f.write(b'test')
                appbuilder.assistant.assistants.files.download(file_id=file.id, file_path=os.path.join(data_dir, 'test'))
            finally:
                os.remove(os.path.join(data_dir, 'test'))
        
        appbuilder.assistant.assistants.files.download(file_id=file.id, file_path=data_dir)

        # test delete
        files_delete = appbuilder.assistant.assistants.files.delete(file_id=file.id)
        self.assertIsInstance(files_delete, assistant_type.AssistantFilesDeleteResponse)
        

if __name__ == '__main__':
    unittest.main()
        