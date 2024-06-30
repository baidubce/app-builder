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
import json
import uuid
from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional
from appbuilder.core.component import Message, Component
from appbuilder.core.console.appbuilder_client import data_class
from appbuilder.utils.logger_util import logger


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
    component_mainfest: list[dict] = Field(..., description='组件描述')


class IntegratedInputs(BaseModel):
    function_call_user_instruction: str = Field("", description='用户输入的文本')
    function_call_oral_response: bool = Field(False, description='是否返回口语化改写结果')
    function_call_custom_variables: dict = Field({}, description='用户自定义变量')
    function_call_stop_tool_list: list[str] = Field(
        ["ChatAgent"], description='人工指定的终止节点')
    function_call_backup_function: str = Field(
        "chat_agent", description='人工指定的backup能力')
    function_call_contexts: Optional[FunctionCallContexts] = Field(
        None, description='用于恢复中断现场, 仅SDK可用')
    funciton_call_builtin_tool_list: list[dict] = Field(
        [], description='内置可用工具集合')
    funciton_call_plugin_tool_list: list[PluginTool] = Field(
        [], description='插件可用工具集合, 仅SDK可用')


class ModelCompletionParams(BaseModel):
    temperature: float = Field(0.0, description='温度系数')
    top_p: float = Field(0.0, description='top_p系数')


class ModelDefinition(BaseModel):
    name: str = Field(..., description='模型名称')
    completion_params: ModelCompletionParams = Field(..., description='模型描述')


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

class DTEFunctionCallAgent(Component):
    def __init__(self):
        self.user_id = str(uuid.uuid4())

    def create_conversation(self) -> str:
        """创建对话"""
        return str(uuid.uuid4())

    def create_trace_id(self) -> str:
        """创建追踪ID"""
        return str(uuid.uuid4())
    
    def get_builtin_tool_list(self) -> list[BuiltInToolList]:
        
        pass

    def upload_file(self, file_path: str) -> str:
        """上传文件"""
        pass

    def run(self, conversation_id: str,
            query: str,
            model_configs: IntegratedModelConfigs = None,
            inputs: Optional[IntegratedInputs] = None) -> Message:
        """运行对话"""
        return Message()
