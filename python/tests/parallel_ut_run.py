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


# add test
import os
import sys
import multiprocessing
import subprocess
import shutil
import copy
import time
from collections import deque
import logging
import coverage

logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.propagate = False
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(current_path)

"""
将Unittest Case分为以下几类
1、SKIP_UNITTEST
2、CPU_PARALLEL_RUN_UNITTEST
3、CPU_SERIAL_RUN_UNITTEST
4、UNKNOWN_UNITTEST
"""

# Coverage 运行命令
COVERAGE_CMD = ["coverage", "run", "--pylib", "--source=appbuilder.core,appbuilder.utils", "--parallel-mode"]

# 需要跳过的单测用例
SKIP_UNITTEST = []

# 可以CPU并行的单测用例
CPU_PARALLEL_RUN_UNITTEST = []

# 分类未知，故在CPU上串行执行的单测用例
UNKNOWN_UNITTEST = []


def choose_test_case(file):
    """
    选择测试用例，根据不同的环境变量选择对应的测试用例。如果没有找到指定的测试用例，则返回。

    Args:
        file (str): 文件路径，包含完整路径和文件名。

    Returns:
        None, str: 无返回值，如果找到了指定的测试用例，将其添加到相应的列表中；否则，返回None。
    """
    skip_case_str = '@unittest.skip('
    cpu_parallel_str = '@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL"'

    with open(file, 'r') as f:
        all_line = f.readlines()

        if list(set([line.strip().find(skip_case_str) for line in all_line])) != [-1]:
            SKIP_UNITTEST.append(file.split("/")[-1])
            return

        if list(set([line.strip().find(cpu_parallel_str) for line in all_line])) != [-1]:
            CPU_PARALLEL_RUN_UNITTEST.append(file.split("/")[-1])
            return

        UNKNOWN_UNITTEST.append(file.split("/")[-1])
        return


def get_all_unittest_file():
    """
    获取当前目录下所有以test开头的.py文件，并返回一个列表，包含这些文件的完整路径名。

    Args:
        无参数。

    Returns:
        list (list[str]): 返回一个列表，包含所有以test开头的.py文件的完整路径名。如果没有找到任何文件，则返回一个空列表。
    """
    for root, _, fs in os.walk(current_path):
        for f in fs:
            file = f.split(".")[-1]
            prefix = f.split(".")[0].split("_")[0]
            if file == "py" and prefix == "test":
                fullname = os.path.join(root, f)
                choose_test_case(fullname)
    
    logger.info("\n需要跳过的单测用例：{}个".format(len(SKIP_UNITTEST)))
    for idx, case in enumerate(SKIP_UNITTEST):
        logger.info("--> {}. {}".format(idx+1, case))

    logger.info("\nCPU并行的单测用例：{}个".format(len(CPU_PARALLEL_RUN_UNITTEST)))
    for idx, case in enumerate(CPU_PARALLEL_RUN_UNITTEST):
        logger.info("--> {}. {}".format(idx+1, case))

    logger.info("\nCPU串行执行的单测用例：{}个".format(len(UNKNOWN_UNITTEST)))
    for idx, case in enumerate(UNKNOWN_UNITTEST):
        logger.info("--> {}. {}".format(idx+1, case))


def pull_last_n_log(ut_context, file_name, line_count=80):
    """
    打印最后的line_count行日志，默认为80行。

    Args:
        ut_context (dict): 测试用例上下文字典，包含了log_file字段，表示错误日志文件路径。
        file_name (str): 要打印的日志文件名称，将会显示在日志前面。
        line_count (int, optional): 要打印的行数，默认为80行。

    Returns:
        None.
    """
    sys.stdout.write("\nError LOG of {}, at {} :\n".format(
        file_name, os.path.abspath(ut_context["log_file"])))
    if ut_context["log_file"]:
        prefix = "|{} Error LOG| ".format(file_name)
        sys.stdout.write(
            prefix + prefix.join(deque(open(ut_context["log_file"], 'r', encoding='utf-8'), line_count)))


def run_sync_unittest(test_file):
    """
    同步运行单元测试
    
    Args:
        test_file (str): 测试文件名
    
    Returns:
        dict: 包含进程对象、日志文件对象以及开始时间的字典
    
    """
    default_env = os.environ.copy()
    current_env = copy.copy(default_env)
    current_env["PYTHONPATH"] = parent_path + os.pathsep + current_env.get("PYTHONPATH", "")
    cmd = COVERAGE_CMD + [test_file]
    log = open("{}/ut_logs/{}_run.log".format(current_path, test_file), "w")
    begin_time = time.time()
    proc = subprocess.Popen(
        cmd, env=current_env, cwd=current_path, stdout=log, stderr=log)
    return {"process": proc, "log": log, "begin_time": begin_time}


def run_async_unittest(test_file, case_idx, case_num, timeout=1200):
    """
    异步运行单元测试，并记录日志文件和结果。

    Args:
        test_file (str): 测试文件名，包含路径。
        case_idx (int): 当前测试用例在所有测试用例中的索引值，从1开始。
        case_num (int): 所有测试用例的数量。
        timeout (int, optional): 超时时间，默认为1200秒（20分钟）。

    Returns:
        None, str: 无返回值，会将结果写入到一个文件中。
    """
    default_env = os.environ.copy()
    current_env = copy.copy(default_env)
    current_env["PYTHONPATH"] = parent_path + os.pathsep + current_env.get("PYTHONPATH", "")
    cmd = COVERAGE_CMD + [test_file]
    log_file = "{}/ut_logs/{}_run.log".format(current_path, test_file)
    log = open(log_file, "w")
    begin_time = time.time()
    proc = subprocess.Popen(
        cmd, env=current_env, cwd=current_path, stdout=log, stderr=log)

    proc.wait(timeout)
    ret = proc.poll()

    end_time = time.time()
    with open("ut_logs/{}_res".format(test_file), "w+") as f:
        f.write(str({"name": test_file, "time": end_time -
                begin_time, "status": ret, "log_file": log_file}))
    logger.info("[{}] Test Case : {}/{} 耗时: {:.2f} s --> {}".format("OK" if ret == 0 else "ERROR",
                                                                    case_idx, case_num, end_time - begin_time, test_file,))
    return

