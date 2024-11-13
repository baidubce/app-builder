import appbuilder
from appbuilder.core.console.appbuilder_client import data_class
import os
from appbuilder import FunctionView, function, function_parameter, function_return

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-DKaql4wY9ojwp2uMe8IEj/7ae1190aff0684153de365381d9b06beab3064c5"
app_id = "7cc4c21f-0e25-4a76-baf7-01a2b923a1a7"  # 已发布AppBuilder应用的ID
# 初始化智能体
client = appbuilder.AppBuilderClient(app_id)
# 创建会话
conversation_id = client.create_conversation()
#注意：要使用此方法要为函数写好注释。最好按照谷歌规范来写

@function(description="获取指定中国城市的当前天气信息。仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。")
@function_parameter(name="location", example="北京", description="城市名，例如：北京。")
@function_parameter(name="unit", example="celsius", description="温度单位，支持 'celsius' 或 'fahrenheit'")
@function_return(description="天气情况描述", example="北京今天25度")
#定义示例函数
def get_current_weather(location: str, unit: str) -> str:
  return "北京今天25度"

print(get_current_weather.__pf_function__)
'''
#定义函数列表
functions = [get_current_weather]
function_map = {f.__name__: f for f in functions}
#调用大模型
msg = client.run(
  conversation_id=conversation_id,
  query="今天北京的天气怎么样？",
  tools = [appbuilder.function_to_model(f).model_dump() for f in functions]
  )
print(msg.model_dump_json(indent=4))
# 获取最后的事件和工具调用信息
event = msg.content.events[-1]
tool_call = event.tool_calls[-1]

# 获取函数名称和参数
name = tool_call.function.name
args = tool_call.function.arguments

# 将函数名称映射到具体的函数并执行
raw_result = function_map[name](**args)

# 传递工具的输出
msg_2 = client.run(
    conversation_id=conversation_id,
    tool_outputs=[{
        "tool_call_id": tool_call.id,
        "output": str(raw_result)
    }],
)
print(msg_2.model_dump_json(indent=4))'''