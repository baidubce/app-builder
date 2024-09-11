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
from appbuilder import AutomaticTestToolEval
from appbuilder.core._exception import AppbuilderBuildexException

def check_ancestor(cls):
    """
    判断给定类是否继承自 Component，但排除某些类。
    
    Args:
        cls (type): 待检查的类。
    
    Returns:
        bool: 如果类继承自 Component 并且不是排除的类，返回 True，否则返回 False。
    """
    parent_cls = Component
    excluded_classes = ('Component', 'CompletionBaseComponent')
    if cls.__name__ in excluded_classes:
        return False
    if issubclass(cls, CompletionBaseComponent):
        return False
    if issubclass(cls, parent_cls):
        return True
    return False


def find_tool_eval_components():
    """
    查找所有继承自 Component 类并且具有 tool_eval 方法的类
    
    Args:
        无
    
    Returns:
        List[Tuple[str, type]]: 包含类名和类对象的元组列表
    
    """
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
                    if check_ancestor(obj):
                        components.append((name, obj))

    return components


def read_whitelist_components():
    """
    读取白名单组件列表文件，返回列表形式。
    
    Args:
        无。
    
    Returns:
        list: 包含白名单组件名称的列表。
    
    """
    with open('whitelist_components.txt', 'r') as f:
        lines = [line.strip() for line in f]
    return lines


def write_error_data(error_df):
    """
    将错误信息和错误统计信息写入到txt文件中。
    
    Args:
        error_df (pandas.DataFrame): 包含错误信息的DataFrame，必须包含'Component Name'和'Error Message'两列。
        error_stats (dict): 包含错误统计信息的字典，键为错误信息，值为出现次数。
    
    Returns:
        None
    
    """
    txt_file_path = 'components_error_info.txt'
    with open(txt_file_path, 'a') as file:
        file.write("Component Name\tError Message\n")
        try:  
            for _, row in error_df.iterrows():
                file.write(f"{row['Component Name']}\t{row['Error Message']}\n")
        except:
            file.write(f"None\tNone\n")
    print(f"\n错误信息已写入: {txt_file_path}")

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestComponentManifestsAndToolEval(unittest.TestCase):
    def setUp(self) -> None:
        """
        初始化测试环境，包括获取工具评估组件和白名单组件。
        
        Args:
            无参数。
        
        Returns:
            None
        
        """
        self.tool_eval_components = find_tool_eval_components()
        self.whitelist_components = read_whitelist_components()

    def test_manifests(self):
        """
        测试manifests是否符合规范。
        
        Args:
            无
        
        Returns:
            无返回值，该函数主要用于测试组件的manifests是否符合规范。
        
        Raises:
            无
        
        """
        """
        要求必填，格式:  list[dict]，dict字段为
        * "name"：str，要求不重复
        * "description"：str，对于组件tool_eval函数功能的描述
        * "parameters"：json_schema，对于tool_eval函数入参的描述，json_schema格式要求见https://json-schema.org/understanding-json-schema
        """
        error_data = []
        print("完成manifests测试的组件:")
        for name, cls in self.tool_eval_components:
            init_signature = inspect.signature(cls.__init__)
            params = init_signature.parameters
            mock_args = {}
            for parameter_name, param in params.items():
                # 跳过 'self' 参数
                if parameter_name == 'self':
                    continue
                if parameter_name == 'model' or name == 'model_name':
                    mock_args[parameter_name] = appbuilder.get_model_list()[0]
            try:
                app = cls(**mock_args)
            except Exception as e:
                if 'missing' in str(e) and 'required' in str(e):
                   pass
                elif 'supported' in str(e):
                    pass
                else:
                    error_data.append({"Component Name": name, "Error Message": str(e)})
            
            try:
                manifests = app.manifests
            except Exception as e:
                error_data.append({"Component Name": name, "Error Message": "检查是否定义了manifests属性"})
            
            try:
                if not  isinstance(manifests, list):
                    raise AppbuilderBuildexException("请检查manifests是否为list类型")
                if not len(manifests) > 0:
                    raise AppbuilderBuildexException("manifests 列表为空")
                if not isinstance(manifests[0],dict):
                    raise AppbuilderBuildexException("请检查manifests列表中元素是否为dict类型")
                if not isinstance(manifests[0]['name'], str):
                    raise AppbuilderBuildexException("请检查manifests列表中元素中的name字段是否为str类型")
                if not isinstance(manifests[0]['description'], str):
                    raise AppbuilderBuildexException("请检查manifests列表中元素中的description字段是否为str类型")
                if not isinstance(manifests[0]['parameters'], dict):
                    raise AppbuilderBuildexException("请检查manifests列表中元素中的parameters字段是否为dict类型")
            except Exception as e:
                error_data.append({"Component Name": name, "Error Message": str(e)}) 
        
        # 将错误信息表格存储在本地变量中
        error_df = pd.DataFrame(error_data) if error_data else None
        
        # 将报错信息写入文件
        write_error_data(error_df)
        
        # 判断报错组件是否位于白名单中
        if error_data:
            component_names = error_df["Component Name"].tolist()
            for component_name in component_names:
                if component_name in self.whitelist_components:
                    print("{}zu白名单中，暂时忽略报错。".format(component_name))
                else:
                    raise AppbuilderBuildexException(f"组件 {component_name} 未在白名单中，请检查是否需要添加到白名单。")
        else:
            print("所有组件测试通过")

    def test_tool_eval(self):
        """
        测试tool_eval组件，收集报错信息，生成并存储报错信息表格，并进行统计和可视化。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        Raises:
            AppbuilderBuildexException: 如果报错组件不在白名单中，则抛出异常。
        """
        print("完成tool_eval测试的组件:")
        error_data = []
        for name, cls in self.tool_eval_components:
            init_signature = inspect.signature(cls.__init__)
            params = init_signature.parameters
            mock_args = {}
            for parameter_name, param in params.items():
                # 跳过 'self' 参数
                if parameter_name == 'self':
                    continue
                if parameter_name == 'model' or name == 'model_name':
                    mock_args[parameter_name] = appbuilder.get_model_list()[0]
            try:
                app = cls(**mock_args)
            except Exception as e:
                if 'missing' in str(e) and 'required' in str(e):
                   pass
                elif 'supported' in str(e):
                    pass
                else:
                    error_data.append({"Component Name": name, "Error Message": str(e)})
            try:
                AutomaticTestToolEval(app)
                print("组件名称:{} 通过测试".format(name))
            except Exception as e:
                if not isinstance(e, IndexError):
                    error_data.append({"Component Name": name, "Error Message": str(e)})
                    print("组件名称:{} 错误信息:{}".format(name, e))

        # 将错误信息表格存储在本地变量中
        error_df = pd.DataFrame(error_data) if error_data else None
        
        # 将报错信息写入文件
        write_error_data(error_df)
        
        # 判断报错组件是否位于白名单中
        if error_data:
            component_names = error_df["Component Name"].tolist()
            for component_name in component_names:
                if component_name in self.whitelist_components:
                    print("{}zu白名单中，暂时忽略报错。".format(component_name))
                else:
                    raise AppbuilderBuildexException(f"组件 {component_name} 未在白名单中，请检查是否需要添加到白名单。")
        else:
            print("所有组件测试通过")

if __name__ == '__main__':
    unittest.main() 
