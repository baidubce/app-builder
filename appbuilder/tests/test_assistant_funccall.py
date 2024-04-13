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
            name="热心市民",
            description="你是一个热心市民",
            instructions="请回答其他人的问题",
        )

        check_tool = {
            "name": "get_cur_whether",
            "description": "这是一个获得当地天气的工具",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "省，市名，例如：河北省"
                        },
                        "unit": {
                            "type": "string",
                            "enum": [
                                "摄氏度",
                                "华氏度"
                            ]
                        }
                    },
                "required": [
                        "location"
                    ]
            }
        }

        assistant_config.thirdparty_tools.append(check_tool)

        assistant = appbuilder.assistants.assistants.create(assistant_config)
        conversation = appbuilder.assistants.conversations.create()

        message = appbuilder.assistants.messages.create(
            conversation_id=conversation.id,
            content="今天北京的天气怎么样？",
        )

        run_result = appbuilder.assistants.runs.run(
            conversation_id=conversation.id,
            assistant_id=assistant.id,
        )

        print(run_result)


if __name__ == "__main__":
    unittest.main()
