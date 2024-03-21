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
import re
import sys

arguments = sys.argv

sdk_code_dict = {
    "animal_recognize": "animal_recognize",
    "asr": "asr",
    "dish_recognize": "dish_recognize",
    "doc_crop_enhance": "doc_crop_enhance",
    "doc_parser": "doc_parser",
    "doc_splitter": "doc_splitter",
    "embeddings": "embeddings",
    "excel2figure": "excel2figure",
    "extract_table": "extract_table",
    "nl2sql": "nl2sql",
    "select_table": "select_table",
    "general_ocr": "general_ocr",
    "handwrite_ocr": "handwrite_ocr",
    "image_understand": "image_understand",
    "landmark_recognize": "landmark_recognize",
    "dialog_summary": "dialog_summary",
    "is_complex_query": "is_complex_query",
    "mrc": "mrc",
    "nl2pandas": "nl2pandas",
    "oral_query_generation": "oral_query_generation",
    "playground": "playground",
    "qa_pair_mining": "qa_pair_mining",
    "query_decomposition": "query_decomposition",
    "query_rewrite": "query_rewrite",
    "similar_question": "similar_question",
    "style_rewrite": "style_rewrite",
    "style_writing": "style_writing",
    "tag_extraction": "tag_extraction",
    "matching": "matching",
    "mix_card_ocr": "mix_card_ocr",
    "object_recognize": "object_recognize",
    "plant_recognize": "plant_recognize",
    "qrcode_ocr": "qrcode_ocr",
    "rag_with_baidu_search": "web_search",
    "bes": "retriever",
    "table_ocr": "table_ocr",
    "text_to_image": "image",
    "translate": "translate",
    "tts": "tts",
    "tts_high": "tts_high",
    "tts_audio": "tts_audio",
    "code_interpreter": "code_interpreter",
    "web_pilot": "web_pilot",
    "wolfram_alpha": "wolfram_alpha",
    "arxiv": "arxiv",
    "product_query": "product_query",
    "flight_query": "flight_query",
    "query_express_package": "query_express_package",
    "bing_image_search": "bing_image_search",
    "news_get": "news_get",
    "weather_query": "weather_query",
    "video_get": "video_get",
    "baidu_vdb": "baidu_vdb"

}

# 循环中的数据
sdk_detail_sqls = []
sdk_component_sqls = []
sdk_code_sqls = []


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
        # 检查是否为一级标题
        if line.startswith('# ') and 'title' not in sections:
            sections['title'] = line[2:].strip()
            sections['name'] = re.sub(r'[\(（][^\)）]*[\)）]', '', sections['title']).strip()
        # 检查是否为二级标题
        if line.startswith('## '):
            # 如果当前有正在处理的section，将其存入字典
            if current_section and current_section not in sections:
                sections[current_section] = section_content.strip()

            # 更新当前section名称和重置section内容
            current_section = line[3:].strip()
            section_content = ""
            need_append_content = False
            if current_section == '简介':
                sections['remark'] = ''

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
            # 判断当前section 是否是简介
            if current_section == '简介' and not line.startswith('##') and not need_append_content:
                sections['remark'] = sections['remark'] + line
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
                match = re.search(r'/(\w+)/README\.md$', file_path)
                dir_name = match.group(1)
                introduce = parsed_content.get('简介').replace('\n', r'\n').replace('\'', '\'\'')
                interface_doc = parsed_content.get('参数说明').replace('\n', r'\n').replace('\'', '\'\'')
                sdk_code = sdk_code_dict.get(dir_name)
                if sdk_code is not None:
                    sdk_detail_sql = f"insert into sdk_detail(sdk_code, introduce, interface_doc, deploy_package, title) values('{sdk_code}','{introduce}','{interface_doc}',null,'{parsed_content.get('title')}') on conflict(sdk_code) do update set introduce='{introduce}',interface_doc='{interface_doc}',title='{parsed_content.get('title')}';"
                    sdk_detail_sqls.append(sdk_detail_sql)
                    remark = parsed_content.get('remark').replace('\n', '')
                    sdk_component_sql = f"update sdk_tool set name = '{parsed_content.get('name')}',remark='{remark}' where sdk_code = '{sdk_code}';"
                    sdk_component_sqls.append(sdk_component_sql)
                    for key, value in parsed_content.get('基本用法').items():
                        code = value.replace('\n', r'\n').replace('\'', '\'\'')
                        sdk_code_sql = f"insert into sdk_code_demo(sdk_code, language, code_demo) values('{sdk_code}','{key}','{code}') on conflict(sdk_code,language) do update set code_demo='{code}';"
                        sdk_code_sqls.append(sdk_code_sql)
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

# 打开文件以追加模式 ('a')
# with open('data.sql', 'a') as file:
#     # 循环写入数据
#     for line in sdk_detail_sqls:
#         file.write(line + '\n')
#     for line in sdk_code_sqls:
#         file.write(line + '\n')
#     for line in sdk_component_sqls:
#         file.write(line + '\n')
