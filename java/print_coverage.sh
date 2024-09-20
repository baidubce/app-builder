#!/bin/bash

# 设置脚本退出时错误码
set -e

# 运行 Maven 测试并生成 JaCoCo 报告，捕获输出
echo "运行 Maven 测试并生成 JaCoCo 报告..."
if mvn clean test jacoco:report jacoco:check > mvn_output.log 2>&1; then
    echo "Maven 测试成功。"
else
    echo "Maven 测试失败。查看详细错误日志："
    cat mvn_output.log
    exit 1  # 直接退出
fi

# 更新 PATH
export PATH="$HOME/.local/bin:$PATH"

# 运行 Python 脚本解析测试和覆盖率报告
python parse_tests_and_coverage.py
