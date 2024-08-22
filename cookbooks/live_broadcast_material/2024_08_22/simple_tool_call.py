import os
import appbuilder

# AppBuilder Token，此处为试用Token
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# 应用为：智能问题解决者
app_id = "b9473e78-754b-463a-916b-f0a9097a8e5f"
app_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_client.create_conversation()

# 首次提问一个问题，应用不具备该能力，通过回答可以印证
message_1 = app_client.run(
    conversation_id=conversation_id,
    query="请问本公司的张三同学的生日是哪天？",
)
print("Agent第一次回答: {}".format(message_1.content.answer))


# -------------------------------------------------------------#
# 赋予应用一个本地查询组件能力
def get_person_infomation(name: str):
    info_dict = {
        "张三": "1980年1月1日",
        "李四": "1975年12月31日",
        "刘伟": "1990年12月30日"
    }

    if name in info_dict:
        return f"您要查找的{name}的生日是：{info_dict[name]}"
    else:
        return f"您要查找的{name}的信息我们暂未收录，请联系管理员添加。"
    
# 创建工具的描述：json_schema格式
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_person_infomation",
            "description": "查找公司内指定人员的信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "人员名称，例如：张三、李四",
                    },
                },
                "required": ["name"],
            },
        },
    }
]

# 我们再次询问应用，并给他赋予这个能力
message_2 = app_client.run(
    conversation_id=conversation_id,
    query="请问本公司的张三同学的生日是哪天？",
    tools=tools
)
print("Agent的中间思考过程：")
print(message_2.content.events[-1].model_dump_json(indent=4))
print("Agent思考结束，等待我们上传本地结果\n")

# 大模型下发了调用本地函数的参数，我们使用这个参数调用本地函数
tool_call = message_2.content.events[-1].tool_calls[-1]
tool_call_id = tool_call.id
tool_call_argument = tool_call.function.arguments
local_func_result = get_person_infomation(**tool_call_argument)
print("local_func_result: {}\n".format(local_func_result))

# 向应用返回本地运行的结果，完成本地函数toolcall调用
message_3 = app_client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call_id,
        "output": local_func_result
    }]
)
print("Agent 拥有了本地函数调用能力后，回答是: {}".format(message_3.content.answer))