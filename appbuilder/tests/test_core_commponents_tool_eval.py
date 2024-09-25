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
import unittest
import inspect
import appbuilder
import importlib.util
import numpy as np
import pandas as pd

from appbuilder.core.component import Component
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core._exception import AppbuilderBuildexException
from appbuilder.tests.component_check.check_base import ComponentCheckBase

def check_ancestor(cls):
    parent_cls = Component
    excluded_classes = ('Component', 'MatchingBaseComponent', 'EmbeddingBaseComponent', 'CompletionBaseComponent')
    if cls.__name__ in excluded_classes:
        return False
    if issubclass(cls, CompletionBaseComponent):
        return False
    if issubclass(cls, parent_cls):
        if parent_cls in excluded_classes:
            return False
        return True
    for base in cls.__bases__:
        if check_ancestor(base):
            return True
    return False


def find_tool_eval_components():
    current_file_path = os.path.abspath(__file__)
    print(current_file_path)
    components = []
    added_components = set()
    base_path = current_file_path.split('/')
    base_path = base_path[:-2]+['core', 'components']
    base_path = '/'.join(base_path)
    print(base_path)

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = module_path.replace(base_path, '').replace('/', '.').replace('\\', '.').strip('.')
                
                # 动态加载模块
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    continue

                # 查找继承自 Component 的类
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    has_tool_eval = 'tool_eval' in obj.__dict__ and callable(getattr(obj, 'tool_eval', None))
                    if has_tool_eval and obj.__name__ not in added_components and check_ancestor(obj):
                        added_components.add(obj.__name__)
                        components.append((name, obj))

    return components


def read_whitelist_components():
    with open('whitelist_components.txt', 'r') as f:
        lines = [line.strip() for line in f]
    return lines


def write_error_data(error_df,error_stats):
    txt_file_path = 'components_error_info.txt'
    with open(txt_file_path, 'w') as file:
        file.write("Component Name\tError Message\n")
        for _, row in error_df.iterrows():
            file.write(f"{row['Component Name']}\t{row['Error Message']}\n")
        file.write("\n错误统计信息:\n")
        for error, count in error_stats.items():
            file.write(f"错误信息: {error}, 出现次数: {count}\n")
    print(f"\n错误信息已写入: {txt_file_path}")

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestComponentManifestsAndToolEval(unittest.TestCase):
    def setUp(self) -> None:
        self.tool_eval_components = find_tool_eval_components()
        self.whitelist_components = read_whitelist_components()
        self.component_check_base = ComponentCheckBase()

    def test_component(self):
        error_data = []
        for name, cls in self.tool_eval_components:
            try:
                pass_check, reasons = self.component_check_base.notify(cls)
            except Exception as e:
                error_data.append({"Component Name": name, "Error Message": str(e)})
                print("组件名称:{} 错误信息:{}".format(name, ", ".join(reasons)))
            if not pass_check:
                error_data.append({"Component Name": name, "Error Message": ", ".join(reasons)})
                print("组件名称:{} 错误信息:{}".format(name, ", ".join(reasons)))

        error_df = pd.DataFrame(error_data) if error_data else None
        
        if error_df is not None:
            print("\n错误信息表格:")
            print(error_df)
            # 使用 NumPy 进行统计
            unique_errors, counts = np.unique(error_df["Error Message"], return_counts=True)
            error_stats = dict(zip(unique_errors, counts))
            print("\n错误统计信息:")
            for error, count in error_stats.items():
                print(f"错误信息: {error}, 出现次数: {count}")
        else:
            print("\n所有组件测试通过，无错误信息。")
        
        # 将报错信息写入文件
        write_error_data(error_df, error_stats)
        
        # 判断报错组件是否位于白名单中
        component_names = error_df["Component Name"].tolist()
        for component_name in component_names:
            if component_name in self.whitelist_components:
                print("{}zu白名单中，暂时忽略报错。".format(component_name))
            else:
                raise AppbuilderBuildexException(f"组件 {component_name} 未在白名单中，请检查是否需要添加到白名单。")


if __name__ == '__main__':
    unittest.main() 
