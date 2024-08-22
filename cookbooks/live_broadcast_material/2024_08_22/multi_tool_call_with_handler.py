import os
import appbuilder
from appbuilder.core.console.appbuilder_client.event_handler import AppBuilderEventHandler

class MyEventHandler(AppBuilderEventHandler):
    def execute_local_command(self, cmd: str):
        import subprocess
        try:
            result = subprocess.check_output(cmd, shell=True).decode("utf-8")
            if result.strip() == "":
                return "命令执行成功，无返回值"
            return result
        except Exception as e:
            return str(e)
    
    def interrupt(self, run_context, run_response):
        thought = run_context.current_thought
        # 绿色打印
        print("\033[1;32m", "-> Agent 中间思考: ", thought, "\033[0m")

        tool_output = []
        for tool_call in run_context.current_tool_calls:
            tool_call_id = tool_call.id
            tool_res = self.execute_local_command(
                **tool_call.function.arguments)
            # 蓝色打印
            print("\033[1;34m", "-> 本地ToolCall结果: \n", tool_res, "\033[0m\n")
            tool_output.append(
                {
                    "tool_call_id": tool_call_id,
                    "output": tool_res
                }
            )
        return tool_output
    
    def success(self, run_context, run_response):
        print("\n\033[1;31m","-> Agent 非流式回答: \n", run_response.answer, "\033[0m")




# AppBuilder Token，此处为试用Token
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# 应用为：智能问题解决者
app_id = "b9473e78-754b-463a-916b-f0a9097a8e5f"
app_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_client.create_conversation()

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

with app_client.run_with_handler(
        conversation_id = conversation_id,
        query = "请问当前文件夹下有哪些文件？如果没有test.txt文件，请新建一个test.txt文件，内容为：Hello World！",
        tools = tools,
        event_handler = MyEventHandler(),
    ) as run:
        run.until_done()