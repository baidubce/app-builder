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
import uuid
import unittest
import subprocess
import importlib
import requests
import logging

import appbuilder
from appbuilder import AppBuilderTracer, AppbuilderInstrumentor
from appbuilder.utils.trace._function import _components_run_trace_with_sentry,_components_stream_run_trace_with_sentry

logging.basicConfig(level=logging.INFO)

class TestAppbuilderForSentryOff(unittest.TestCase):

    def test_sentry_inport_error(self):
        """
        测试sentry导入错误的情况
        
        Args:
            无
        
        Returns:
            无返回值，该函数主要用于测试
        
        Raises:
            ImportError: 当sentry-sdk库不存在时，会触发ImportError异常
        
        """
        # 配置测试环境
        try:
            subprocess.check_output(['python3','-m','pip', 'uninstall', 'sentry-sdk', '-y'])
        except Exception as e:
            print('pip uninstall sentry-sdk failed')
        os.environ['ENABLE_SENTRY_TRACE'] = 'true'
        os.environ['SENTRY_DSN'] = 'test'

        with self.assertRaises(ImportError):
            tracer = AppBuilderTracer()
            tracer.start_trace()

        with self.assertRaises(ImportError):
            arg = ()
            kwarg = {}
            _components_run_trace_with_sentry(func = 'func', args = arg, kwargs = kwarg)
        
        with self.assertRaises(ImportError):
            arg = ()
            kwarg = {}
            res = _components_stream_run_trace_with_sentry(func = 'func', args = arg, kwargs = kwarg)
            for r in res:
                pass


if __name__ == '__main__':
    unittest.main()
