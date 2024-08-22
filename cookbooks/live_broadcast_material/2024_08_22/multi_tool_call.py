import os
import appbuilder

# AppBuilder Token，此处为试用Token
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# 应用为：智能问题解决者
app_id = "b9473e78-754b-463a-916b-f0a9097a8e5f"
app_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_client.create_conversation()

# -------------------------------------------------------------#
# 赋予应用一个执行本地命令的能力
def execute_local_command(cmd: str):
    import subprocess
    try:
        result = subprocess.check_output(cmd, shell=True).decode("utf-8")
        if result.strip() == "":
            return "命令执行成功，无返回值"
        return result
    except Exception as e:
        return str(e)


# 创建工具的描述：json_schema格式
tools = [
    {
        "type": "function",
        "function": {
            "name": "execute_local_command",
            "description": "可以在bash环境中，执行输入的指令，注意，一次只能执行一个原子命令。例如：ls",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "需要执行的指令",
                    },
                },
                "required": ["cmd"],
            },
        },
    }
]

# 我们再次询问应用，并给他赋予这个能力
message_1 = app_client.run(
    conversation_id=conversation_id,
    query="请问当前文件夹下有哪些文件？如果没有test.txt文件，请新建一个test.txt文件，内容为：Hello World！",
    tools=tools
)
print("Agent的中间思考过程：")
print(message_1.content.events[-1].model_dump_json(indent=4))
print("Agent思考结束，等待我们上传本地结果\n")

# 大模型下发了调用本地函数的参数，我们使用这个参数调用本地函数
tool_call = message_1.content.events[-1].tool_calls[-1]
tool_call_id = tool_call.id
tool_call_argument = tool_call.function.arguments
local_func_result = execute_local_command(**tool_call_argument)
print("No.1 local_func_result:\n {}\n".format(local_func_result))

# 向应用返回本地运行的结果，继续等待Agent的思考
message_2 = app_client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call_id,
        "output": local_func_result
    }]
)

event_status = message_2.content.events[-1].status
if event_status != "interrupt":
    print("Agent 的回答是：\n")
    print(message_2.content.answer)
    quit()


print("Agent的中间思考过程：")
print(message_2.content.events[-1].model_dump_json(indent=4))


# 大模型下发了调用本地函数的参数，我们使用这个参数调用本地函数
tool_call = message_2.content.events[-1].tool_calls[-1]
tool_call_id = tool_call.id
tool_call_argument = tool_call.function.arguments
local_func_result = execute_local_command(**tool_call_argument)
print("No.2 local_func_result: {}\n".format(local_func_result))

# 向应用返回本地运行的结果，完成应用的调用
message_3 = app_client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call_id,
        "output": local_func_result
    }]
)

event_status = message_3.content.events[-1].status
if event_status != "interrupt":
    print("Agent 的回答是：\n")
    print(message_3.content.answer)
    quit()

print("Agent的中间思考过程：")
print(message_3.content.events[-1].model_dump_json(indent=4))
# 大模型下发了调用本地函数的参数，我们使用这个参数调用本地函数
tool_call = message_3.content.events[-1].tool_calls[-1]
tool_call_id = tool_call.id
tool_call_argument = tool_call.function.arguments
local_func_result = execute_local_command(**tool_call_argument)
print("No.3 local_func_result: {}\n".format(local_func_result))

message_4 = app_client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call_id,
        "output": local_func_result
    }]
)
print("Agent 的回答是：\n")
print(message_4.content.answer)