def parallel_execute_unittest(test_cases, parallel_num=2):
    case_num = len(test_cases)
    success_cases = []
    failed_cases = []

    process_pool = multiprocessing.Pool(processes=6)
    for idx, test_file in enumerate(test_cases):
        process_pool.apply_async(
            run_async_unittest, args=(test_file, idx+1, case_num,))

    process_pool.close()
    process_pool.join()
    total_case_time = 0

    for case in test_cases:
        if not os.path.exists("ut_logs/{}_res".format(case)):
            continue
        with open("ut_logs/{}_res".format(case), 'r') as f:
            line = f.readlines()[0]
            message = eval(line.split("\n")[0])

        if message["status"] == 0:
            if message["name"] not in success_cases:
                success_cases.append(message["name"])
        else:
            if message["name"] not in failed_cases:
                failed_cases.append(message["name"])
                pull_last_n_log(message, message["name"], )
        total_case_time += message["time"]

    return success_cases, failed_cases, total_case_time


def run_cpu_parallel_unittest():
    os.environ["TEST_CASE"] = "CPU_PARALLEL"
    logger.info("\n================ CPU_PARALLEL ================\n")

    begin_time = time.time()
    success_cases, failed_cases, total_case_time = parallel_execute_unittest(
        CPU_PARALLEL_RUN_UNITTEST)

    logger.info("\n CPU_PARALLEL 运行成功单测：{} 个".format(len(success_cases)))

    if len(failed_cases) > 0:
        logger.info("\n以下单测失败，将重试运行 2 次")
        for case in failed_cases:
            logger.info("retry case --> {}".format(case))
        retry_success_cases, retry_failed_cases, retry_case_time = parallel_execute_unittest(
            failed_cases, 1)

        total_case_time += retry_case_time

        for success in retry_success_cases:
            failed_cases.remove(success)
    
        if len(retry_failed_cases) > 0:
            logger.info("\n以下单测失败，将重试运行 1 次")
            for case in retry_failed_cases:
                logger.info("retry case --> {}".format(case))
            second_success_cases, second_failed_cases, second_case_time = parallel_execute_unittest(
                retry_failed_cases, 1)
            total_case_time += second_case_time
            for success in second_success_cases:
                failed_cases.remove(success)

    end_time = time.time()
    logger.info("\n CPU_PARALLEL 运行失败单测： {} 个".format(len(failed_cases)))
    for failed in failed_cases:
        logger.info("--> {}".format(failed))

    logger.info("\n CPU_PARALLEL 单测并行运行总计耗时 {} s".format(
        end_time - begin_time))
    logger.info("\n CPU_PARALLEL 单测串行运行总计耗时 {} s".format(
        total_case_time))

    return success_cases, failed_cases, end_time - begin_time

def run_unknown_unittest():
    os.environ["TEST_CASE"] = "CPU_SERIAL"
    logger.info("\n================ CPU_SERIAL ================\n")

    begin_time = time.time()
    success_cases, failed_cases, total_case_time = parallel_execute_unittest(
        UNKNOWN_UNITTEST, 1)

    logger.info("\n CPU_SERIAL 运行成功单测：{} 个".format(len(success_cases)))

    if len(failed_cases) > 0:
        logger.info("\n以下单测失败，将重试运行一次")
        for case in failed_cases:
            logger.info("retry case --> {}".format(case))
        retry_success_cases, retry_failed_cases, retry_case_time = parallel_execute_unittest(
            failed_cases, 1)

        total_case_time += retry_case_time

        for success in retry_success_cases:
            failed_cases.remove(success)

    end_time = time.time()
    logger.info("\n CPU_SERIAL 运行失败单测： {} 个".format(len(failed_cases)))
    for failed in failed_cases:
        logger.info("--> {}".format(failed))

    logger.info("\n CPU_SERIAL 单测并行运行总计耗时 {} s".format(
        end_time - begin_time))
    logger.info("\n CPU_SERIAL 单测串行运行总计耗时 {} s".format(
        total_case_time))

    return success_cases, failed_cases, end_time - begin_time


def create_unittest_report():
    """
    生成单元测试报告。
    
    Args:
        无。
    
    Returns:
        无返回值。
    
    """
    # 创建日志目录
    if not os.path.exists("./ut_logs"):
        os.mkdir("./ut_logs")

    get_all_unittest_file()
    total_success_cases = []
    total_failed_cases = []
    total_ut_time = 0

    test_suite = [run_cpu_parallel_unittest, run_unknown_unittest]
    for suite in test_suite:
        success_cases, failed_cases, suite_time = suite()
        total_success_cases += success_cases
        total_failed_cases += failed_cases
        total_ut_time += suite_time
    
    logger.info("============== Summary Report =============")
    logger.info("\nCI运行结束，总耗时：{}".format(total_ut_time))
    if len(total_failed_cases) != 0:
        logger.info("\nCI 运行失败！Failed Case 如下: ")
        for case in total_failed_cases:
            logger.info("ERROR： {}".format(case))
        exit(1)
    else:
        logger.info("\nCI 运行成功！")

    # shutil.rmtree("./ut_logs")


if __name__ == '__main__':
    create_unittest_report()
