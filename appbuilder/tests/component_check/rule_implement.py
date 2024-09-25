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
import inspect
from pydantic import BaseModel
from .check_base import CheckInfo
from .check_base import RuleBase
from .check_base import register_component_check_rule
from appbuilder.utils.json_schema_to_model import json_schema_to_pydantic_model


class ManifestValidRule(RuleBase):
    """
    通过尝试将component的manifest转换为pydantic模型来检查manifest是否符合规范
    """
    def __init__(self):
        super().__init__()
        self.rule_name = "ManifestValidRule"

    def check(self, component_cls) -> CheckInfo:
        check_pass_flag = True
        invalid_details = []

        component_opject = component_cls()
        manifests = component_opject.manifests

        # NOTE(暂时检查manifest中的第一个mainfest)
        manifest = manifests[0]

        try:
            tool_name = manifest['name']
            tool_desc = manifest['description']
            schema = manifest["parameters"]
            schema["title"] = tool_name
            pydantic_model = json_schema_to_pydantic_model(schema, tool_name)
            assert isinstance(pydantic_model, BaseModel)
            check_to_json = pydantic_model.schema_json()
        except Exception as e:
            check_pass_flag = False
            invalid_details.append(e)

        return CheckInfo(check_pass_flag, invalid_details)

Data_Type = {
    'string': str,
    'integer': int,
    'object': int,
    'array': list,
    'boolean': bool,
    'null': None,
}

class MainfestMatchToolEvalRule(RuleBase):
    def __init__(self):
        super().__init__()
        self.rule_name = "MainfestMatchToolEvalRule"
        
    
    def check(self, component_cls) -> CheckInfo:
        check_pass_flag = True
        invalid_details = []

        component_opject = component_cls()
        manifests = component_opject.manifests

        assert len(manifests) >= 1, "Component must have one manifest"

        #NOTE(暂时检查manifest中的第一个mainfest)
        manifest = manifests[0]
        properties = manifest['parameters']['properties']
        required_params = []
        anyOf = manifest['parameters'].get('anyOf', None)
        if anyOf:
            for anyOf_dict in anyOf:
                required_params += anyOf_dict['required']
        if not anyOf:
            required_params += manifest['parameters']['required']
        required_param_dict = {
            'name':str,
            'streaming':bool
        }
        for param in required_params:
            required_param_dict[param] = Data_Type[properties[param]['type']]
        required_params = []
        for param in required_param_dict.keys():
            required_params.append(param)

        # 交互检查
        tool_eval_input_params = []
        signature = inspect.signature(self.components.tool_eval)
        for param_name, param in signature.parameters.items():
            if param_name == 'kwargs':
                continue
            if param_name in required_params:
                if required_param_dict[param_name] == param.annotation:
                    tool_eval_input_params.append(param_name)
                else:
                    check_pass_flag = False
                    invalid_details.append("请检查tool_eval的传入参数{param_name}是否符合成员变量manifest的参数类型要求")
            else:
                check_pass_flag = False
                invalid_details.append(f'请检查tool_eval的传入参数{param_name}是否在成员变量manifest要求内')

        for required_param in required_params:
            if required_param not in tool_eval_input_params:
                check_pass_flag = False
                invalid_details.append(f'请检查成员变量manifest要求的tool_eval的传入参数{required_param}是否在其中')
        
        return CheckInfo(
            check_rule_name=self.rule_name,
            check_result=check_pass_flag,
            check_detail=",".join(invalid_details))
            
    


class ToolEvalInputNameRule(RuleBase):
    """
    检查tool_eval的输入参数中，是否包含系统保留的输入名称
    """
    def __init__(self):
        super().__init__()
        self.rule_name = 'ToolEvalInputNameRule'
        self.system_input_name = [
            "_sys_name",
            "_sys_origin_query",
            "_sys_user_instruction",
            "_sys_file_names",
            "_sys_file_urls",
            "_sys_current_time",
            "_sys_chat_history",
            "_sys_used_tool",
            "_sys_uid",
            "_sys_traceid",
            "_sys_conversation_id",
            "_sys_gateway_endpoint",
            "_sys_appbuiler_token",
            "_sys_debug",
            "_sys_custom_variables",
            "_sys_thought_model_config",
            "_sys_rag_model_config",
        ]

    def check(self, component_cls) -> CheckInfo:
        tool_eval_signature = inspect.signature(component_cls.__init__)
        params = tool_eval_signature.parameters
        invalid_details = []
        check_pass_flag = True
        for param_name in params:
            if param_name == 'self':
                continue
            if param_name in self.system_input_name:
                invalid_details.append(param_name)
                check_pass_flag = False
        

        return CheckInfo(
            check_rule_name=self.rule_name,
            check_result=check_pass_flag,
            check_detail="以下ToolEval方法参数名称是系统保留字段，请更换：{}".format("，".join(invalid_details)) if len(invalid_details) > 0 else "")



register_component_check_rule("ManifestValidRule", ManifestValidRule)
register_component_check_rule("MainfestMatchToolEvalRule", MainfestMatchToolEvalRule)
register_component_check_rule("ToolEvalInputNameRule", ToolEvalInputNameRule)
