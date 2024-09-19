#!/usr/bin/env python3
import os
import sys
import glob
from lxml import etree

def parse_surefire_reports():
    """解析 Maven Surefire 生成的测试报告，打印每个测试的结果，并汇总测试统计信息。"""
    surefire_reports = glob.glob('target/surefire-reports/*.xml')
    if not surefire_reports:
        print("未找到 Surefire 报告文件（target/surefire-reports/*.xml）。")
        return None

    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    passed_tests = []
    failed_tests = []

    print("\n=== 测试结果 ===")
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

        except etree.XMLSyntaxError as e:
            print(f"XML 解析错误在文件 {report}: {e}")
        except Exception as e:
            print(f"解析报告文件 {report} 时发生错误: {e}")

    # 打印测试总结
    print("\n=== 测试总结 ===")
    print(f"总测试数: {total_tests}")
    print(f"成功: {len(passed_tests)}")
    print(f"失败: {total_failures}")
    print(f"错误: {total_errors}")
    print(f"跳过: {total_skipped}")

    return {
        "total_tests": total_tests,
        "passed": len(passed_tests),
        "failures": total_failures,
        "errors": total_errors,
        "skipped": total_skipped
    }

def parse_jacoco():
    """解析 JaCoCo XML 报告，打印覆盖率详情。"""
    JACOCO_XML = "target/site/jacoco/jacoco.xml"
    if not os.path.isfile(JACOCO_XML):
        print("jacoco.xml 未找到。请先运行 'mvn jacoco:report' 生成报告。")
        return

    try:
        parser = etree.XMLParser(load_dtd=False, no_network=True, recover=True)
        tree = etree.parse(JACOCO_XML, parser)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        print(f"XML 解析错误: {e}")
        return
    except Exception as e:
        print(f"解析 jacoco.xml 时发生错误: {e}")
        return

    # 初始化总计数器
    total_lines_missed = 0
    total_lines_covered = 0

    # 创建数据表
    table_data = [["Class", "Line Coverage (%)", "Missing Lines"]]

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
                    # 查找 mi > 0 的行号
                    missing_lines = [
                        str(int(line.get('nr'))) 
                        for line in sourcefile_element.findall('line') 
                        if line.get('mi') and int(line.get('mi')) > 0
                    ]
                    missing_lines_str = ",".join(missing_lines) if missing_lines else "-"
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

    # 打印数据表
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

def generate_incremental_coverage():
    """生成增量代码覆盖率报告。"""
    JACOCO_XML = "target/site/jacoco/jacoco.xml"
    BASE_BRANCH = "origin/master"
    
    # 安装 diff-cover，如果未安装
    if not shutil.which("diff-cover"):
        print("diff-cover 未找到，正在安装...")
        os.system("pip install --user diff-cover")
    
    # 检查 jacoco.xml 文件是否存在
    if os.path.isfile(JACOCO_XML):
        print("\njacoco.xml 已找到。")
    else:
        print("\njacoco.xml 未找到。请先运行 'mvn jacoco:report' 生成报告。")
        return
    
    # 生成修改的 Java 文件列表
    os.system(f"git diff {BASE_BRANCH} --name-only -- '*.java' > diff_files.txt")

    # 检查 diff_files.txt 是否有内容
    if os.path.getsize("diff_files.txt") > 0:
        print("\n生成增量代码覆盖率报告...")
        result = os.system(f"diff-cover {JACOCO_XML} --compare-branch={BASE_BRANCH} --html-report coverage_diff.html")
        if result != 0:
            print("生成增量覆盖率报告失败。")
            os.remove("diff_files.txt")
            sys.exit(1)
        else:
            print("增量覆盖率报告已生成在 coverage_diff.html。")
    else:
        print("\n相对于 {BASE_BRANCH}，没有修改的 Java 文件。未生成增量覆盖率报告。")

    # 清理临时文件
    os.remove("diff_files.txt")

def main():
    """主函数，执行所有步骤。"""
    # 解析测试报告并打印结果
    test_results = parse_surefire_reports()



    parse_jacoco()


    # 生成增量覆盖率报告
    generate_incremental_coverage()

if __name__ == "__main__":
    import shutil  # 用于检查 diff-cover 是否存在
    main()