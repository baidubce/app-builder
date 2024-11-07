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
import os
import json
import inspect
from pydantic import BaseModel
from appbuilder.utils.func_utils import Singleton
from appbuilder.utils.json_schema_to_model import json_schema_to_pydantic_model


class CheckInfo(BaseModel):
    check_rule_name: str
    check_result: bool
    check_detail: str


class RuleBase(object):
    def __init__(self):
        self.invalid = False

    def check(self, component_cls) -> CheckInfo:
        raise NotImplementedError

    def reset_state(self):
        self.invalid = False


class ComponentCheckBase(metaclass=Singleton):
    def __init__(self):
        self.rules = {}

    def register_rule(self, rule_name: str, rule_obj: RuleBase):
        if not isinstance(rule_obj, RuleBase):
            raise TypeError("rule_obj must be a subclass of RuleBase")
        if rule_name in self.rules:
            raise ValueError(f"Rule {rule_name} already exists.")
        self.rules[rule_name] = rule_obj

    def remove_rule(self, rule_name: str):
        del self.rules[rule_name]

    def notify(self, component_cls) -> tuple[bool, list]:
        check_pass = True
        check_details = {}
        reasons = []
        for rule_name, rule_obj in self.rules.items():
            res = rule_obj.check(component_cls)
            check_details[rule_name] = res
            if res.check_result == False:
                check_pass = False
                reasons.append(res.check_detail)

        if check_pass:
            return True, reasons
        else:
            return False, reasons

def register_component_check_rule(rule_name: str, rule_cls: RuleBase):
    component_checker = ComponentCheckBase()
    component_checker.register_rule(rule_name, rule_cls())



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


        try:
            if not hasattr(component_cls, "manifests"):
                raise ValueError("No manifests found")
            manifests = component_cls.manifests
            # NOTE(暂时检查manifest中的第一个mainfest)
            if not manifests or len(manifests) == 0:
                raise ValueError("No manifests found")
            manifest = manifests[0]
            tool_name = manifest['name']
            tool_desc = manifest['description']
            schema = manifest["parameters"]
            schema["title"] = tool_name
            # 第一步，将json schema转换为pydantic模型
            pydantic_model = json_schema_to_pydantic_model(schema, tool_name)
            check_to_json = pydantic_model.schema_json()
            json_to_dict = json.loads(check_to_json)
        except Exception as e:
            print(e)
            check_pass_flag = False
            invalid_details.append(str(e))

        if len(invalid_details) > 0:
            invalid_details = ",".join(invalid_details)
        else:
            invalid_details = ""
        return CheckInfo(
            check_rule_name=self.rule_name,
            check_result=check_pass_flag,
            check_detail=invalid_details)

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

        try:
            if not hasattr(component_cls, "manifests"):
                raise ValueError("No manifests found")
            manifests = component_cls.manifests
            # NOTE(暂时检查manifest中的第一个mainfest)
            if not manifests or len(manifests) == 0:
                raise ValueError("No manifests found")
            manifest = manifests[0]
            properties = manifest['parameters']['properties']
            required_params = []
            anyOf = manifest['parameters'].get('anyOf', None)
            if anyOf:
                for anyOf_dict in anyOf:
                    required_params += anyOf_dict['required']
            if not anyOf:
                required_params += manifest['parameters']['required']


            # 交互检查
            tool_eval_input_params = []
            print("required_params: {}".format(required_params))
            signature = inspect.signature(component_cls.tool_eval)
            ileagal_params = []
            for param_name, param in signature.parameters.items():
                if param_name == 'kwargs' or param_name == 'args' or param_name == 'self':
                    continue
                if param_name not in required_params:
                    check_pass_flag = False
                    ileagal_params.append(param_name)

            if len(ileagal_params) > 0:
                invalid_details.append("tool_eval 参数 {} 不在 mainfest 参数列表中".format(",".join(ileagal_params)))

            ileagal_params =[]
            for required_param in required_params:
                if required_param not in tool_eval_input_params:
                    check_pass_flag = False
                    ileagal_params.append(required_param)
            if len(ileagal_params) > 0:
                invalid_details.append("mainfest 参数 {} 不在 tool_eval 参数列表中".format(",".join(ileagal_params)))

            return CheckInfo(
                check_rule_name=self.rule_name,
                check_result=check_pass_flag,
                check_detail=",".join(invalid_details))

        except Exception as e:
            check_pass_flag = False
            invalid_details.append(str(e))
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