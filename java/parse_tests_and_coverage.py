#!/usr/bin/env python3
import os
import sys
import subprocess
import glob  # 添加这一行
from lxml import etree
from git import Repo
from collections import defaultdict

def parse_surefire_reports():
    """解析 Maven Surefire 生成的测试报告，打印每个测试的结果，并汇总测试统计信息。"""
    surefire_reports = glob.glob('target/surefire-reports/*.xml')
    if not surefire_reports:
        print("未找到 Surefire 报告文件（target/surefire-reports/*.xml）。")
        sys.stdout.flush()  # 立即刷新输出
        return None

    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    passed_tests = []
    failed_tests = []

    print("\n=== 测试结果 ===")
    sys.stdout.flush()  # 立即刷新输出
    for report in surefire_reports:
        try:
            tree = etree.parse(report)
            root = tree.getroot()
            test_suite_name = root.get('name', 'Unknown Test Suite')

            for test_case in root.findall('testcase'):
                test_name = test_case.get('name')
                class_name = test_case.get('classname')
                status = "OK"
                error_message = ""
                if test_case.find('failure') is not None:
                    status = "FAIL"
                    error = test_case.find('failure')
                    error_message = error.text.strip() if error.text else "未知错误"
                    failed_tests.append((class_name, test_name, error_message))
                    total_failures += 1
                elif test_case.find('error') is not None:
                    status = "ERROR"
                    error = test_case.find('error')
                    error_message = error.text.strip() if error.text else "未知错误"
                    failed_tests.append((class_name, test_name, error_message))
                    total_errors += 1
                elif test_case.find('skipped') is not None:
                    status = "SKIPPED"
                    total_skipped += 1
                else:
                    passed_tests.append((class_name, test_name))

                total_tests += 1

                # 打印每个测试的结果
                if status == "OK":
                    print(f"[OK] {class_name}.{test_name}")
                elif status in ["FAIL", "ERROR"]:
                    print(f"[{status}] {class_name}.{test_name}")
                    print(f"      错误信息: {error_message}")
                elif status == "SKIPPED":
                    print(f"[SKIPPED] {class_name}.{test_name}")
                sys.stdout.flush()  # 立即刷新输出

        except etree.XMLSyntaxError as e:
            print(f"XML 解析错误在文件 {report}: {e}")
            sys.stdout.flush()  # 立即刷新输出
        except Exception as e:
            print(f"解析报告文件 {report} 时发生错误: {e}")
            sys.stdout.flush()  # 立即刷新输出

    # 打印测试总结
    print("\n=== 测试总结 ===")
    print(f"总测试数: {total_tests}")
    print(f"成功: {len(passed_tests)}")
    print(f"失败: {total_failures}")
    print(f"错误: {total_errors}")
    print(f"跳过: {total_skipped}")
    sys.stdout.flush()  # 立即刷新输出

    return {
        "total_tests": total_tests,
        "passed": len(passed_tests),
        "failures": total_failures,
        "errors": total_errors,
        "skipped": total_skipped
    }

