# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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

"""
单测统一框架，将tests目录下的单测脚本统一执行
"""
import unittest
import os


class CustomTestResult(unittest.TextTestResult):
    """
    自定义单测过程信息打印
    """
    def startTest(self, test):
        """
        start
        """
        super().startTest(test)
        print("Running {} ".format(test.id()), end="")

    def addSuccess(self, test):
        """
        success
        """
        super().addSuccess(test)
        print("Success")

    def addError(self, test, err):
        """
        error
        """
        super().addError(test, err)
        print("Error")

    def addFailure(self, test, err):
        """
        failure
        """
        super().addFailure(test, err)
        print("Failure")


if __name__ == '__main__':
    # 定义测试用例的目录为当前目录
    test_dir = os.path.dirname(__file__)
    # 定义测试用例的匹配模式
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*.py')
    # 运行测试用例， 需要指定环境变量

    for dis in discover:

        cases = []

        for test_case in dis:
            if isinstance(test_case, unittest.TestCase):
                # 获取测试用例的标识符
                case_id = test_case.id()
                case = case_id.split(".")
                cases.append(case[1])
            else:
                # 如果是TestSuite，需要进一步迭代
                for inner_test_case in test_case:
                    case_id = inner_test_case.id()
                    case = case_id.split(".")
                    cases.append(case[1])

        cases = list(set(cases))

        runner = unittest.TextTestRunner(resultclass=CustomTestResult)
        runner.run(dis)
