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
            console_show = True,
            loglevel='DEBUG',
            file_name='test.log',
            when='D',
            interval=0, # 测试interval<1时，自动更新为1
            max_bytes=None, # 测试not max_bytes or max_bytes <= 0时，自动更新为sys.maxsize
            total_size_limit=None, # 测试not total_size_limit or total_size_limit <= 0时，自动更新为sys.maxsize
            backup_count=None, # 测试not backup_count or backup_count <= 0时，自动更新为sys.maxsize
        )

    def test_set_log_config_raise_error(self):
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        with self.assertRaises(ValueError):    
            lwl.setLogConfig(
                console_show = True,
                loglevel='DEBUG',
                file_name='test.log',
                when='ERROR-WHEN',
                interval=0, # 测试interval<1时，自动更新为1
                max_bytes=None, # 测试not max_bytes or max_bytes <= 0时，自动更新为sys.maxsize
                total_size_limit=None, # 测试not total_size_limit or total_size_limit <= 0时，自动更新为sys.maxsize
                backup_count=None, # 测试not backup_count or backup_count <= 0时，自动更新为sys.maxsize
            )

    def test_rolling_with_time(self):
        logger = logging.getLogger('CustomLogger')
        logger.setLevel(logging.DEBUG)
        handler = SizeAndTimeRotatingFileHandler(
            filename ='test.log', 
            when='S', 
            interval=1, 
            max_bytes=1024*100*1024, 
            backup_count=10, 
            total_size_limit=1024*300*1024
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        for i in range(3):
            logger.info("This is a test log message.")
            time.sleep(1)

    def test_rolling_with_size(self):
        logger = logging.getLogger('CustomLogger')
        logger.setLevel(logging.DEBUG)
        handler = SizeAndTimeRotatingFileHandler(
            filename ='test.log', 
            when='S', 
            interval=10, 
            max_bytes=1*1024, 
            backup_count=2, 
            total_size_limit=1024*300*1024
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
            filename ='test.log', 
            when='S', 
            interval=100, 
            max_bytes=10*1024, 
            backup_count=10000, 
            total_size_limit=20*1024
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        for i in range(100):
            logger.info("This is a test log message."*100)
            time.sleep(0.001)

if __name__ == '__main__':
    unittest.main()