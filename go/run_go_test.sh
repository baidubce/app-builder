#!/bin/bash

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
            echo "Running tests in $testfile (package: $pkg)" > $temp_file
            echo "Running $func in package $pkg" >> $temp_file
            go test $pkg -run ^$func$ >> $temp_file 2>&1
            # 打印临时文件的内容
            cat $temp_file
            # 删除临时文件
            rm $temp_file
        ) &
    done
done

# 等待所有后台进程完成
wait