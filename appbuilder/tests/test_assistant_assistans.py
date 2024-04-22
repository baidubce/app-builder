import unittest
import os
import appbuilder

class TestAssistantImport(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"

    def test_assistants_create_v1(self):
        from appbuilder.core.assistant.type import assistant_class

        assistant = appbuilder.assistant.assistants.create(
            name="Abc-_123",
            description="test",
        )

        self.assertIsInstance(assistant, assistant_class.AssistantCreateResponse)
        self.assertEqual(assistant.name, "Abc-_123")
        self.assertEqual(assistant.description, "test")


    def test_assistants_create_v2(self):
        try:
            appbuilder.assistant.assistants.create(
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
                name="Abc-_123",
                description="test",
                metadata={
                    "key" * 64 : "value" * 512
                }
            )
        except Exception as e:
            self.assertIn("metadata", e.description)
            

if __name__ == '__main__':
    unittest.main()