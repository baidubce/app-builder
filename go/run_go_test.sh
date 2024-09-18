#!/bin/bash

# Check and add necessary paths
export PATH="$HOME/.local/bin:$PATH"
export PATH="$PATH:$(go env GOPATH)/bin"

# Set up a Python virtual environment to avoid conflicts with system Python
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install diff-cover in the virtual environment
echo "Installing diff-cover in the virtual environment..."
pip install diff-cover

# Check if diff-cover is installed
if ! command -v diff-cover &> /dev/null; then
    echo "diff-cover installation failed. Please check your Python and pip installation."
    exit 1
fi

echo "diff-cover is installed."

# 初始化计数器
total_tests=0
skipped_tests=0
failed_tests=0
passed_tests=0

# 用于存储跳过和失败的测试函数
skipped_list=()
failed_list=()

# 创建一个覆盖率输出文件
coverage_file="coverage.out"
echo "mode: set" > $coverage_file

# 用于存储后台任务的 PIDs
pids=()

# 用于存储测试结果的文件
test_results_log=$(mktemp)

# 遍历当前目录及子目录中的所有测试文件
for testfile in $(find . -name '*_test.go'); do
    # 获取测试文件的包路径
    pkg=$(dirname "$testfile")

    # 使用 go test -list 来列出文件中的测试函数
    test_funcs=$(go test -list . $pkg | grep -E '^Test')

    # 遍历找到的测试函数并并发运行它们
    for func in $test_funcs; do
        (
            # 创建一个临时文件
            temp_file=$(mktemp)
            coverage_temp_file=$(mktemp)

            echo "Running tests in $testfile (package: $pkg)" > $temp_file
            echo "Running $func in package $pkg" >> $temp_file
            go test -coverprofile=$coverage_temp_file -covermode=atomic $pkg -run ^$func$ >> $temp_file 2>&1
            # 打印临时文件的内容
            cat $temp_file

            # 分析测试结果
            if grep -q -- "--- SKIP" $temp_file; then
                echo "$func SKIP" >> "$test_results_log"
            elif grep -q -- "--- FAIL" $temp_file; then
                echo "$func FAIL" >> "$test_results_log"
                failed_list+=("$func")
            else
                echo "$func PASS" >> "$test_results_log"
                # 合并覆盖率报告
                tail -n +2 $coverage_temp_file >> $coverage_file
            fi

            # 删除临时文件
            rm $temp_file
            rm $coverage_temp_file
        ) &
        # 记录后台任务的 PID
        pids+=($!)
    done
done

# 等待所有后台任务完成
for pid in "${pids[@]}"; do
    wait $pid
done

# 读取测试结果
while IFS= read -r result; do
    case $result in
        *"PASS")
            passed_tests=$((passed_tests + 1))
            ;;
        *"FAIL")
            failed_tests=$((failed_tests + 1))
            failed_list+=("${result%% FAIL}")
            ;;
        *"SKIP")
            skipped_tests=$((skipped_tests + 1))
            skipped_list+=("${result%% SKIP}")
            ;;
    esac
done < "$test_results_log"

total_tests=$((passed_tests + failed_tests + skipped_tests))

# 输出统计结果
echo "Total tests: $total_tests"
echo "Passed tests: $passed_tests"
echo "Failed tests: $failed_tests"
if [ $failed_tests -gt 0 ]; then
    echo "Failed test functions:"
    for failed in "${failed_list[@]}"; do
        echo "  $failed"
    done
fi
echo "Skipped tests: $skipped_tests"
if [ $skipped_tests -gt 0 ]; then
    echo "Skipped test functions:"
    for skipped in "${skipped_list[@]}"; do
        echo "  $skipped"
    done
fi

# 输出覆盖率摘要
echo "--------------------------"
echo "全量代码覆盖率为："
go tool cover -func=$coverage_file

# 将覆盖率数据转换为 XML 格式
echo "Converting coverage data to XML format..."
gocov convert coverage.out | gocov-xml > coverage.xml

# 生成包含所有文件的差异文件
echo "Generating full diff..."
git diff $(git hash-object -t tree /dev/null) HEAD > full_diff.patch

# 使用 diff-cover 生成全量覆盖率报告
echo "Generating full coverage report..."
diff-cover coverage.xml --diff-file full_diff.patch --html-report coverage_full.html

echo "Full coverage report generated at coverage_full.html"

# 计算增量代码的单测覆盖率
# 基准分支为 master，如果你的基准分支不是 master，请将下面的 master 替换为你的基准分支名称
base_branch="upstream/master"

# 生成增量覆盖率报告
echo "--------------------------"
echo "增量代码覆盖率为："
git diff $base_branch --name-only -- '*.go' > diff_files.txt

# 检查是否有修改的 go 文件
if [ -s diff_files.txt ]; then
    # 转换为 LCOV 格式
    gocov convert coverage.out | gocov-xml > coverage.xml
    # 生成增量覆盖率报告
    diff-cover coverage.xml --compare-branch=$base_branch --html-report coverage_diff.html
    echo "Incremental coverage report generated at coverage_diff.html"
else
    echo "No Go files changed relative to $base_branch. Incremental coverage not generated."
fi

# 清理
rm diff_files.txt
rm "$test_results_log"