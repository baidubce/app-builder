import os

def find_readme_files(base_path):
    readme_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower() == "readme.md":
                readme_files.append(os.path.join(root, file))
    return readme_files

def extract_first_line(readme_path):
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            if first_line.startswith('#'):
                first_line = first_line[1:].strip()
            return first_line
    except Exception as e:
        print(f"Error reading {readme_path}: {str(e)}")
        return None

def update_mkdocs_yml(results, mkdocs_path='../../../mkdocs.yml'):
    try:
        with open(mkdocs_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 查找 "    - 组件:" 行的索引
        start_index = -1
        end_index = -1
        for i, line in enumerate(lines):
            if line.strip() == '- 组件:':
                start_index = i
            elif line.strip() == '- 监控:':
                end_index = i
                break
        
        if start_index == -1 or end_index == -1:
            print("未找到 '- 组件:' 或 '- 监控:' 行")
            return
        
        # 删除两标记之间的内容
        del lines[start_index + 1:end_index]

        # 在找到的行后面插入新的结果
        for result in reversed(results):
            lines.insert(start_index + 1, f"      - {result}\n")

        # 写回文件
        with open(mkdocs_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        print("mkdocs.yml 更新成功")
    except Exception as e:
        print(f"Error updating {mkdocs_path}: {str(e)}")

def main():
    base_path = '../../BasisModule/Components'  # 当前目录
    readme_files = find_readme_files(base_path)
    results = []

    for readme_path in readme_files:
        first_line = extract_first_line(readme_path)
        if first_line:
            relative_path = os.path.relpath(readme_path, start=base_path)
            result = f"{first_line}: BasisModule/Components/{relative_path.replace(os.sep, '/')}"
            results.append(result)

    # 更新 mkdocs.yml 文件
    update_mkdocs_yml(results)

if __name__ == "__main__":
    main()