def parse_jacoco():
    """解析 JaCoCo XML 报告，打印覆盖率详情并返回包含类名和未覆盖行号的字典。"""
    JACOCO_XML = "target/site/jacoco/jacoco.xml"
    
    if not os.path.isfile(JACOCO_XML):
        print("jacoco.xml 未找到。请先运行 'mvn jacoco:report' 生成报告。")
        sys.stdout.flush()  # 立即刷新输出
        return {}

    try:
        parser = etree.XMLParser(load_dtd=False, no_network=True, recover=True)
        tree = etree.parse(JACOCO_XML, parser)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        print(f"XML 解析错误: {e}")
        sys.stdout.flush()  # 立即刷新输出
        return {}
    except Exception as e:
        print(f"解析 jacoco.xml 时发生错误: {e}")
        sys.stdout.flush()  # 立即刷新输出
        return {}

    # 初始化总计数器
    total_lines_missed = 0
    total_lines_covered = 0

    # 创建数据表
    table_data = [["Class", "Line Coverage (%)", "Missing Lines"]]

    # 初始化存储结果的字典
    coverage_data = {}

    # 遍历所有 class 元素
    for class_element in root.findall('.//class'):
        class_name = class_element.get('name')
        counter_line = class_element.find("counter[@type='LINE']")
        if counter_line is not None:
            lines_missed = int(counter_line.get('missed', '0'))
            lines_covered = int(counter_line.get('covered', '0'))
        else:
            lines_missed = 0
            lines_covered = 0

        total_lines_missed += lines_missed
        total_lines_covered += lines_covered

        # 获取 sourcefilename 属性
        sourcefilename = class_element.get('sourcefilename')
        if sourcefilename:
            package_element = class_element.getparent()
            if package_element is not None and package_element.tag == 'package':
                sourcefile_element = package_element.find(f"sourcefile[@name='{sourcefilename}']")
                if sourcefile_element is not None:
                    # 查找 mi > 0 的行号（未覆盖的行）
                    missing_lines = [
                        int(line.get('nr')) 
                        for line in sourcefile_element.findall('line') 
                        if line.get('mi') and int(line.get('mi')) > 0
                    ]
                    missing_lines_str = ",".join(map(str, missing_lines)) if missing_lines else "-"
                else:
                    missing_lines_str = "N/A"
            else:
                missing_lines_str = "N/A"
        else:
            missing_lines_str = "N/A"

        # 计算行覆盖率
        total_lines = lines_missed + lines_covered
        if total_lines > 0:
            coverage = (lines_covered / total_lines) * 100
        else:
            coverage = 0.0

        table_data.append([class_name, f"{coverage:.2f}%", missing_lines_str])

        # Populate coverage_data dictionary if there are missing lines
        if missing_lines_str != "N/A" and missing_lines_str != "-":
            coverage_data[class_name] = [int(line) for line in missing_lines_str.split(',')]

    # 计算总覆盖率
    total_lines = total_lines_missed + total_lines_covered
    if total_lines > 0:
        total_coverage = (total_lines_covered / total_lines) * 100
    else:
        total_coverage = 0.0

    # 添加总覆盖率到数据表
    table_data.append(["-----------------------------", "----------------", "----------------"])
    table_data.append(["Total Line Coverage:", f"{total_coverage:.2f}%", ""])

    # 计算每列的最大宽度
    num_columns = len(table_data[0])
    col_widths = [0] * num_columns
    for row in table_data:
        for idx, col in enumerate(row):
            if len(col) > col_widths[idx]:
                col_widths[idx] = len(col)

    # 打印覆盖率详情
    print("\n=== 覆盖率详情 ===")
    for row in table_data:
        if len(row) == 1:
            print(row[0])
        else:
            row_str = ""
            for idx, col in enumerate(row):
                # 左对齐并加上适当的空格
                row_str += col.ljust(col_widths[idx] + 2)
            print(row_str)
        sys.stdout.flush()  # 立即刷新输出

    return coverage_data

