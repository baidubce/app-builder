import os
import unittest
import inspect
import subprocess
import appbuilder
import importlib.util
import pandas as pd

from appbuilder.core.component import Component
from appbuilder import AutomaticTestToolEval
from appbuilder.core.components.llms.base import CompletionBaseComponent
from appbuilder.core._exception import AppbuilderBuildexException

def test_add_components():
    """
    获取自上一个与upstream/master合并的commit以来新增的Python文件名列表。
    
    Args:
        无参数。
    
    Returns:
        List[str]: 自上一个与origin/master合并的commit以来新增的Python文件名列表。
    
    Raises:
        无异常。
    """
    try:
        merge_base = subprocess.run(
            ["git", "merge-base", "HEAD", "origin/master"],  # PR中改为upstream/master
            capture_output=True, text=True, check=True
        )
        base_commit = merge_base.stdout.strip()
        print("Merge base commit:", base_commit)
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=A", base_commit, "--", "*.py"],
            capture_output=True, text=True, check=True
        )

        new_files = result.stdout.splitlines()
        print("新增的 Python 文件:", new_files)

    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息: {e.stderr}")
        return []

    return new_files


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


def find_tool_eval_components(new_files):
    """
    查找所有继承自 Component 的类，并返回类名和类对象。
    
    Args:
        new_files: 需要检查的文件列表。
    
    Returns:
        一个包含类名和类对象的元组列表。
    """
    components = []
    for file_path in new_files:
        if file_path.endswith(".py"):
            abs_file_path = os.path.abspath(file_path)
            print(f"正在检查文件: {abs_file_path}")

            module_name = os.path.splitext(os.path.basename(abs_file_path))[0]
            try:
                spec = importlib.util.spec_from_file_location(module_name, abs_file_path)
                if spec is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"加载模块时出错: {e}")
                continue

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if check_ancestor(obj):
                    components.append((name, obj))

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

def write_error_data(error_df):
    """
    将错误信息和错误统计信息写入到txt文件中。
    
    Args:
        error_df (pandas.DataFrame): 包含错误信息的DataFrame，必须包含'Component Name'和'Error Message'两列。
        error_stats (dict): 包含错误统计信息的字典，键为错误信息，值为出现次数。
    
    Returns:
        None
    
    """
    txt_file_path = 'new_add_components_error_info.txt'
    with open(txt_file_path, 'w') as file:
        file.write("Component Name\tError Message\n")
        if not error_df:
            file.write(f"None\tNone\n")
        else:   
            for _, row in error_df.iterrows():
                file.write(f"{row['Component Name']}\t{row['Error Message']}\n")
    print(f"\n错误信息已写入: {txt_file_path}")

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

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestAddComponent(unittest.TestCase):
    def setUp(self):
        self.tool_eval_components = find_tool_eval_components(test_add_components())
        self.whitelist_components = read_whitelist_components()

    def test_exist_tool_eval_manifest(self):
        """
        测试组件是否包含manifests和tool_eval属性或方法
        
        Args:
            无
        
        Returns:
            无返回值
        
        Raises:
            AppbuilderBuildexException: 当同一个组件中既不存在manifests属性，也不存在tool_eval方法时抛出
        
        """
        manifests_test =[]
        tool_eval_test = []
        print("============================================================")
        print("开始测试组件manifests和tool_eval是否存在")
        for name, obj in self.tool_eval_components:
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


if __name__ == "__main__":
    unittest.main() 