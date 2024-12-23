from multiprocessing import Pool
import os
import numpy as np
import pandas as pd
import unittest
import os

from appbuilder.core._exception import AppbuilderBuildexException
from component_tool_eval_cases import component_tool_eval_cases
from component_collector import  get_all_components, get_v2_components, get_component_white_list
from component_check import check_component_with_retry, write_error_data


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestComponentManifestsAndToolEval(unittest.TestCase):
    """
    组件manifests和tool_eval入参测试类
    Args:
        无
    
    Returns:
        无返回值
    
    Raises:
        无
        
    """
    def setUp(self) -> None:
        """初始化测试用例，设置component名单和白名单，并初始化ComponentCheckBase实例
        Args:
            无
        Returns:
            无
        """
        self.all_components = get_all_components()
        self.v2_components = get_v2_components()
        self.whitelist_components = get_component_white_list()

    def _test_component(self, components, component_cases, whitelist_components, txt_file_path):
        """测试所有组件的manifests和tool_eval入参
        Args:
            无
        Raises:
            AppbuilderBuildexException: 如果有任何组件不在白名单中，则抛出异常
        """
        error_data = []
        error_stats ={}
         
        with Pool(processes=os.cpu_count()) as pool:
            # 使用pool.map来执行多进程
            args = []
            for component, import_res in components.items():
                if component not in component_cases:
                    error_data.append({"Component Name": component, "Error Message": "{} 没有添加测试case到 \
                        component_tool_eval_cases 中".format(component)})
                    continue
                else:
                    args.append((component, import_res, component_tool_eval_cases[component]))
            
            results = pool.map(check_component_with_retry, args)
            
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

    def _test_all_components(self):
        """测试旧版本组件"""
        self._test_component(self.all_components, [], self.whitelist_components, 'components_error_info.txt')

    def test_v2_components(self):
        """测试v2版本组件"""
        self._test_component(self.v2_components, component_tool_eval_cases, [], 'v2_components_error_info.txt')


if __name__ == '__main__':
    unittest.main() 