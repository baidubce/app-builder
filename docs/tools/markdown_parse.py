"""
markdown 文件解析工具
使用示例：
python markdown_parse.py "your_file_path"
响应结果：
parse file your_file_path/README.md result:   xxxx
check your_file_path/README.md success/error:  xxxx

如果出现 error，说明 markdown 内容缺失 简介、基本用法或者参数说明
"""
import json
import os
import sys

arguments = sys.argv


def parse_markdown(markdown):
    # 初始化结果字典和当前处理的section
    sections = {}
    current_section = None
    code_block = False
    code_lang = None
    code_content = ""
    section_content = ""
    need_append_content = False
    # 按行遍历markdown内容
    for line in markdown.split('\n'):
        # 检查是否为二级标题
        if line.startswith('## '):
            # 如果当前有正在处理的section，将其存入字典
            if current_section and current_section not in sections:
                sections[current_section] = section_content.strip()

            # 更新当前section名称和重置section内容
            current_section = line[3:].strip()
            section_content = ""
            need_append_content = False

            # 检查是否为代码块开始
        elif line.startswith('```') and current_section == '基本用法' and not code_block:
            # 如果紧接着下一行是代码语言，则提取它
            code_lang = line[3:].strip()
            if code_lang is not None and len(code_lang) > 0:
                code_block = True
                continue

            # 检查是否为代码块结束
        elif line.startswith('```') and current_section == '基本用法' and code_block:
            code_block = False
            # 如果提取到了代码语言，将代码内容存入字典
            if code_lang:
                if current_section not in sections:
                    sections[current_section] = {}
                sections[current_section][code_lang] = code_content.strip()
            code_lang = None
            code_content = ""
            continue

            # 如果在代码块内，则累加代码内容
        if code_block:
            code_content += line + '\n'
            # 否则，累加section内容
        else:
            if line.startswith('###'):
                need_append_content = True
            if need_append_content:
                section_content += line + '\n'

    # 处理最后一个section
    if current_section:
        sections[current_section] = section_content.strip()

    return sections


def read_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown = file.read()
        return markdown


def check_parse_result(result):
    msg_list = []
    success = True
    json_data = json.loads(result)
    if "简介" not in json_data or ("简介" in json_data and len(json_data["简介"]) == 0):
        success = False
        msg_list.append("简介内容缺失")
    if "基本用法" not in json_data or ("基本用法" in json_data and len(json_data["基本用法"]) == 0):
        success = False
        msg_list.append("基本用法内容缺失")
    if "参数说明" not in json_data or ("参数说明" in json_data and len(json_data["参数说明"]) == 0):
        success = False
        msg_list.append("参数说明内容缺失")
    return success, ";".join(msg_list)


def parse_file(file_path):
    if os.path.isfile(file_path):
        # 如果是文件，且为 markdown，解析文档
        _, file_extension = os.path.splitext(file_path)
        if file_extension == '.md':
            markdown_content = read_markdown(file_path)
            parsed_content = parse_markdown(markdown_content)
            result = json.dumps(parsed_content, indent=2, ensure_ascii=False)
            print(f"parse file {file_path} result:\n {result}")
            success, _msg = check_parse_result(result)
            if success:
                print(f"check {file_path} success")
            if not success:
                print(f"check {file_path} error: {_msg}")
            return
    else:
        # 获取目标目录下的所有文件和子目录
        entries = os.listdir(file_path)
        for entry in entries:
            # 构建完整路径
            child_path = os.path.join(file_path, entry)
            parse_file(child_path)


parse_file(arguments[1])
