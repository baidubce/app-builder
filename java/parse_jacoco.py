#!/usr/bin/env python3
import os
import sys
from lxml import etree

def list_all_classes(root):
    """列出报告中的所有类，帮助调试类名是否正确。"""
    classes = root.findall('.//class')
    print("报告中的所有类：")
    for cls in classes:
        print(cls.get('name'))

def main():
    jacoco_report_path = "target/site/jacoco/jacoco.xml"

    # 检查 jacoco.xml 是否存在
    if not os.path.isfile(jacoco_report_path):
        print("jacoco.xml file not found. Please run 'mvn jacoco:report' first.")
        sys.exit(1)

    # 解析 jacoco.xml 文件
    try:
        parser = etree.XMLParser(load_dtd=False, no_network=True, recover=True)
        tree = etree.parse(jacoco_report_path, parser)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        print(f"XML 解析错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"解析 jacoco.xml 时发生错误: {e}")
        sys.exit(1)

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
    for row in table_data:
        if len(row) == 1:
            print(row[0])
        else:
            row_str = ""
            for idx, col in enumerate(row):
                # 左对齐并加上适当的空格
                row_str += col.ljust(col_widths[idx] + 2)
            print(row_str)

def list_all_classes_if_needed(root):
    """如果需要调试，列出所有类名。"""
    list_all_classes(root)

if __name__ == "__main__":
    print("------------------------------------------------------------------------全量覆盖率：------------------------------------------------------------------------")
    main()