def get_modified_files(repo, base_branch, path_pattern='src/main/**/*.java'):
    """
    获取相对于 base_branch 的修改文件及其修改的行号
    返回一个字典：{file_path: set(line_numbers)}
    """
    # 获取 diff 输出，带有行号
    diff_command = [
        'git', 'diff', base_branch, '--unified=0', '--', path_pattern
    ]
    try:
        diff_output = subprocess.check_output(diff_command, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"执行 git diff 失败: {e.output.decode('utf-8')}")
        sys.stdout.flush()
        sys.exit(1)
    
    modified_files = defaultdict(set)  # {file_path: set(line_numbers)}
    current_file = None
    line_num = 0

    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            parts = line.split()
            if len(parts) >= 4:
                a_path = parts[2][2:]
                b_path = parts[3][2:]
                current_file = b_path  # 使用新文件路径
        elif line.startswith('@@'):
            if current_file:
                # 解析 hunk header
                # 格式: @@ -start,count +start,count @@
                hunk_header = line
                try:
                    hunk_info = hunk_header.split(' ')[1:3]
                    new_hunk = hunk_info[1]
                    start, count = new_hunk[1:].split(',')
                    start = int(start)
                    count = int(count)
                except Exception as e:
                    print(f"解析 hunk header 失败: {hunk_header}, 错误: {e}")
                    sys.stdout.flush()
                    continue
                line_num = start
        elif line.startswith('+') and not line.startswith('+++'):
            if current_file:
                modified_files[current_file].add(line_num)
                line_num += 1
        elif line.startswith('-') and not line.startswith('---'):
            # 删除的行，不需要增加 line_num
            pass
        else:
            # 其他情况，不处理
            pass

    return modified_files

def generate_incremental_coverage_report(modified_files, coverage_data):
    """
    生成增量代码覆盖率报告
    """
    total_modified = 0
    total_uncovered = 0
    per_file_report = []

    # 遍历修改的文件和行号
    for file_path, modified_lines in modified_files.items():
        # 将文件路径转换为类名，去掉 'java/src/main/java/' 和 '.java'
        class_name = file_path.replace('java/src/main/java/', '').replace('.java', '')
        # 从 coverage_data 中查找对应的类名
        missing_lines = coverage_data.get(class_name, [])
        # 计算被覆盖和未被覆盖的行
        uncovered_in_modified = modified_lines.intersection(missing_lines)
        covered_in_modified = modified_lines.difference(missing_lines)

        total_modified += len(modified_lines)
        total_uncovered += len(uncovered_in_modified)

        # 保存每个文件的报告
        per_file_report.append({
            'file': file_path,
            'modified': sorted(modified_lines),
            'covered': sorted(covered_in_modified),
            'uncovered': sorted(uncovered_in_modified)
        })

    # 计算增量覆盖率
    coverage_percent = ((total_modified - total_uncovered) / total_modified) * 100 if total_modified > 0 else 0.0

    # 生成报告输出
    report_lines = []
    report_lines.append("=== 增量代码覆盖率报告 ===\n")
    for file_report in per_file_report:
        report_lines.append(f"文件: {file_report['file']}")
        report_lines.append(f"修改的行数: {len(file_report['modified'])}")
        report_lines.append(f"被覆盖的行数: {len(file_report['covered'])}")
        report_lines.append(f"未被覆盖的行数: {len(file_report['uncovered'])}")
        if file_report['uncovered']:
            report_lines.append(f"未覆盖的行号: {', '.join(map(str, file_report['uncovered']))}")
        report_lines.append("\n")

    # 增量覆盖率总结
    report_lines.append("=== 总结 ===")
    report_lines.append(f"总修改行数: {total_modified}")
    report_lines.append(f"总未被覆盖行数: {total_uncovered}")
    report_lines.append(f"增量覆盖率: {coverage_percent:.2f}%")

    report = "\n".join(report_lines)
    print(report)
    sys.stdout.flush()

    return {
        'total_modified': total_modified,
        'total_uncovered': total_uncovered,
        'coverage_percent': coverage_percent,
        'details': per_file_report
    }


def main():
    """主函数，执行所有步骤。"""
    parse_surefire_reports()
    # 假设 parse_jacoco() 已经正确返回了覆盖率数据字典
    coverage_data = parse_jacoco()

    # 获取增量修改的文件及行号
    repo = Repo(os.getcwd(), search_parent_directories=True)
    base_branch = "upstream/master"
    modified_files = get_modified_files(repo, base_branch, path_pattern='src/main/**/*.java')

    # 生成增量覆盖率报告
    generate_incremental_coverage_report(modified_files, coverage_data)


if __name__ == "__main__":
    main()