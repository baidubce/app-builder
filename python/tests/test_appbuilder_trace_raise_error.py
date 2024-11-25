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

from opentelemetry import trace
from appbuilder import AppbuilderTraceException
from appbuilder.utils.trace._function import _input,_client_trace_generator,_assistant_stream_run_with_handler_output


class TestAppbuilderTraceRaiseError(unittest.TestCase):
    def setUp(self):
        tracer_provider = trace.get_tracer_provider()
        tracer = trace.get_tracer(
                instrumenting_module_name=__name__,
                tracer_provider=tracer_provider,
            )

        self.tracer = tracer

    def test_appbuilder_trace_raise_error_input(self):
        """
        测试AppBuilder跟踪时输入错误时抛出AppbuilderTraceException异常
        
        Args:
            无参数
        
        Returns:
            无返回值
        
        Raises:
            AppbuilderTraceException: 如果输入不满足要求，抛出AppbuilderTraceException异常
        
        """ 
        def sample_function(x):
            return x * 2
        with self.assertRaises(AppbuilderTraceException):
            _input([sample_function], 2, 3)

    def test_appbuilder_trace_raise_error_client_trace_generator(self):
        generator = _client_trace_generator('generator', self.tracer, 'parent_context')
        with self.assertRaises(AppbuilderTraceException):
            next(generator)

    def test_appbuilder_trace_raise_error_assistant_stream_run_with_handler_output(self):
        generator = _assistant_stream_run_with_handler_output(None, self.tracer, None)
        with self.assertRaises(AppbuilderTraceException):
            next(generator)
            

if __name__ == '__main__':
    unittest.main()
       