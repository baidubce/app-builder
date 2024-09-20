#!/bin/bash

# 启用错误检测和管道失败检测
set -o pipefail

# 初始化错误标志
error_flag=0

# 用于存储错误消息
error_messages=()

# 检查并添加必要的路径
export PATH="$HOME/.local/bin:$PATH"
export PATH="$PATH:$(go env GOPATH)/bin"


pip install diff-cover || { error_flag=1; error_messages+=("Failed to install diff-cover."); }
# 检查 diff-cover 是否已安装
if ! command -v diff-cover &> /dev/null; then
    error_flag=1
    error_messages+=("diff-cover installation failed. Please check your Python and pip installation.")
fi

echo "diff-cover is installed."

# 安装 gocov 和 gocov-xml，如果未安装
if ! command -v gocov &> /dev/null; then
    echo "gocov not found, installing..."
    go install github.com/axw/gocov/gocov@latest || { error_flag=1; error_messages+=("Failed to install gocov."); }
fi

if ! command -v gocov-xml &> /dev/null; then
    echo "gocov-xml not found, installing..."
    go install github.com/AlekSi/gocov-xml@latest || { error_flag=1; error_messages+=("Failed to install gocov-xml."); }
fi

# 添加 GOPATH/bin 到 PATH，以便找到 gocov 和 gocov-xml
export PATH="$PATH:$(go env GOPATH)/bin"

# 验证 gocov 和 gocov-xml 是否安装成功
if ! command -v gocov &> /dev/null; then
    error_flag=1
    error_messages+=("gocov installation failed.")
fi

if ! command -v gocov-xml &> /dev/null; then
    error_flag=1
    error_messages+=("gocov-xml installation failed.")
fi

echo "gocov and gocov-xml are installed."

# 初始化计数器
total_tests=0
skipped_tests=0
failed_tests=0
passed_tests=0

# 用于存储跳过和失败的测试函数
skipped_list=()
failed_list=()

# 创建临时文件用于存储测试输出和覆盖率数据
test_output=$(mktemp)
coverage_file=$(mktemp)

# 确保临时文件创建成功
if [ ! -f "$test_output" ] || [ ! -f "$coverage_file" ]; then
    echo "无法创建临时文件。"
    exit 1
fi

# 运行所有包的测试并保存输出
echo "运行所有包的测试并生成覆盖率报告..."
set +e
go test ./... -coverprofile="$coverage_file" -covermode=atomic -v > "$test_output" 2>&1
GO_TEST_EXIT_CODE=$?
set -e
echo "Go test 退出代码: $GO_TEST_EXIT_CODE"

# 检查覆盖率文件是否生成且非空
if [ ! -s "$coverage_file" ]; then
    echo "覆盖率文件未生成或为空。"
    error_flag=1
    error_messages+=("Coverage profile not generated or empty.")
fi

# 解析测试结果
current_test=""
while IFS= read -r line; do
    if [[ "$line" == "=== RUN"* ]]; then
        # 提取测试函数名称
        test_name=$(echo "$line" | awk '{print $3}')
        # 提取包路径
        pkg=$(echo "$line" | awk '{print $2}' | sed 's/(//;s/)//')
        current_test="$pkg.$test_name"
    elif [[ "$line" == "--- PASS:"* ]]; then
        echo "[OK] $current_test"
        passed_tests=$((passed_tests + 1))
        passed_list+=("$current_test")
    elif [[ "$line" == "--- FAIL:"* ]]; then
        echo "[FAIL] $current_test"
        failed_tests=$((failed_tests + 1))
        failed_list+=("$current_test")
    elif [[ "$line" == "--- SKIP:"* ]]; then
        echo "[SKIP] $current_test"
        skipped_tests=$((skipped_tests + 1))
        skipped_list+=("$current_test")
    fi
done < "$test_output"

# 计算总测试数
total_tests=$((passed_tests + failed_tests + skipped_tests))

# 输出测试总结
echo ""
echo "=== 测试总结 ==="
echo "总测试数: $total_tests"
echo "成功: $passed_tests"
echo "失败: $failed_tests"
echo "跳过: $skipped_tests"

# 检查错误标志，如果有错误则输出错误消息并退出
if [ $error_flag -ne 0 ]; then
    echo "在过程中检测到以下错误："
    for msg in "${error_messages[@]}"; do
        echo "- $msg"
    done
    exit 1
fi

# 打印测试失败时的详细日志
if [ $GO_TEST_EXIT_CODE -ne 0 ]; then
    echo "测试运行过程中失败，错误代码: $GO_TEST_EXIT_CODE"
    echo "请查看详细的测试日志："
    echo "----------------------------------------"
    cat "$test_output"  # 打印测试的输出日志
    echo "----------------------------------------"
    exit 1
fi

# 输出覆盖率摘要
echo "--------------------------"
echo "全量代码覆盖率为："
go tool cover -func=$coverage_file

# 将覆盖率数据转换为 XML 格式
echo "Converting coverage data to XML format..."
if ! gocov convert $coverage_file | gocov-xml > coverage.xml; then
    error_flag=1
    error_messages+=("Failed to convert coverage data to XML format.")
fi

# 检查 coverage.xml 是否非空
if [ ! -s coverage.xml ]; then
    error_flag=1
    error_messages+=("Coverage XML file is empty or invalid.")
fi

# 生成包含所有文件的差异文件
echo "Generating full diff..."
if ! git diff $(git hash-object -t tree /dev/null) HEAD > full_diff.patch; then
    error_flag=1
    error_messages+=("Failed to generate full diff.")
fi

# 使用 diff-cover 生成全量覆盖率报告
echo "Generating full coverage report..."
if ! diff-cover coverage.xml --diff-file full_diff.patch --html-report coverage_full.html; then
    error_flag=1
    error_messages+=("Failed to generate full coverage report.")
else
    echo "Full coverage report generated at coverage_full.html"
fi

# 计算增量代码的单测覆盖率
base_branch="upstream/master"

# 生成增量覆盖率报告
echo "--------------------------"
echo "增量代码覆盖率为："
git diff $base_branch --name-only -- '*.go' > diff_files.txt

# 检查是否有修改的 go 文件
if [ -s diff_files.txt ]; then
    if ! diff-cover coverage.xml --compare-branch=$base_branch --html-report coverage_diff.html; then
        error_flag=1
        error_messages+=("Failed to generate incremental coverage report.")
    else
        echo "Incremental coverage report generated at coverage_diff.html"
    fi
else
    echo "No Go files changed relative to $base_branch. Incremental coverage not generated."
fi

# 清理
rm diff_files.txt
rm full_diff.patch
# 清理临时文件
rm "$test_output"
rm "$coverage_file"

# 检查错误标志，如果有错误则输出错误消息并退出
if [ $error_flag -ne 0 ]; then
    echo "Errors were detected during the process:"
    for msg in "${error_messages[@]}"; do
        echo "- $msg"
    done
    exit 1
fi