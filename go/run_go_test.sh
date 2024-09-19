#!/bin/bash

# 启用错误检测和管道失败检测
set -o pipefail
set -e

# 初始化错误标志
error_flag=0

# 用于存储错误消息
error_messages=()

# 添加必要的路径
export PATH="$HOME/.local/bin:$PATH"
export PATH="$PATH:$(go env GOPATH)/bin"

# 升级 pip 到最新版本
echo "升级 pip 到最新版本..."
pip install --upgrade pip || { error_flag=1; error_messages+=("Failed to upgrade pip."); }

# 安装 diff-cover
echo "安装 diff-cover..."
pip install diff-cover || { error_flag=1; error_messages+=("Failed to install diff-cover."); }

# 检查 diff-cover 是否已安装
if ! command -v diff-cover &> /dev/null; then
    error_flag=1
    error_messages+=("diff-cover 安装失败。请检查您的 Python 和 pip 安装。")
fi

echo "diff-cover 已安装。"

# 安装 gocov 和 gocov-xml，如果未安装
install_go_tool() {
    local tool=$1
    local repo=$2
    echo "检查并安装 $tool..."
    if ! command -v "$tool" &> /dev/null; then
        go install "$repo@latest" || { error_flag=1; error_messages+=("安装 $tool 失败。"); }
    fi
}

install_go_tool "gocov" "github.com/axw/gocov/gocov"
install_go_tool "gocov-xml" "github.com/AlekSi/gocov-xml"

# 验证 gocov 和 gocov-xml 是否安装成功
if ! command -v gocov &> /dev/null; then
    error_flag=1
    error_messages+=("gocov 安装失败。")
fi

if ! command -v gocov-xml &> /dev/null; then
    error_flag=1
    error_messages+=("gocov-xml 安装失败。")
fi

echo "gocov 和 gocov-xml 已安装。"

# 检查是否有错误
if [ $error_flag -ne 0 ]; then
    echo "安装过程中发生错误："
    for msg in "${error_messages[@]}"; do
        echo "- $msg"
    done
    exit 1
fi

# 创建一个日志文件用于存储测试结果
test_results_log=$(mktemp)
coverage_temp_file=$(mktemp)

# 运行所有包的测试并保存 JSON 输出和覆盖率数据
echo "运行所有包的测试并生成 JSON 数据..."
go test ./... -json -coverprofile="$coverage_temp_file" -covermode=atomic > "$test_results_log" 2>&1
GO_TEST_EXIT_CODE=$?
echo "Go test 退出码: $GO_TEST_EXIT_CODE"

# 检查覆盖率文件是否生成且非空
if [ ! -s "$coverage_temp_file" ]; then
    echo "覆盖率文件未生成或为空。"
    error_flag=1
    error_messages+=("覆盖率文件未生成或为空。")
fi

# 使用 Python 脚本解析 JSON 测试结果
echo "使用Python解析测试结果..."
python3 parse_test_report_json.py "$test_results_log"

# 检查 Python 脚本是否执行成功
if [ $? -ne 0 ]; then
    error_flag=1
    error_messages+=("测试结果解析失败。")
fi

# 打印覆盖率摘要（如果覆盖率文件有效）
if [ -s "$coverage_temp_file" ]; then
    echo "--------------------------"
    echo "全量代码覆盖率为："
    go tool cover -func="$coverage_temp_file" | grep total
fi

# 将覆盖率数据转换为 XML 格式
echo "转换覆盖率数据为 XML 格式..."
if ! gocov convert "$coverage_temp_file" | gocov-xml > coverage.xml; then
    error_flag=1
    error_messages+=("将覆盖率数据转换为 XML 格式失败。")
fi

# 检查 coverage.xml 是否非空
if [ ! -s coverage.xml ]; then
    error_flag=1
    error_messages+=("覆盖率 XML 文件为空或无效。")
fi

# 生成全量代码差异文件
echo "生成全量代码差异文件..."
if ! git diff $(git hash-object -t tree /dev/null) HEAD > full_diff.patch; then
    error_flag=1
    error_messages+=("生成全量差异文件失败。")
fi

# 使用 diff-cover 生成全量覆盖率报告
echo "生成全量覆盖率报告..."
if ! diff-cover coverage.xml --diff-file full_diff.patch --html-report coverage_full.html; then
    error_flag=1
    error_messages+=("生成全量覆盖率报告失败。")
else
    echo "全量覆盖率报告已生成在 coverage_full.html"
fi

# 设置基准分支
base_branch="upstream/master"

# 生成增量代码覆盖率报告
echo "--------------------------"
echo "生成增量代码覆盖率报告..."
git diff "$base_branch" --name-only -- '*.go' > diff_files.txt

# 检查是否有修改的 Go 文件
if [ -s diff_files.txt ]; then
    if ! diff-cover coverage.xml --compare-branch="$base_branch" --html-report coverage_diff.html; then
        error_flag=1
        error_messages+=("生成增量覆盖率报告失败。")
    else
        echo "增量覆盖率报告已生成在 coverage_diff.html"
    fi
else
    echo "相对于 $base_branch 没有修改的 Go 文件。未生成增量覆盖率报告。"
fi

# 清理临时文件
rm "$test_results_log"
rm "$coverage_temp_file"
rm full_diff.patch
rm diff_files.txt

# 检查错误标志，如果有错误则输出错误消息并退出
if [ $error_flag -ne 0 ]; then
    echo "过程中检测到错误："
    for msg in "${error_messages[@]}"; do
        echo "- $msg"
    done
    exit 1
fi

echo "脚本执行成功。"
exit 0