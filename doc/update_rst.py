import os

def process_rst_file(filepath):
    """
    处理rst文件，移除包含特定文本的行。
    
    Args:
        filepath (str): rst文件的路径。
    
    Returns:
        None
    
    说明:
        打开rst文件，读取文件内容到lines列表中。
        遍历lines列表，根据条件移除包含特定文本的行，
        这些特定文本包括'base'且'appbuilder.core'、'model'且'appbuilder.core'、
        'appbuilder.core.utils'且'appbuilder.core'、'data_class'且'appbuilder.core'。
        每次移除满足条件的行时，最多连续移除8行，防止移除过多内容。
        将修改后的内容写回原文件。
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        if 'base' in lines[i] and 'appbuilder.core' in lines[i] and 'knowledge_base' not in lines[i]:
            i += min(8, len(lines) - i)
        elif 'model' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        elif 'appbuilder.core.utils' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        elif 'data_class' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        elif 'Module contents' in lines[i]:
            i += min(8, len(lines) - i)
        else:
            new_lines.append(lines[i])
            i += 1

    # Write the modified content back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def main():
    """
    遍历当前目录下的所有.rst文件
    
    Args:
        无参数
    
    Returns:
        无返回值
    
    """
    # Traverse the current directory for all .rst files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.rst'):
                filepath = os.path.join(root, file)
                print(f'Processing {filepath}')
                process_rst_file(filepath)

if __name__ == "__main__":
    main()