import json
import sys

def parse_test_report_json(log_file):
    passed_tests = []
    failed_tests = []
    skipped_tests = []
    current_test = ""

    try:
        with open(log_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
                    continue

                action = event.get('Action', '')
                if action == 'run':
                    current_test = event.get('Test', '')
                elif action == 'pass':
                    test_name = event.get('Test', '')
                    if test_name:
                        print(f"[PASS] {test_name}")
                        passed_tests.append(test_name)
                elif action == 'fail':
                    test_name = event.get('Test', '')
                    if test_name:
                        print(f"[FAIL] {test_name}")
                        failed_tests.append(test_name)
                        # 打印错误输出
                        output = event.get('Output', '').strip()
                        if output:
                            print(f"  错误信息: {output}")
                elif action == 'skip':
                    test_name = event.get('Test', '')
                    if test_name:
                        print(f"[SKIP] {test_name}")
                        skipped_tests.append(test_name)

        total_tests = len(passed_tests) + len(failed_tests) + len(skipped_tests)

        # 输出测试总结
        print("\n=== 测试总结 ===")
        print(f"总测试数: {total_tests}")
        print(f"成功: {len(passed_tests)}")
        print(f"失败: {len(failed_tests)}")
        print(f"跳过: {len(skipped_tests)}")

        # 打印详细信息
        if failed_tests:
            print("\n详细错误信息：")
            for test in failed_tests:
                print(f"[FAIL] {test}")

        if skipped_tests:
            print("\n跳过的测试：")
            for test in skipped_tests:
                print(f"[SKIP] {test}")

        if passed_tests:
            print("\n通过的测试：")
            for test in passed_tests:
                print(f"[PASS] {test}")

    except FileNotFoundError:
        print(f"错误: 文件 {log_file} 未找到。")
        sys.exit(1)
    except Exception as e:
        print(f"解析测试报告时发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 parse_test_report_json.py <测试日志文件>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    parse_test_report_json(log_file)