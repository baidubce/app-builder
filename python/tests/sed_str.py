# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 该文件的作用等同于以 sed -i 命令，对文件进行修改
# 接受三个输入，分别为文件名，替换原始字符串，替换目标字符串
# 会将文件中的原始字符串替换为目标字符串

import sys
import os
def sed_str(file, old_str, new_str):
    """
    使用sed命令替换文件中的字符串，并返回修改后的结果。

    Args:
        file (str): 需要进行字符串替换的文件路径。
        old_str (str): 需要被替换的原始字符串。
        new_str (str): 需要替换成的新字符串。

    Returns:
        int: 返回值为0表示操作成功，其他值表示失败。

    Raises:
        无。
    """
    with open(file, 'r') as f:
        lines = f.read()
    new_lines = lines.replace(
        old_str, new_str)
    with open(file, 'w') as f:
        f.write(new_lines)
        f.close()
    os.chmod(file, 0o755)
    print("sed success!")
    return 0    

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python sed_str.py file old_str new_str")
        exit(-1)
    file = sys.argv[1]
    old_str = sys.argv[2]
    new_str = sys.argv[3]
    sed_str(file, old_str, new_str)