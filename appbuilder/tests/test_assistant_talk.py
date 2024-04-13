import unittest
import pydantic
import os
import appbuilder

class TestAssistantTalk(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
        os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"
   
    def test_end_to_end(self):
        assistant_config = appbuilder.AssistantConfig(
            name="技术文档撰写专家",
            description="你是一位优秀的技术文档撰写专家， 给用户提供技术文档写作建议",
            instructions="请将该用户称为王先生，该用户注册了高级会员",
        )

        assistant = appbuilder.assistants.assistants.create(assistant_config)
        conversation = appbuilder.assistants.conversations.create()

        message = appbuilder.assistants.messages.create(
            conversation_id=conversation.id,
            content="请帮我写一份技术文档",
        )

        run_result = appbuilder.assistants.runs.run(
            conversation_id=conversation.id,
            assistant_id=assistant.id,
        )

        print(run_result)


if __name__ == "__main__":
    unittest.main()