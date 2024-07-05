# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""AppBuilderClient组件"""
import os
import time
import json
import uuid
import appbuilder
from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional
from appbuilder.core.component import Message, Component
from appbuilder.utils.logger_util import logger
from appbuilder.utils.sse_util import SSEClient
from appbuilder import AnimalRecognition

appbuilder.logger.setLoglevel("info")

os.environ["APPBUILDER_TOKEN"]= "bce-v3/ALTAK-boyiIC3WpU8783XpRoBYE/bcef8b3da5b60aa2be0674539ef06f10e47d5613"
TRACE_ID = str(uuid.uuid4())


class ChatHistory(BaseModel):
    query: str = Field("", description='用户输入的文本')
    answer: str = Field("", description='模型返回的文本')


class UsedTool(BaseModel):
    function_call: dict = Field(
        {}, description='工具调用指令,需要追加的内容为中断事件内的function_call字段')
    function_resp: str = Field(
        "", description='工具返回结果, 需要追加的内容为本地的工具执行结果，以自然语言/json dump str描述长度不宜超过1000')


class FunctionCallContexts(BaseModel):
    chat_history: list[ChatHistory] = Field([], description='聊天历史记录')
    used_tool: list[UsedTool] = Field([], description='使用过的工具')


class ComponentMainfest(BaseModel):
    name: str = Field(..., description='能力名称, 不可重名')
    description: str = Field(...,
                             description='能力描述, 需要有一定的prompt engineering能力')
    parameters: dict = Field({}, description='接口的json schema定义')


class PluginTool(BaseModel):
    component_name: str = Field(..., description='插件名称')
    component_manifest: list[dict] = Field(..., description='组件描述')


class IntegratedInputs(BaseModel):
    function_call_user_instruction: str = Field("", description='用户输入的文本')
    function_call_oral_response: bool = Field(False, description='是否返回口语化改写结果')
    # function_call_custom_variables: dict = Field({}, description='用户自定义变量')
    function_call_stop_tool_list: list[str] = Field(
        ["ChatAgent"], description='人工指定的终止节点')
    function_call_backup_function: str = Field(
        "chat_agent", description='人工指定的backup能力')
    function_call_contexts: Optional[FunctionCallContexts] = Field(
        FunctionCallContexts(), description='用于恢复中断现场, 仅SDK可用')
    function_call_builtin_tool_list: list[dict] = Field(
        [], description='内置可用工具集合')
    function_call_plugin_tool_list: list[PluginTool] = Field(
        [], description='插件可用工具集合, 仅SDK可用')


class ModelCompletionParams(BaseModel):
    temperature: float = Field(0.0, description='温度系数')
    top_p: float = Field(0.0, description='top_p系数')


class ModelDefinition(BaseModel):
    name: str = Field(..., description='模型名称')
    completion_params: ModelCompletionParams = Field(
        ModelCompletionParams(), description='模型描述')


class IntegratedModelConfigs(BaseModel):
    thought_model_config: ModelDefinition = Field(..., description='思考模型配置')
    rag_model_config: ModelDefinition = Field(..., description='RAG模型配置')


class IntegratedRequest(BaseModel):
    query: str = Field(..., description='用户输入的文本')
    conversation_id: str = Field(..., description='会话ID')
    trace_id: str = Field(..., description='追踪ID')
    user: str = Field(..., description='用户ID')
    inputs: IntegratedInputs = Field(..., description='当次对话交互的详情')
    model_configs: IntegratedModelConfigs = Field(..., description='模型配置')


class BuiltInTool(BaseModel):
    function_name: str = Field(..., description='能力名称')
    function_desc: str = Field(..., description='能力描述')


class BuiltInToolList(BaseModel):
    component_name: str = Field(..., description='组件名称')
    functions: list[BuiltInTool] = Field(..., description='组件能力详情')


class GetBuiltInToolResponse(BaseModel):
    code: int = Field(..., description='状态码')
    result: list[BuiltInToolList] = Field(..., description='内置工具列表')

    def __str__(self):
        return json.dumps(self.dict(), indent=4, ensure_ascii=False)


class IntegratedContent(BaseModel):
    event: str = Field(description='事件名称')
    event_status: str = Field(description='事件状态')
    error: Optional[dict] = Field(None, description='错误信息')
    event_id: str = Field(description='事件ID')
    # visible_scope: str = Field(description='llm/user/all')
    type: str = Field(description='类型')
    text: Union[str, dict, list] = Field( description='事件内容')
    usage: Optional[dict] = Field(None, description='使用的模型')

class IntegratedResult(BaseModel):
    is_completion: bool = Field(description='是否完成')
    conversation_id: str = Field(description='会话ID')
    send_at: int = Field(description='发送时间')
    trace_id: str = Field(description='追踪ID')
    user_id: str = Field(description='用户ID')
    answer: str = Field(description='模型返回的文本')
    content: list[IntegratedContent] = Field(description='中间结果，提供用于折叠展示等需求所用的信息。包含：event、event_status、event_id、type和text。')

class IntegratedResponse(BaseModel):
    code: int = Field(description='状态码')
    message: str = Field(description='状态信息')
    result: IntegratedResult = Field(description='当次对话交互的详情')


