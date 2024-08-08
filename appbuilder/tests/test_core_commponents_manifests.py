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


from appbuilder.core.component import Component



def check_ancestor(cls):
    parent_cls = Component
    excluded_classes = ('Component', 'MatchingBaseComponent', 'EmbeddingBaseComponent', 'CompletionBaseComponent')
    if cls.__name__ in excluded_classes:
        return False
    if issubclass(cls, parent_cls):
        if parent_cls in excluded_classes:
            return False
        return True
    for base in cls.__bases__:
        if check_ancestor(base):
            return True
    return False

import os
import importlib.util
import inspect

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

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestComponentManifestsAndToolEval(unittest.TestCase):
    def setUp(self) -> None:
        self.tool_eval_components = find_tool_eval_components()

    def test_manifests(self):
        """
        要求必填，格式:  list[dict]，dict字段为
        * "name"：str，要求不重复
        * "description"：str，对于组件tool_eval函数功能的描述
        * "parameters"：json_schema，对于tool_eval函数入参的描述，json_schema格式要求见https://json-schema.org/understanding-json-schema
        """
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
            app = cls(**mock_args)
            manifests = app.manifests

            assert isinstance(manifests, list)
            assert len(manifests) > 0
            assert isinstance(manifests[0],dict)
            assert isinstance(manifests[0]['name'], str)
            assert isinstance(manifests[0]['description'], str)
            assert isinstance(manifests[0]['parameters'], dict)
            print("组件名称:{}".format(name))

if __name__ == '__main__':
    unittest.main()
    