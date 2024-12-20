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
import unittest
import json
import os
import copy

from appbuilder.utils.logger_util import LoggerWithLoggerId, LOGGING_CONFIG


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestTestUtilsLoggingUtil(unittest.TestCase):
    def setUp(self):
        self.original_logging_config = copy.deepcopy(LOGGING_CONFIG)
        print(json.dumps(LOGGING_CONFIG, indent=4, ensure_ascii=False))
        self.logger = LoggerWithLoggerId(self.original_logging_config["loggers"]["appbuilder"], {}, 'DEBUG')

    def tearDown(self):
        global LOGGING_CONFIG
        LOGGING_CONFIG = copy.deepcopy(self.original_logging_config)

    
    def test_set_log_config_01(self):
        self.logger.setLogConfig(
            console_show=False,
            update_interval = -1,
            update_time='M',
            backup_count=-1
        )

    def test_set_log_config_02(self):
        self.logger.setLogConfig(
            filename='test.log',
            console_show=False,
            update_interval = -1,
            update_time='M',
            backup_count=-1
        )

    def test_set_log_config_03(self):
        with self.assertRaises(ValueError):
            self.logger.setLogConfig(
                console_show=False,
                update_interval = -1,
                update_time='Test',
                backup_count=-1
            )
        

if __name__ == '__main__':
    unittest.main()
        