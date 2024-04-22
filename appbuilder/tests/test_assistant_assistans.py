import unittest
import os
import appbuilder

class TestAssistantImport(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"

    def test_assistants_create(self):
        
        assistant = appbuilder.assistants.assistants.create(
            name="Abc-_123",
            description="test",
        )