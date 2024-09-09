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
import importlib.util

from appbuilder.core.component import Component
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core._exception import AppbuilderBuildexException

def check_ancestor(cls):
    """
    判断给定类是否继承自指定基类，但不包括排除的类。
    
    Args:
        cls (type): 待检查的类。
    
    Returns:
        bool: 如果该类继承自指定基类，则返回True，否则返回False。
    
    """
    parent_cls = Component
    excluded_classes = ('Component','CompletionBaseComponent')
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
    """
    查找所有继承自 Component 的类，并返回它们的名称和对象。
    
    Args:
        无参数。
    
    Returns:
        一个列表，每个元素为一个元组，元组的第一个元素为类名，第二个元素为类对象。
    
    """
    current_file_path = os.path.abspath(__file__)
    print(current_file_path)
    components = []
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
                    if check_ancestor(obj):
                            components.append((name,obj))
    return components

def read_static_whitelist():
    """
    读取static_whitelist.txt文件，返回一个包含文件中所有非空行的集合。
    
    Args:
        无参数。
    
    Returns:
        一个包含static_whitelist.txt文件中所有非空行的集合（set）。
    
    """
    with open("static_whitelist.txt", 'r') as f:
        return set(line.strip() for line in f if line.strip())

def has_tool_eval_method(cls):
    """
    判断给定的类是否具有 'tool_eval' 方法。
    
    Args:
        cls (type): 需要判断的类。
    
    Returns:
        bool: 如果类具有 'tool_eval' 方法，则返回 True；否则返回 False。
    
    """
    return callable(getattr(cls, 'tool_eval', None))


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestIncrementalComponent(unittest.TestCase):
    def test_component_have_manifests(self):
        """
        测试组件是否具有manifests和tool_eval
        
        Args:
            无
        
        Returns:
            无返回值，直接打印测试结果和错误信息到控制台，并将错误信息追加到components_test.txt文件中
        
        Raises:
            AppbuilderBuildexException: 当同一个组件中manifests和tool_eval均不存在时，抛出异常
        """
        manifests_test =[]
        tool_eval_test = []
        print("============================================================")
        print("开始测试组件manifests和tool_eval是否存在")
        for name, obj in find_tool_eval_components():
            static_whitelist = read_static_whitelist()
            if name in static_whitelist:
                continue
            try:
                self.assertTrue(hasattr(obj, 'manifests'), f"{name} does not have 'manifests'")
                print(f"{name} has 'manifests'")
            except:
                manifests_test.append(name)

            try:
                self.assertTrue(has_tool_eval_method(obj), f"{name} does not have 'tool_eval' method")
                print(f"{name} has 'tool_eval' method")
            except:
                    
                tool_eval_test.append(name)
            
        if len(manifests_test) > 0:
            print("以下组件成员变量manifests不存在：")
            for i in manifests_test:
                print(i)
        
        if len(tool_eval_test) > 0:
            print("以下组件方法tool_eval不存在：")
            for i in tool_eval_test:
                print(i)
        print("============================================================")
        with open("components_test.txt", 'w') as f:
            if len(manifests_test) > 0:
                for name in manifests_test:
                    f.write(name+'\t'+"成员变量manifests不存在\n")
            if len(tool_eval_test) > 0:
                for name in tool_eval_test:
                    f.write(name+'\t'+"方法tool_eval不存在\n")


        if len(manifests_test) == 0 and len(tool_eval_test) == 0:
            with open("components_test.txt", 'a') as f:
                f.write('None'+'\t'+"None\n")
        if len(manifests_test) > 0 and len(tool_eval_test) > 0:
            raise AppbuilderBuildexException("manifests and tool_eval not exist in the same component")
                
if __name__ == '__main__':
    unittest.main()
