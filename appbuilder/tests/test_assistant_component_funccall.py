import unittest
import pydantic
import os
import appbuilder

from appbuilder import TableOCR

class TestAssistantTalk(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"

    def test_end_to_end(self):
        assistant_config = appbuilder.AssistantConfig(
            name="表格内容识别专家",
            description="你是一个从不出错的表格内容识别专家，负责从给定的图片中识别出文字内容信息",
            instructions="请在回答任何内容前，加上『我是专家，我认为』",
        )

        assistant_config.thirdparty_tools.append(TableOCR())

        assistant = appbuilder.assistants.assistants.create(assistant_config)
        conversation = appbuilder.assistants.conversations.create()

        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024" \
                    "-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
                    "064079145ff4698856f477b820147768fc2187d3"
        appbuilder.assistants.messages.create(
            conversation_id=conversation.id,
            content="请帮我识别[{}]这张图片中的表格内容".format(image_url),
        )

        run_result = appbuilder.assistants.runs.run(
            conversation_id=conversation.id,
            assistant_id=assistant.id,
        )

        print("First run result: ", run_result)

        os.environ["GATEWAY_URL"] = ""
        tool_call = run_result.required_action.submit_tool_outputs.tool_calls[0]
        func = assistant_config.find_component_tool(tool_call)
        func_res = func.tool_eval(**eval(tool_call.function.arguments))
        final_res = ""
        for res in func_res:
            print("res: ", res)
            final_res += res

        print("final_res: \n", final_res)

        os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
        # run_id = run_result.id

        # appbuilder.assistants.messages.create(
        #     conversation_id=conversation.id,
        #     content=func_res,
        # )
        # run_result = appbuilder.assistants.runs.run(
        #     conversation_id=conversation.id,
        #     assistant_id=assistant.id,
        #     tool_output={"tool_call_id":tool_call.id, "output": func_res, "run_id": run_id},
        # )
        # print(run_result)

if __name__ == "__main__":
    unittest.main()
