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

import os
import unittest
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestGetQianfanModelList(unittest.TestCase):

    def test_run(self):
        """
        正常用例
        """
        secret_key = os.environ["APPBUILDER_TOKEN"]
        api_type_filter = ["chat", "completions", "embeddings", "text2image"]
        is_available = True

        models = appbuilder.get_model_list(
            secret_key=secret_key,
            api_type_filter=api_type_filter,
            is_available=is_available
        )

        self.assertIn("ERNIE", str(models))
        self.assertGreater(len(models), 0, "Model list should not be empty")

if __name__ == '__main__':
    unittest.main()
