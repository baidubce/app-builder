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
import time
from jsonschema import validate, ValidationError, SchemaError
from pydantic import BaseModel
from typing import Generator
from appbuilder.utils.func_utils import Singleton
from appbuilder.utils.json_schema_to_model import json_schema_to_pydantic_model
from appbuilder.tests.component_schemas import type_to_json_schemas
from component_tool_eval_cases import component_tool_eval_cases
from component_tool_eval_schemas import components_tool_eval_output_json_maps


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
            required_exists = False
            if anyOf:
                for anyOf_dict in anyOf:
                    if 'required' in anyOf_dict:
                        required_exists = True
                        required_params += anyOf_dict['required']
                    
            if not anyOf:
                if 'required' in manifest['parameters']:
                    required_exists = True
                    required_params += manifest['parameters']['required']

            if not required_exists:
                check_pass_flag = False
                invalid_details.append("mainfest 未定义required参数")
                return CheckInfo(
                    check_rule_name=self.rule_name,
                    check_result=check_pass_flag,
                    check_detail=",".join(invalid_details))
            
            # 交互检查
            tool_eval_input_params = []
            print("required_params: {}".format(required_params))
            signature = inspect.signature(component_cls.tool_eval)
            ileagal_params = []
            for param_name, param in signature.parameters.items():
                if param_name == 'kwargs' or param_name == 'args' or param_name == 'self':
                    continue
                tool_eval_input_params.append(param_name)
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


