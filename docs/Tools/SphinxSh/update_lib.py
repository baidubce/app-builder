import subprocess

def mv_new_md(input_filename, output_filename):
    """
    将新生成的Markdown文件移动到目标位置并删除原文件。
    
    Args:
        input_filename (str): 目标文件名。
        output_filename (str): 新生成的Markdown文件名。
    
    Returns:
        None
    
    """
    command  = ['mv', output_filename, input_filename]
    subprocess.run(command, check=True)
    command = ['rm', '-rf', output_filename]
    subprocess.run(command, check=True)

def process_line_for_assistant(line):
    """
    处理一行文本以供助手使用。
    
    Args:
        line (str): 要处理的文本行。
    
    Returns:
        str or None: 如果行中包含'module'字段且不包含"subpackages"或"submodules"，则返回处理后的行。
                     否则返回None表示应该删除该行。
    
    说明：
        1. 仅提取存在'module'字段且不包含"subpackages"或"submodules"的行，并返回格式处理之后的行。
        2. 处理后的行格式为"- [模块名](链接)"，其中模块名为文本行中最后一个点后的内容，
           链接为原文本行中的链接部分。
        3. 如果模块名在指定的模块列表中（'assistants', 'files', 'messages', 'runs', 'threads'），
           则返回处理后的行，否则返回None。
    """
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
    """
    对给定的行进行组件处理。
    
    Args:
        line (str): 需要处理的行。
    
    Returns:
        str or None: 处理后的行。如果行中没有包含"module"字段，或者包含"subpackages"或"submodules"，则返回None，表示应该删除该行。
    
    """
    # 仅提取存在module字段且不包含"subpackages"或"submodules"的行，并返回格式处理之后的行
    if 'module' in line.lower() and 'subpackages' not in line.lower() and 'submodules' not in line.lower():
        parts = line.split('](')
        new_names = parts[0].split(' module')[0].split('.')
        if len(new_names) == 5:
            return f"- [{new_names[-2]}]({parts[-1]}"
        else: 
            if new_names[-3] == 'llms':
                return f"- [{new_names[-2]}--(LLM)]({parts[-1]}"
            elif new_names[-3] == 'retriever':
                return f"- [{new_names[-2]}--(retriever)]({parts[-1]}"
            elif new_names[-3] == 'gbi':
                return f"- [{new_names[-2]}--(GBI)]({parts[-1]}"
    else:
        # 如果行中没有"module"，返回None表示应该删除该行
        return None

def process_line_for_console(line):
    """
    对给定行进行格式处理，并返回处理后的行。
    
    Args:
        line (str): 需要处理的行文本。
    
    Returns:
        str: 处理后的行文本，如果行应被删除则返回None。
    
    说明:
        该函数仅处理包含"module"字段且不包含"subpackages"或"submodules"的行。
        对于包含"module"的行，会提取模块名并返回格式化后的Markdown链接。
        如果模块名是"data_class"，则直接返回None。
        如果行中包含"(appbuilder.core.console.knowledge_base.md)"，则返回固定的Markdown链接。
        如果行中不包含"module"，则返回None表示该行应被删除。
    """
    # 仅提取存在module字段且不包含"subpackages"或"submodules"的行，并返回格式处理之后的行
    if 'module' in line.lower() and 'subpackages' not in line.lower() and 'submodules' not in line.lower():
        parts = line.split('](')
        new_names = parts[0].split(' module')[0].split('.')
        if new_names[-1] == 'data_class':
            return None
        else:
            return f"- [{new_names[-1]}]({parts[-1]}"
    elif '(appbuilder.core.console.knowledge_base.md)' in line:
        return "- [knowledge_base](appbuilder.core.console.knowledge_base.md)"
    else:
        # 如果行中没有"module"，返回None表示应该删除该行
        return None
    
def process_file_for_assistant(input_filename, output_filename):
    """
    为助手处理文件。
    
    Args:
        input_filename (str): 输入文件名。
        output_filename (str): 输出文件名。
    
    Returns:
        None
    
    """
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

    mv_new_md(input_filename, output_filename)

def process_file_for_components(input_filename, output_filename):
    """
    从文件中读取文本行，处理每行文本以提取组件信息，并将结果写入到新的文件中。
    
    Args:
        input_filename (str): 输入文件的路径。
        output_filename (str): 输出文件的路径。
    
    Returns:
        None
    
    """
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


def process_file_for_console(input_filename, output_filename):
    """
    将文件内容处理后输出到另一个文件，并移动原文件。
    
    Args:
        input_filename (str): 输入文件名。
        output_filename (str): 输出文件名。
    
    Returns:
        None
    
    """
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_line = process_line_for_console(line.strip())
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
    # 处理console.md文件
    process_file_for_console("../../API-Reference/Python/appbuilder.core.console.md", "../../API-Reference/Python/new_appbuilder.core.console.md")