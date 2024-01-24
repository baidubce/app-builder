import json


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
        elif line.startswith('```') and line[3:].strip() != 'json' and not code_block:
            # 如果紧接着下一行是代码语言，则提取它
            code_lang = line[3:].strip()
            if code_lang is not None and len(code_lang) > 0:
                code_block = True
                continue

            # 检查是否为代码块结束
        elif line.startswith('```') and code_block:
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


# Markdown文档内容
markdown_content = read_markdown("../appbuilder/core/components/asr/README.md")

# 解析Markdown
parsed_content = parse_markdown(markdown_content)

# 打印结果
print(json.dumps(parsed_content, indent=2, ensure_ascii=False))