class DTEFunctionCallAgent(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = str(uuid.uuid4())

    def create_conversation(self) -> str:
        """创建对话"""
        return str(uuid.uuid4())

    def create_trace_id(self) -> str:
        """创建追踪ID"""
        return str(uuid.uuid4())

    def get_builtin_tool_list(self) -> list[BuiltInToolList]:
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        url = "http://copilot-qa.now.baidu-int.com" +\
            "/dte/api/v2/function_call/get_builtin_tool_list"
        response = self.http_client.session.post(
            url, headers=headers, json={}, timeout=None,
        )
        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()
        resp = GetBuiltInToolResponse(**data)
        return resp

    def upload_file(self, file_path: str) -> str:
        """上传文件"""
        pass

    def run(self, conversation_id: str,
            query: str,
            model_configs: IntegratedModelConfigs = None,
            inputs: Optional[IntegratedInputs] = None):
        """运行对话"""
        headers = self.http_client.auth_header_v2()
        headers["Content-Type"] = "application/json"
        headers["X-Appbuilder-Authorization"] = "Bearer bce-v3/ALTAK-boyiIC3WpU8783XpRoBYE/bcef8b3da5b60aa2be0674539ef06f10e47d5613"
        url = "http://copilot-qa.now.baidu-int.com" +\
            "/dte/api/v2/function_call/integrated"

        request = IntegratedRequest(
            query=query,
            conversation_id=conversation_id,
            trace_id=TRACE_ID,
            user="80c5bbee-931d-4ed9-a4ff-63e1971bd072",
            model_configs=model_configs,
            inputs=inputs
        )

        response = self.http_client.session.post(
            url=url,
            headers=headers,
            json=self._transform_input(request.model_dump()),
            timeout=None,
            stream=True
        )

        self.http_client.check_response_header(response)
        client = SSEClient(response)
        return self._iterate_events(client.events())

    def _iterate_events(self, events):
        for event in events:
            try:
                data = event.data
                if len(data) == 0:
                    data = event.raw
                data = json.loads(data)
            except Exception as e:
                logger.error(f"Failed to parse event data: {e}")
            # print(data)
            result = IntegratedResponse(**data)
            # print(result)
            yield result


    def _transform_input(self, json_dict: dict)->dict:
        import copy
        new_json_dict = copy.deepcopy(json_dict)
        input_dict = {}
        # 替换json_dict 中 所有 key 为 "function_call_xxx" 为 "function_call.xxx"
        for key, value in json_dict["inputs"].items():
            if "function_call_" in key:
                new_key = key.replace("function_call_", "function_call.")
            else:
                new_key = key
            input_dict[new_key] = value
        new_json_dict["inputs"] = input_dict
        return new_json_dict


if __name__ == '__main__':

    dte_function_call_agent = DTEFunctionCallAgent()

    image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                "62cf937c03f8c5260d51c6ae"

    query = "我有一张图片，url是: {}, 麻烦帮我看看这是什么动物".format(image_url)
    print("\nquery: {}\n".format(query))

    conversation_id = dte_function_call_agent.create_conversation()
    inputs = IntegratedInputs(
        function_call_plugin_tool_list=[
                PluginTool(
                    component_name="animal_rec",
                    component_manifest=AnimalRecognition().manifests
                )
            ]
    )
    model_configs = IntegratedModelConfigs(
        thought_model_config=ModelDefinition(name="eb-4",),
        rag_model_config=ModelDefinition(name="eb-4")
    )

    begin_time = time.time()
    res = dte_function_call_agent.run(
        conversation_id=conversation_id,
        query=query,
        model_configs=model_configs,
        inputs=inputs
    )
    func_args = {}
    function_call_context = {}

    for r in res:
        print("\n",r)
        for c in r.result.content:
            if c.event == 'Interrupt':
                func_args = c.text.get("function_call", {}).get("arguments", {})
                
                function_call_context = c.text.get("function_call", "")
    first_time = time.time()
    print("\n ---- 函数本地执行！---- ")
    print("func_args: ", func_args)
    print("function_call_context: ", function_call_context)
    print("\n")
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"
    func_res = AnimalRecognition().tool_eval(
        name="animal_rec",
        streaming=True,
        origin_query=query,
        **func_args
    )
    func_message = ""
    for res in func_res:
        func_message += res
    tool_eval_time = time.time()
    print("func_message: ", func_message)
    print("\n")
    print(" ---- 返回函数结果，远程继续执行！---- ")
    os.environ["APPBUILDER_TOKEN"]= "bce-v3/ALTAK-boyiIC3WpU8783XpRoBYE/bcef8b3da5b60aa2be0674539ef06f10e47d5613"
    inputs = IntegratedInputs(
        function_call_plugin_tool_list=[
            {
                "component_name": "animal_rec",
                "component_manifest": AnimalRecognition().manifests
            }
        ],
        function_call_contexts=FunctionCallContexts(
            chat_history=[ChatHistory(
                query=query,
                answer=""
            )],
            used_tool=[UsedTool(
                function_call=function_call_context,
                function_resp=func_message
            )]
        )
    )
    res = dte_function_call_agent.run(
        conversation_id=conversation_id,
        query="",
        model_configs=model_configs,
        inputs=inputs
    )

    final_message = ""
    for r in res:
        print("\n",r)
        final_message += r.result.answer
    end_time = time.time()
    
    print("\nfinal_message: ", final_message)
    print("总耗时：{}秒， 首轮对话耗时：{}秒， 函数本地执行耗时：{}秒， 第二轮对话执行耗时：{}秒。".format(
        end_time - begin_time, first_time - begin_time, tool_eval_time - first_time, end_time - tool_eval_time))


