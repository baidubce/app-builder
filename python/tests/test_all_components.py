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
import unittest
import os
import numpy as np
import pandas as pd
from multiprocessing import Pool

from appbuilder.core.component import Component
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core._exception import AppbuilderBuildexException
from component_collector import  get_all_components, get_v2_components, get_component_white_list
from appbuilder.tests.base_rules import ComponentCheckBase
import component_check

def check_component_with_retry(component_import_res_tuple):
    """
    使用重试机制检查组件。测试用例失败后会重试两次。
    
    Args:
        component_import_res_tuple (tuple): 包含组件和导入结果的元组。
    
    Returns:
        list: 包含错误信息的数据列表。
    
    """
    component, import_res = component_import_res_tuple
    component_check_base = ComponentCheckBase()
    
    error_data = []
    max_retries = 2  # 设置最大重试次数
    attempts = 0

    while attempts <= max_retries:
        if import_res["import_error"] != "":
            error_data.append({"Component Name": component.__name__, "Error Message": import_res["import_error"]})
            print("组件名称:{} 错误信息:{}".format(component.__name__, import_res["import_error"]))
            break

        component_obj = import_res["obj"]
        try:
            # 此处的self.component_check_base.notify需要根据实际情况修改
            pass_check, reasons = component_check_base.notify(component_obj) # 示例修改
            reasons = list(set(reasons))
            if not pass_check:
                error_data.append({"Component Name": component.__name__, "Error Message": ", ".join(reasons)})
                print("组件名称:{} 错误信息:{}".format(component.__name__, ", ".join(reasons)))
                # 如果检查失败，增加尝试次数并重试
                attempts += 1
                if attempts <= max_retries:
                    print("组件名称:{} 将重试，当前尝试次数:{}".format(component.__name__, attempts))
                continue
            # 如果检查通过，则退出循环
            break
        except Exception as e:
            error_data.append({"Component Name": component.__name__, "Error Message": str(e)})
            print("组件名称:{} 错误信息:{}".format(component.__name__, str(e)))
            # 如果发生异常，增加尝试次数并重试
            attempts += 1
            if attempts <= max_retries:
                print("组件名称:{} 将重试，当前尝试次数:{}".format(component.__name__, attempts))
            continue

    return error_data

def write_error_data(txt_file_path, error_df,error_stats):
    with open(txt_file_path, 'w') as file:
        file.write("Component Name\tError Message\n")
        for _, row in error_df.iterrows():
            file.write(f"{row['Component Name']}\t{row['Error Message']}\n")
        file.write("\n错误统计信息:\n")
        for error, count in error_stats.items():
            file.write(f"错误信息: {error}, 出现次数: {count}\n")
    print(f"\n错误信息已写入: {txt_file_path}")

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestComponentManifestsAndToolEval(unittest.TestCase):
    def setUp(self) -> None:
        self.all_components = get_all_components()
        self.v2_components = get_v2_components()
        self.whitelist_components = get_component_white_list()
        self.component_check_base = ComponentCheckBase()

    def _test_component(self, components, whitelist_components, txt_file_path):
        error_data = []
        error_stats ={}
         
        with Pool(processes=os.cpu_count()) as pool:
            # 使用pool.map来执行多进程
            results = pool.map(check_component_with_retry, components.items())
            
            # 合并每个进程返回的错误数据
            for result in results:
                error_data.extend(result)

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
            write_error_data(txt_file_path, error_df, error_stats)

            # 判断报错组件是否位于白名单中
            component_names = error_df["Component Name"].tolist()
            for component_name in component_names:
                if component_name in whitelist_components:
                    print("{}在白名单中，暂时忽略报错。".format(component_name), flush=True)
                else:
                    raise AppbuilderBuildexException(f"组件 {component_name} 未在白名单中，请检查是否需要添加到白名单。")

        else:
            print("\n所有组件测试通过，无错误信息。")


    def test_all_components(self):
        self._test_component(self.all_components, self.whitelist_components, 'components_error_info.txt')

    def test_v2_components(self):
        self._test_component(self.v2_components, [], 'v2_components_error_info.txt')


if __name__ == '__main__':
    unittest.main() 