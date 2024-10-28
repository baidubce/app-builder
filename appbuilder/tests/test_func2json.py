import unittest
import appbuilder
import os
from typing import List, Dict, Union

#@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-DKaql4wY9ojwp2uMe8IEj/7ae1190aff0684153de365381d9b06beab3064c5"
        self.app_id = "7cc4c21f-0e25-4a76-baf7-01a2b923a1a7"
        self.client = appbuilder.AppBuilderClient(self.app_id)
        self.conversation_id = self.client.create_conversation()

    def run_tool_call_test(self, function, query):
        # 设置函数映射
        functions = [function]
        function_map = {f.__name__: f for f in functions}

        tools = [appbuilder.function_to_json(f) for f in functions]
        print(tools)
        # 将函数转换为JSON格式并调用
        msg = self.client.run(
            conversation_id=self.conversation_id,
            query=query,
            tools=tools
        )
        print(msg.model_dump_json(indent=4))

        # 获取最后事件的工具调用信息
        event = msg.content.events[-1]
        tool_call = event.tool_calls[-1]
        name = tool_call.function.name
        args = tool_call.function.arguments

        # 检查和打印参数类型
        print("检查参数类型:")
        for arg_name, arg_value in args.items():
            print(f"参数名称: {arg_name}, 参数值: {arg_value}, 参数类型: {type(arg_value)}")

        # 执行映射函数并返回结果
        # 尝试将返回值转换为字符串，如果无法转换则抛出 TypeError
        try:
            raw_result = str(function_map[name](**args))
        except (TypeError, ValueError) as e:
            raise TypeError(f"无法将函数 '{name}' 的返回值转换为字符串: {e}")
        print(raw_result)
        # 传递工具的输出
        msg_2 = self.client.run(
            conversation_id=self.conversation_id,
            tool_outputs=[{
                "tool_call_id": tool_call.id,
                "output": raw_result
            }],
        )
        print(msg_2.model_dump_json(indent=4))
    '''  没有description而报错
    def test_minimal_function(self):
        """测试最简陋的函数"""
        def a(b, c):
            return b + c
        self.run_tool_call_test(a, "计算2和3的和")
    '''
    '''  没有description而报错
    def test_basic_function(self):
        """测试基本款函数"""
        def add_numbers(num1, num2):
            return num1 + num2
        self.run_tool_call_test(add_numbers, "计算5和10的和")
    '''
    '''  没有description而报错
    def test_improved_function(self):
        """测试较好的函数（带类型注解）"""
        def add_numbers(num1: int, num2: int) -> int:
            return num1 + num2
        self.run_tool_call_test(add_numbers, "计算7和8的和")
    
    def test_recommended_function(self):
        """测试推荐的函数（带类型注解和注释）"""
        def add_numbers(num1: int, num2: int) -> int:
            """
            计算两个整数的和

            参数:
                num1 (int): 第一个整数
                num2 (int): 第二个整数

            返回:
                两个数的和
            """
            return num1+num2
        self.run_tool_call_test(add_numbers, "计算12和13的和")
    '''
    def test_complex_function(self):
        """测试高复杂性函数（多个参数和逻辑）"""
        def process_data(data: List[float], scale: float, offset: float, 
                 min_threshold: float, max_threshold: float,
                 normalization: bool = True, standardize: bool = False, 
                 round_digits: int = 2, filter_outliers: bool = True,
                 log_transform: bool = False) -> Dict[str, Union[float, List[float]]]:
            """
            处理数据并生成统计信息，包含缩放、平移、过滤和标准化等操作。

            参数:
            - data (List[float]): 待处理的数值列表
            - scale (float): 缩放因子，用于缩放数据
            - offset (float): 平移值，用于偏移数据
            - min_threshold (float): 最小阈值，低于此值的数据将被过滤
            - max_threshold (float): 最大阈值，高于此值的数据将被过滤
            - normalization (bool): 是否归一化数据（0到1），默认为True
            - standardize (bool): 是否将数据标准化为均值0，方差1，默认为False
            - round_digits (int): 小数位数，用于四舍五入结果，默认为2
            - filter_outliers (bool): 是否过滤异常值，默认为True
            - log_transform (bool): 是否对数据进行对数变换，默认为False

            返回:
            Dict[str, Union[float, List[float]]]: 包含统计信息的字典，包含以下键：
                - 'processed_data': 处理后的数据列表
                - 'mean': 数据的平均值
                - 'std_dev': 数据的标准差
                - 'min': 数据的最小值
                - 'max': 数据的最大值

            异常:
            - ValueError: 如果输入数据为空或无效参数组合则抛出

            示例:
            >>> process_data([10, 20, 30], scale=1.5, offset=5, min_threshold=10, max_threshold=50)
            {'processed_data': [20.0, 35.0, 50.0], 'mean': 35.0, 'std_dev': 15.0, 'min': 20.0, 'max': 50.0}
            """
            import math
            import statistics

            # 参数检查
            if not data:
                raise ValueError("数据列表不能为空")
            if scale <= 0 or min_threshold >= max_threshold:
                raise ValueError("缩放因子必须为正，且最小阈值应小于最大阈值")

            # 数据缩放和平移
            processed_data = [(x * scale) + offset for x in data]

            # 数据过滤
            processed_data = [x for x in processed_data if min_threshold <= x <= max_threshold]

            # 异常值过滤
            if filter_outliers:
                mean_value = statistics.mean(processed_data)
                std_dev_value = statistics.stdev(processed_data)
                processed_data = [x for x in processed_data if (mean_value - 2 * std_dev_value) <= x <= (mean_value + 2 * std_dev_value)]

            # 对数变换
            if log_transform:
                processed_data = [math.log(x) if x > 0 else 0 for x in processed_data]

            # 归一化
            if normalization and processed_data:
                min_val, max_val = min(processed_data), max(processed_data)
                processed_data = [(x - min_val) / (max_val - min_val) if (max_val - min_val) != 0 else 0 for x in processed_data]

            # 标准化
            if standardize and processed_data:
                mean_val = statistics.mean(processed_data)
                std_dev = statistics.stdev(processed_data)
                processed_data = [(x - mean_val) / std_dev if std_dev != 0 else 0 for x in processed_data]

            # 结果四舍五入
            processed_data = [round(x, round_digits) for x in processed_data]

            # 计算统计信息
            return {
                'processed_data': processed_data,
                'mean': round(statistics.mean(processed_data), round_digits) if processed_data else None,
                'std_dev': round(statistics.stdev(processed_data), round_digits) if len(processed_data) > 1 else None,
                'min': min(processed_data) if processed_data else None,
                'max': max(processed_data) if processed_data else None
            }
        query = "处理数据[1, 2, 3, 4]，缩放因子为1.5，偏移量为2.0，过滤阈值范围为1.0到10.0，"
        self.run_tool_call_test(process_data, query)
        '''
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "process_data",
                    "description": """Processes data and generates statistics including scaling, offsetting, filtering, and normalization.示例:
            >>> process_data([10, 20, 30], scale=1.5, offset=5, min_threshold=10, max_threshold=50)
            {'processed_data': [20.0, 35.0, 50.0], 'mean': 35.0, 'std_dev': 15.0, 'min': 20.0, 'max': 50.0}""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "number"
                                },
                                "description": "A list of float numbers to process, e.g., [1.0, 2.0, 3.5]"
                            },
                            "scale": {
                                "type": "number",
                                "description": "A float representing the scale factor to apply to the data."
                            },
                            "offset": {
                                "type": "number",
                                "description": "float类型，A float representing the offset to add to the scaled data."
                            },
                            "min_threshold": {
                                "type": "number",
                                "description": "float类型，A float representing the minimum threshold; values below this will be filtered."
                            },
                            "max_threshold": {
                                "type": "number",
                                "description": "float类型，A float representing the maximum threshold; values above this will be filtered."
                            },
                            "normalization": {
                                "type": "boolean",
                                "description": "A boolean specifying whether to normalize data to range 0-1.",
                                "default": True
                            },
                            "standardize": {
                                "type": "boolean",
                                "description": "A boolean specifying whether to standardize data to mean 0 and standard deviation 1.",
                                "default": False
                            },
                            "round_digits": {
                                "type": "integer",
                                "description": "An integer representing the number of decimal places to round processed data to.",
                                "default": 2
                            },
                            "filter_outliers": {
                                "type": "boolean",
                                "description": "A boolean specifying whether to filter outliers in the data.",
                                "default": True
                            },
                            "log_transform": {
                                "type": "boolean",
                                "description": "A boolean specifying whether to apply logarithmic transformation to the data.",
                                "default": False
                            }
                        },
                        "required": ["data", "scale", "offset", "min_threshold", "max_threshold"]
                    },
                    "returns": {
                        "type": "object",
                        "properties": {
                            "processed_data": {
                                "type": "array",
                                "items": {
                                    "type": "number"
                                },
                                "description": "A list of float numbers representing the processed data."
                            },
                            "mean": {
                                "type": "number",
                                "description": "A float representing the mean value of processed data."
                            },
                            "std_dev": {
                                "type": "number",
                                "description": "A float representing the standard deviation of processed data."
                            },
                            "min": {
                                "type": "number",
                                "description": "A float representing the minimum value in processed data."
                            },
                            "max": {
                                "type": "number",
                                "description": "A float representing the maximum value in processed data."
                            }
                        }
                    }
                }
            }
        ]
        # 设置函数映射
        functions = [process_data]
        function_map = {f.__name__: f for f in functions}
        msg = self.client.run(
            conversation_id=self.conversation_id,
            query=query,
            tools=tools
        )
        print(msg.model_dump_json(indent=4))

        # 获取最后事件的工具调用信息
        event = msg.content.events[-1]
        tool_call = event.tool_calls[-1]
        name = tool_call.function.name
        args = tool_call.function.arguments

        # 检查和打印参数类型
        print("检查参数类型:")
        for arg_name, arg_value in args.items():
            print(f"参数名称: {arg_name}, 参数值: {arg_value}, 参数类型: {type(arg_value)}")

        # 执行映射函数并返回结果
        # 尝试将返回值转换为字符串，如果无法转换则抛出 TypeError
        raw_result = function_map[name](**args)

        print(raw_result)
        # 传递工具的输出
        msg_2 = self.client.run(
            conversation_id=self.conversation_id,
            tool_outputs=[{
                "tool_call_id": tool_call.id,
                "output": str(raw_result)
            }],
        )
        print(msg_2.model_dump_json(indent=4))'''
    
if __name__ == '__main__':
    unittest.main()
