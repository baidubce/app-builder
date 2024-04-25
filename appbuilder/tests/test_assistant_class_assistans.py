import unittest
import os
import appbuilder

class TestAssistant(unittest.TestCase):
    def test_assistants_create_v1(self):
        from appbuilder.core.assistant.type import assistant_type

        assistant = appbuilder.assistant.assistants.create(
            name="Abc-_123",
            description="test",
        )

        self.assertIsInstance(assistant, assistant_type.AssistantCreateResponse)
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

    def test_assistants_create_v4(self):
        try:
            appbuilder.assistant.assistants.create(
                name="Abc-_123",
                description="test",
                assistant_id="12345dsdfg"
            )
        except Exception as e:
            print(e)
            self.assertIn("业务逻辑异常", e.description)
            

if __name__ == '__main__':
    unittest.main()