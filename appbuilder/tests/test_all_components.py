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
from component_collector import  get_all_components, get_component_white_list
from appbuilder.tests.component_check import ComponentCheckBase


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

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestComponentManifestsAndToolEval(unittest.TestCase):
    def setUp(self) -> None:
        self.all_components = get_all_components()
        self.whitelist_components = get_component_white_list()
        self.component_check_base = ComponentCheckBase()

    def test_component(self):
        error_data = []
        error_stats ={}
         
        for name, import_res in self.all_components.items():

            if import_res["import_error"] != "":
                error_data.append({"Component Name": name, "Error Message": import_res["import_error"]})
                print("组件名称:{} 错误信息:{}".format(name, import_res["import_error"]))
                continue

            component_obj = import_res["obj"]
            try:
                pass_check, reasons = self.component_check_base.notify(component_obj)
                reasons = list(set(reasons))
                if not pass_check:
                    error_data.append({"Component Name": name, "Error Message": ", ".join(reasons)})
                    print("组件名称:{} 错误信息:{}".format(name, ", ".join(reasons)))
            except Exception as e:
                error_data.append({"Component Name": name, "Error Message": str(e)})
                print("组件名称:{} 错误信息:{}".format(name, str(e)))


        error_df = pd.DataFrame(error_data) if len(error_data) > 0 else None

        if error_df is not None:
            print("\n错误信息表格:")
            print(error_df)
            # 使用 NumPy 进行统计
            unique_errors, counts = np.unique(error_df["Error Message"], return_counts=True)
            error_stats = dict(zip(unique_errors, counts))
            print("\n错误统计信息:")
            for error, count in error_stats.items():
                print(f"错误信息: {error}, 出现次数: {count}")
            # 将报错信息写入文件
            write_error_data(error_df, error_stats)

            # 判断报错组件是否位于白名单中
            component_names = error_df["Component Name"].tolist()
            for component_name in component_names:
                if component_name in self.whitelist_components:
                    print("{}zu白名单中，暂时忽略报错。".format(component_name))
                else:
                    raise AppbuilderBuildexException(f"组件 {component_name} 未在白名单中，请检查是否需要添加到白名单。")

        else:
            print("\n所有组件测试通过，无错误信息。")


if __name__ == '__main__':
    unittest.main() 