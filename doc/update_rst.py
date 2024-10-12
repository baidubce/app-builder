import os

def process_rst_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        if 'base' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        elif 'model' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        elif 'appbuilder.core.utils' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        elif 'data_class' in lines[i] and 'appbuilder.core' in lines[i]:
            i += min(8, len(lines) - i)
        else:
            new_lines.append(lines[i])
            i += 1

    # Write the modified content back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def main():
    # Traverse the current directory for all .rst files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.rst'):
                filepath = os.path.join(root, file)
                print(f'Processing {filepath}')
                process_rst_file(filepath)

if __name__ == "__main__":
    main()