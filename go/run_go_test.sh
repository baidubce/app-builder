#!/bin/bash

# 检查并添加 diff-cover 的路径
export PATH="$HOME/Library/Python/3.9/bin:$PATH"

# 检查 diff-cover 是否可用
if ! command -v diff-cover &> /dev/null; then
    echo "diff-cover could not be found. Installing..."
    # 使用 pip 安装 diff-cover
    python3 -m ensurepip --upgrade
    python3 -m pip install --user diff-cover
    # 检查安装是否成功
    if ! command -v diff-cover &> /dev/null; then
        echo "Installation of diff-cover failed. Please check your Python and pip installation."
        exit 1
    fi
fi

echo "diff-cover is installed."

# 初始化计数器
total_tests=0
skipped_tests=0
failed_tests=0
passed_tests=0

# 用于存储跳过的测试函数
skipped_list=()

# 创建一个覆盖率输出文件
coverage_file="coverage.out"
echo "mode: set" > $coverage_file

# 用于存储后台任务的 PIDs
pids=()

# 遍历当前目录及子目录中的所有测试文件
for testfile in $(find . -name '*_test.go'); do
    # 获取测试文件的包路径
    pkg=$(dirname "$testfile")

    # 使用 go test -list 来列出文件中的测试函数
    test_funcs=$(go test -list . $pkg | grep -E '^Test')

    # 遍历找到的测试函数并并发运行它们
    for func in $test_funcs; do
        total_tests=$((total_tests + 1))
        (
            # 创建一个临时文件
            temp_file=$(mktemp)
            coverage_temp_file=$(mktemp)

            echo "Running tests in $testfile (package: $pkg)" > $temp_file
            echo "Running $func in package $pkg" >> $temp_file
            go test -coverprofile=$coverage_temp_file -covermode=atomic $pkg -run ^$func$ >> $temp_file 2>&1
            # 打印临时文件的内容
            cat $temp_file

            # 检查是否跳过了测试
            if grep -q -- "--- SKIP" $temp_file; then
                skipped_tests=$((skipped_tests + 1))
                skipped_list+=("$func in $pkg")
            elif grep -q -- "--- FAIL" $temp_file; then
                failed_tests=$((failed_tests + 1))
            else
                passed_tests=$((passed_tests + 1))
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

# 输出统计结果
echo "Total tests: $total_tests"
echo "Passed tests: $passed_tests"
echo "Failed tests: $failed_tests"
echo "Skipped tests: $skipped_tests"
if [ $skipped_tests -gt 0 ]; then
    echo "Skipped test functions:"
    for skipped in "${skipped_list[@]}"; do
        echo "  $skipped"
    done
fi

# 输出覆盖率摘要
echo "Overall coverage summary:"
go tool cover -func=$coverage_file

# 生成 HTML 报告
go tool cover -html=$coverage_file -o coverage.html
echo "Coverage report generated at coverage.html"

# 计算增量代码的单测覆盖率
# 基准分支为 master，如果你的基准分支不是 master，请将下面的 master 替换为你的基准分支名称
base_branch="upstream/master"

# 生成增量覆盖率报告
echo "Calculating incremental coverage..."
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