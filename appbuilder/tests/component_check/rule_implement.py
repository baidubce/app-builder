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
from .check_base import CheckInfo
from .check_base import RuleBase
from .check_base import register_component_check_rule

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
        self.rule_name = "MainfestMatchToolEvalRule"
    
    def check(self, component_cls) -> CheckInfo:
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


class ToolEvalInputNameRule(RuleBase):
    """
    检查tool_eval的输入参数中，是否包含系统保留的输入名称
    """
    def __init__(self):
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
        super().__init__()


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

