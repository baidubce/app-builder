
#!/bin/bash

# 设置 PYTHONPATH 为当前目录
export PYTHONPATH=${PYTHONPATH}:$(pwd)/../
export WORKDIR="$(pwd)/../appbuilder"


# 遍历指定工作目录及其子目录下的所有 readme.md 文件
find "$WORKDIR" -type f -iname "readme.md" | while read file; do
    # 对每个找到的 readme.md 文件执行操作

    dirpath=$(dirname "$file")
    basename=$(basename "$dirpath")

    output_file="source/rst/components/${basename}.rst"
    rst_file="rst/components/${basename}.rst"
    python3 markdown2rst.py --input_file $file --output_file ${output_file} --overwrite true

    # 收集输出文件路径
    output_files+=("${rst_file}")

    # 在这里添加对文件的其他处理
    # ...
done

# 用于收集输出文件路径的数组
output_files=()

# 遍历 source/rst/components/ 目录来构建 output_files 列表
cd source/
for file in rst/components/*.rst; do
    # 检查文件是否存在
    if [ -f "$file" ]; then
        output_files+=("$file")
    fi
done
cd ..

echo "output_files: ${output_files[@]}"

# 构建替换字符串
components_rst=""
for file in "${output_files[@]}"; do
    components_rst+="   ${file}\n"
done

# 使用模板文件创建新的 index.rst
cp index.rst.template source/index.rst

# 替换 index.rst 文件中的占位符
sed -i '' "s|{{components_rst}}|${components_rst}|g" source/index.rst

## 删除旧的 index.rst.template 文件
#rm -rf build
## 生成 html
#make html
