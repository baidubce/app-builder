#!/bin/bash

mvn clean test jacoco:report jacoco:check 

python parse_jacoco.py

# 基准分支
base_branch="origin/master"
# 更新 PATH
export PATH="$HOME/.local/bin:$PATH"
# 安装 diff-cover，如果未安装
if ! command -v diff-cover &> /dev/null; then
    echo "diff-cover not found, installing..."
    pip install --user diff-cover
fi


# 检查是否生成了 jacoco.xml 文件
if [ -f target/site/jacoco/jacoco.xml ]; then
    echo "jacoco.xml found."
else
    echo "jacoco.xml not found."
    exit 1
fi

# 增量代码覆盖率检测
echo "增量代码覆盖率为："
git diff $base_branch --name-only -- '*.java' > diff_files.txt

if [ -s diff_files.txt ]; then
    if ! diff-cover target/site/jacoco/jacoco.xml --compare-branch=$base_branch --html-report coverage_diff.html; then
        echo "Failed to generate incremental coverage report."
        exit 1
    else
        echo "Incremental coverage report generated at coverage_diff.html"
    fi
else
    echo "No Java files changed relative to $base_branch. Incremental coverage not generated."
fi

# 清理
rm diff_files.txt