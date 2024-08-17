# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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

import random
import string
import os

class Utils(object):
    """
    utils 方法父类
    """
    @staticmethod
    def get_random_string(str_len, prefix=None):
        """
        生成随机字符串，可指定前缀
        """
        gen_name = ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
        )
        if prefix:
            name = str(prefix) + gen_name
        else:
            name = gen_name
        return name

    @staticmethod
    def get_data_file(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_file_path = os.path.join(current_dir, "data", filename)
        return full_file_path

