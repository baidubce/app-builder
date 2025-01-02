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
import time
import logging
import unittest


from appbuilder import SizeAndTimeRotatingFileHandler
from appbuilder.utils.logger_util import LoggerWithLoggerId

class TestLogSetLogConfig(unittest.TestCase):
    def test_set_log_config(self):
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        lwl.setLogConfig(
            console_output = True,
            loglevel='DEBUG',
            file_name='test.log',
            rotate_frequency='D',
            rotate_interval=0, # 测试rotate_interval<1时，自动更新为1
            max_file_size=None, # 测试not max_file_size or max_file_size <= 0时，自动更新为sys.maxsize
            total_log_size=None, # 测试not total_log_size or total_log_size <= 0时，自动更新为sys.maxsize
            max_log_files=None, # 测试not max_log_files or max_log_files <= 0时，自动更新为sys.maxsize
        )

    def test_set_log_config_log_path(self):
        os.environ["APPBUILDER_LOGPATH"] = "/tmp"
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        lwl.setLogConfig(
            console_output = True,
            loglevel='DEBUG',
            log_path='/tmp',
            file_name='test.log',
            rotate_frequency='D',
            rotate_interval=0, # 测试rotate_interval<1时，自动更新为1
            max_file_size=None, # 测试not max_file_size or max_file_size <= 0时，自动更新为sys.maxsize
            total_log_size=None, # 测试not total_log_size or total_log_size <= 0时，自动更新为sys.maxsize
            max_log_files=None, # 测试not max_log_files or max_log_files <= 0时，自动更新为sys.maxsize
        )

    def test_set_log_config_raise_error(self):
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        with self.assertRaises(ValueError):    
            lwl.setLogConfig(
                console_output = True,
                loglevel='DEBUG',
                file_name='test.log',
                rotate_frequency='ERROR-FREQUENCY',
                rotate_interval=0, # 测试rotate_interval<1时，自动更新为1
                max_file_size=None, # 测试not max_file_size or max_file_size <= 0时，自动更新为sys.maxsize
                total_log_size=None, # 测试not total_log_size or total_log_size <= 0时，自动更新为sys.maxsize
                max_log_files=None, # 测试not max_log_files or max_log_files <= 0时，自动更新为sys.maxsize
            )

        with self.assertRaises(ValueError):    
            lwl.setLogConfig(
                console_output = True,
                loglevel='ERROR-LEVEL',
                file_name='test.log',
                rotate_frequency='D',
                rotate_interval=0, # 测试rotate_interval<1时，自动更新为1
                max_file_size=0, # 测试not max_file_size or max_file_size <= 0时，自动更新为sys.maxsize
                total_log_size=None, # 测试not total_log_size or total_log_size <= 0时，自动更新为sys.maxsize
                max_log_files=None, # 测试not max_log_files or max_log_files <= 0时，自动更新为sys.maxsize
            )

    def test_rolling_with_time(self):
        time_msgs = ['S', 'M', 'H', 'D', 'MIDNIGHT']
        for time_msg in time_msgs:
            logger = logging.getLogger('CustomLogger')
            logger.setLevel(logging.DEBUG)
            handler = SizeAndTimeRotatingFileHandler(
                file_name ='test.log', 
                rotate_frequency=time_msg, 
                rotate_interval=1, 
                max_file_size=1024*100*1024, 
                max_log_files=10, 
                total_log_size=1024*300*1024
            )
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            for _ in range(2):
                logger.info("This is a test log message.")
                time.sleep(0.1)

    def test_rolling_with_size(self):
        logger = logging.getLogger('CustomLogger')
        logger.setLevel(logging.DEBUG)
        handler = SizeAndTimeRotatingFileHandler(
            file_name ='test.log', 
            rotate_frequency='S', 
            rotate_interval=10, 
            max_file_size=1*1024, 
            max_log_files=2, 
            total_log_size=1024*300*1024
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        for i in range(100):
            logger.info("This is a test log message."*100)
            time.sleep(0.001)

    def test_rolling_to_total_max_size(self):
        logger = logging.getLogger('CustomLogger')
        logger.setLevel(logging.DEBUG)
        handler = SizeAndTimeRotatingFileHandler(
            file_name ='test.log', 
            rotate_frequency='S', 
            rotate_interval=100, 
            max_file_size=10*1024, 
            max_log_files=10000, 
            total_log_size=20*1024
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        for _ in range(100):
            logger.info("This is a test log message."*100)
            time.sleep(0.001)

if __name__ == '__main__':
    unittest.main()