class ToolEvalOutputJsonRule(RuleBase):
    """
    检查tool_eval的输出结果是否符合对应的json schema
    """
    def __init__(self):
        super().__init__()
        self.rule_name = 'ToolEvalOutputJsonRule'

    def _check_pre_format(self, outputs):
        invalid_details = []
        if "content" not in outputs:
            invalid_details.append("ToolEval返回值不符合规范：返回内容缺少content")
            return invalid_details
        
        for content in outputs["content"]:
            if "type" not in content:
                invalid_details.append("ToolEval返回值不符合规范：返回content缺少type")
                break
            
            out_type = content["type"]
            if out_type not in type_to_json_schemas:
                invalid_details.append("ToolEval返回值不符合JSON Schema：返回content.type={} 不是合法的输出类型".format(out_type))
                break
        return invalid_details
        
    def _check_jsonschema(self, outputs, output_schemas):
        """检查输出格式是否符合对应的json schema
        """
        invalid_details = []
        if len(self._check_pre_format(outputs)) > 0 :
            return invalid_details
    
        for content in outputs["content"]: 
            out_type = content["type"]
            out_schema = type_to_json_schemas[out_type]
            if out_schema not in output_schemas:
                invalid_details.append("ToolEval返回值不符合JSON Schema：{} 不是该组件期望的Json Schema输出类型".format(out_schema['$schema']))
                continue
            try:
                validate(instance=content, schema=out_schema)
            except Exception as e:
                invalid_details.append("ToolEval返回值不符合JSON Schema: {}\n".format(e.message))
        return invalid_details

    def _gather_iter_outputs(self, outputs):
        text_output = ""
        oral_text_output = ""
        code_output = ""
        for content in outputs.content:
            out_type = content.type
            if out_type == "text":
                text_output += content.text.info
            elif out_type == "oral_text":
                oral_text_output += content.oral_text.info
            elif out_type == "code":
                code_output += content.code.code
        return {
            "text": text_output,
            "oral_text": oral_text_output,
            "code": code_output,
        }
        
    def _check_text_and_code(self, component_case, output_dict):
        """检查输出的内容是否符合预期，只检查text(包含oral_text)和code
        """
        if not hasattr(component_case,"outputs"):
            return []

        expected_output = component_case.outputs()
        expected_output_texts = []
        expected_output_oral_texts = []
        expected_output_codes = []
        if "text" in expected_output:
            expected_output_texts = expected_output["text"] 
        if "oral_text" in expected_output:
            expected_output_oral_texts = expected_output["oral_text"] 
        if "code" in expected_output:
            expected_output_codes = expected_output["code"]
    
        lost_texts = []
        lost_oral_texts = []
        lost_code = []
        for expected_output_text in expected_output_texts:
            if expected_output_text not in output_dict["text"]:
                lost_texts.append(expected_output_text)

        for expected_output_oral_text in expected_output_oral_texts:
            if expected_output_oral_text not in output_dict["oral_text"]:
                lost_oral_texts.append(expected_output_oral_text)

        for expected_output_code in expected_output_codes:
            if expected_output_code not in output_dict["code"]:
                lost_code.append(expected_output_code)

        error_message = ""
        if len(lost_texts) > 0:
            error_message += "应包含text:{}".format(", ".join(lost_texts))
        if len(lost_oral_texts) > 0:
            error_message += "应包含oral_text:{}".format(", ".join(lost_oral_texts))
        if len(lost_code) > 0:
            error_message += "应包含code:{}".format(", ".join(lost_code))
            
        if error_message != "":
            return ["ToolEval返回内容与预期不符: " + error_message]
        else:
            return []
        
    def check(self, component_cls) -> CheckInfo:
        invalid_details = []
        component_cls_name = component_cls.__name__
        if component_cls_name not in components_tool_eval_output_json_maps:
            invalid_details.append("{} 没有注册到 components_tool_eval_output_json_maps 中".format(component_cls_name))
        else:
            output_json_schemas = components_tool_eval_output_json_maps[component_cls_name]
            if component_cls_name not in component_tool_eval_cases:
                invalid_details.append("{} 没有添加测试case到 component_tool_eval_cases 中".format(component_cls_name))
            else:
                component_case = component_tool_eval_cases[component_cls_name]()
                input_dict = component_case.inputs()
                component_obj = component_cls()
                
                try:
                    stream_output_dict = {"text": "", "oral_text":"", "code": ""}
                    stream_outputs = component_obj.tool_eval(**input_dict)
                    for stream_output in stream_outputs: #校验流式输出
                        iter_invalid_detail = self._check_jsonschema(stream_output.model_dump(), output_json_schemas)
                        invalid_details.extend(["流式" + error_message for error_message in iter_invalid_detail])
                        iter_output_dict = self._gather_iter_outputs(stream_output)
                        stream_output_dict["text"] += iter_output_dict["text"]
                        stream_output_dict["oral_text"] += iter_output_dict["oral_text"]
                        stream_output_dict["code"] += iter_output_dict["code"]
                    if len(invalid_details) == 0:
                        invalid_details.extend(self._check_text_and_code(component_case, stream_output_dict))
                except Exception as e:
                    invalid_details.append("ToolEval执行失败: {}".format(e))

                time.sleep(2)
                try:
                    non_stream_outputs = component_obj.non_stream_tool_eval(**input_dict)
                    non_stream_invalid_details  = self._check_jsonschema(non_stream_outputs.model_dump(), output_json_schemas)  #校验非流式输出
                    invalid_details.extend(["非流式" + error_message for error_message in non_stream_invalid_details]) 
                    if len(invalid_details) == 0:
                        non_stream_output_dict = self._gather_iter_outputs(non_stream_outputs)
                        invalid_details.extend(self._check_text_and_code(component_case, non_stream_output_dict))
                except Exception as e:
                    invalid_details.append(" NonStreamToolEval执行失败: {}".format(e))
                    
        if len(invalid_details) > 0:
            return CheckInfo(
                check_rule_name=self.rule_name,
                check_result=False,
                check_detail=",".join(invalid_details))
        else:
            return CheckInfo(
                check_rule_name=self.rule_name,
                check_result=True,
                check_detail="")
                

register_component_check_rule("ManifestValidRule", ManifestValidRule)
register_component_check_rule("MainfestMatchToolEvalRule", MainfestMatchToolEvalRule)
register_component_check_rule("ToolEvalInputNameRule", ToolEvalInputNameRule)
register_component_check_rule("ToolEvalOutputJsonRule", ToolEvalOutputJsonRule)