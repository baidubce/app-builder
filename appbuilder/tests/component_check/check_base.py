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
from pydantic import BaseModel
from appbuilder.utils.func_utils import Singleton

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


class ComponentCheckBase(Singleton):
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
