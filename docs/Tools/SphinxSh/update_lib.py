import subprocess

def mv_new_md(input_filename, output_filename):
    command  = ['mv', output_filename, input_filename]
    subprocess.run(command, check=True)
    command = ['rm', '-rf', output_filename]
    subprocess.run(command, check=True)

def process_line_for_assistant(line):
    # 仅提取存在module字段且不包含"subpackages"或"submodules"的行，并返回格式处理之后的行
    if 'module' in line.lower() and 'subpackages' not in line.lower() and 'submodules' not in line.lower():
        open_module = ('assistants', 'files', 'messages', 'runs', 'threads')

        parts = line.split('](')

        new_name = parts[0].split(' module')[0].split('.')[-1]
        if new_name in open_module:
            return f"- [{new_name}]({parts[-1]}"
        else:
            return None
    else:
        # 如果行中没有"module"，返回None表示应该删除该行
        return None

def process_line_for_components(line):
    # 仅提取存在module字段且不包含"subpackages"或"submodules"的行，并返回格式处理之后的行
    if 'module' in line.lower() and 'subpackages' not in line.lower() and 'submodules' not in line.lower():
        parts = line.split('](')
        new_names = parts[0].split(' module')[0].split('.')
        if len(new_names) == 5:
            return f"- [{new_names[-2]}]({parts[-1]}"
        else: 
            if new_names[-3] == 'llms':
                return f"- [LLM({new_names[-2]})]({parts[-1]}"
            elif new_names[-3] == 'retriever':
                return f"- [Retriever({new_names[-2]})]({parts[-1]}"
            elif new_names[-3] == 'gbi':
                return f"- [GBI({new_names[-2]})]({parts[-1]}"
    else:
        # 如果行中没有"module"，返回None表示应该删除该行
        return None

def process_file_for_assistant(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_line = process_line_for_assistant(line.strip())
        if new_line:
            new_lines.append(new_line)

    with open(output_filename, 'w') as file:
        for line in new_lines:
            file.write(line + '\n')

    # mv_new_md(input_filename, output_filename)

def process_file_for_components(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_line = process_line_for_components(line.strip())
        if new_line:
            new_lines.append(new_line)

    with open(output_filename, 'w') as file:
        for line in new_lines:
            file.write(line + '\n')

    mv_new_md(input_filename, output_filename)


if __name__ == "__main__":
    # 处理Assistant.md文件
    process_file_for_assistant("../../API-Reference/Python/appbuilder.core.assistant.md", "../../API-Reference/Python/new_appbuilder.core.assistant.md")
    # 处理Components.md文件
    process_file_for_components("../../API-Reference/Python/appbuilder.core.components.md", "../../API-Reference/Python/new_appbuilder.core.components.md")