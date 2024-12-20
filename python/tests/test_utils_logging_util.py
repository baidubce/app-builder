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
import os

from appbuilder.utils.logger_util import LoggerWithLoggerId, LOGGING_CONFIG, TIME_HANDLERS_FILE


# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestTestUtilsLoggingUtil(unittest.TestCase):
    def setUp(self):
        self.logger = LoggerWithLoggerId(LOGGING_CONFIG["loggers"]["appbuilder"], {}, 'DEBUG')

    def test_set_auto_logid(self):
        self.logger.set_auto_logid()
    
    def test_set_logid(self):
        self.logger.set_logid('test')
        
    def test_get_logid(self):
        self.logger.set_auto_logid()
    
    def test_set_log_config(self):
        self.logger.setLogConfig(
            console_show=False,
            update_interval = -1,
            update_time='M',
            backup_count=-1
        )

        self.logger.setLogConfig(
            log_file='test.log',
            console_show=False,
            update_interval = -1,
            update_time='M',
            backup_count=-1
        )

        os.environ["APPBUILDER_LOGFILE"] = 'test.log'
        self.logger.setLogConfig(
            console_show=False,
            update_interval = -1,
            update_time='M',
            backup_count=-1
        )
        del os.environ['APPBUILDER_LOGFILE']

        with self.assertRaises(ValueError):
            self.logger.setLogConfig(
                console_show=False,
                update_interval = -1,
                update_time='Test',
                backup_count=-1
            )
    
    def test_process(self):
        msg,kwargs=self.logger.process(msg='test',kwargs={})
        msg,kwargs=self.logger.process(msg='test',kwargs={'extra':{'logid':'test'}})
        


if __name__ == '__main__':
    unittest.main()
        
        
        