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
import logging
import unittest

from appbuilder.utils.logger_util import LoggerWithLoggerId,_setup_logging
from threading import current_thread 

# 创建一个logger类
class test_logger_level():
    def __init__(self):
        self.level='level'

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestUtilsLogger(unittest.TestCase):
    def test_logger_util_LoggerWithLoggerId(self):
        # test_get_logid
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        self.assertEqual(lwl.get_logid(),None)
        lwl.logid_dict[current_thread().ident]='ident'
        self.assertEqual(lwl.get_logid(),'ident')

        # test_process
        kwargs={
            'extra':{'logid':'test_logid'}
        }
        msg,kwargs=lwl.process(msg='test_msg',kwargs=kwargs)
        self.assertEqual(kwargs['extra']['logid'],lwl.logid_dict[current_thread().ident])
        msg,kwargs=lwl.process(msg='test_msg',kwargs={})
        self.assertEqual(kwargs['extra']['logid'],lwl.logid_dict[current_thread().ident])

        # test_level
        test_logger=test_logger_level()
        lwl.logger=test_logger
        self.assertEqual(lwl.level,'level')

    def test_setup_logging(self):
        # test_setup_logging
        os.environ["APPBUILDER_LOGFILE"] = "/tmp/appbuilder.log"
        _setup_logging()
        os.environ["APPBUILDER_LOGLEVEL"]="test" 
        with self.assertRaises(ValueError):
            _setup_logging()

    def test_set_filename_and_loglevel(self):
        # test_set_filename
        lwl=LoggerWithLoggerId(logger='test_logger',extra={'logid':'test_logid'},loglevel='INFO')
        lwl.setLoglevel("debug")
        lwl.setFilename("/tmp/appbuilder.log")
        with self.assertRaises(ValueError):
            lwl.setLoglevel("test")
if __name__ == '__main__':
    unittest.main()
