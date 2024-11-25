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

from appbuilder.utils.trace.tracer_wrapper import (
session_post, 
client_run_trace, 
client_tool_trace,
assistent_tool_trace,
assistant_run_trace,
assistent_stream_run_trace,
assistent_stream_run_with_handler_trace,
components_run_trace,
components_run_stream_trace, 
list_trace, 
)

class TestException(Exception):
    def __init__(self):
        pass

@session_post
def mock_post_01():
    raise Exception("mock exception")

@session_post
def mock_post_02():
    raise TestException()

@client_run_trace
def mock_client_run_trace_01():
    raise Exception("mock exception")

@client_run_trace
def mock_client_run_trace_02():
    raise TestException()

@client_tool_trace
def mock_client_tool_trace_01():
    raise Exception("mock exception")

@client_tool_trace
def mock_client_tool_trace_02():
    raise TestException()

@assistent_tool_trace
def mock_assistent_tool_trace_01():
    raise Exception("mock exception")

@assistent_tool_trace
def mock_assistent_tool_trace_02():
    raise TestException()

@assistant_run_trace
def mock_assistant_run_trace_01():
    raise Exception("mock exception")

@assistant_run_trace
def mock_assistant_run_trace_02():
    raise TestException()

@assistent_stream_run_trace
def mock_assistent_stream_run_trace_01():
    raise Exception("mock exception")

@assistent_stream_run_trace
def mock_assistent_stream_run_trace_02():
    raise TestException()

@assistent_stream_run_with_handler_trace
def mock_assistent_stream_run_with_handler_trace_01():
    raise Exception("mock exception")

@assistent_stream_run_with_handler_trace
def mock_assistent_stream_run_with_handler_trace_02():
    raise TestException()

@components_run_trace
def mock_components_run_trace_01():
    raise Exception("mock exception")

@components_run_trace
def mock_components_run_trace_02():
    raise TestException()

@components_run_stream_trace
def mock_components_run_stream_trace_01():
    raise Exception("mock exception")

@components_run_stream_trace
def mock_components_run_stream_trace_02():
    raise TestException()

@list_trace
def mock_list_trace_01():
    raise Exception("mock exception")

@list_trace
def mock_list_trace_02():
    raise TestException()

class TestTraceSkipRaiseError(unittest.TestCase):
    def setUp(self):
        os.environ["APPBUILDER_TRACE_DEBUG"] = "True"
        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "true"

    def tearDown(self):
        del os.environ["APPBUILDER_TRACE_DEBUG"]
        del os.environ["APPBUILDER_SDK_TRACE_ENABLE"]

    def test_session_post(self):
        # test_session_post APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_post_01()
        # test_session_post APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_post_01()
        with self.assertRaises(TestException):
            mock_post_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_post_02()

    def test_client_run_trace(self):
        # test_client_run_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_client_run_trace_01()
        # test_client_run_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_client_run_trace_01()
        with self.assertRaises(TestException):
            mock_client_run_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_client_run_trace_02()

    def test_client_tool_trace(self):
        # test_client_tool_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_client_tool_trace_01()
        # test_client
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_client_tool_trace_01()
        with self.assertRaises(TestException):
            mock_client_tool_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_client_tool_trace_02()

    def test_assistent_tool_trace(self):
        # test_assistent_tool_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_assistent_tool_trace_01()
        # test_assistent_tool_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_assistent_tool_trace_01()
        with self.assertRaises(TestException):
            mock_assistent_tool_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_assistent_tool_trace_02()

    def test_assistant_run_trace(self):
        # test_assistant_run_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_assistant_run_trace_01()
        # test_assistant_run_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_assistant_run_trace_01()
        with self.assertRaises(TestException):
            mock_assistant_run_trace_02()
        
        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_assistant_run_trace_02()

    def test_assistent_stream_run_trace(self):
        # test_assistent_stream_run_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_assistent_stream_run_trace_01()
        # test_assistent_stream_run_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_assistent_stream_run_trace_01()
        with self.assertRaises(TestException):
            mock_assistent_stream_run_trace_02()
        
        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_assistent_stream_run_trace_02()

    def test_assistent_stream_run_with_handler_trace(self):
        # test_assistent_stream_run_with_handler_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_assistent_stream_run_with_handler_trace_01()
        # test_assistent_stream_run_with_handler_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_assistent_stream_run_with_handler_trace_01()
        with self.assertRaises(TestException):
            mock_assistent_stream_run_with_handler_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_assistent_stream_run_with_handler_trace_02()

    def test_components_run_trace(self):
        # test_components_run_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_components_run_trace_01()
        # test_components_run_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_components_run_trace_01()
        with self.assertRaises(TestException):
            mock_components_run_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_components_run_trace_02()
    
    def test_components_run_stream_trace(self):
        # test_components_run_stream_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_components_run_stream_trace_01()
        # test_components_run_stream_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_components_run_stream_trace_01()
        with self.assertRaises(TestException):
            mock_components_run_stream_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_components_run_stream_trace_02()

    def test_list_trace(self):
        # test_list_trace APPBUILDER_TRACE_DEBUG = true
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"
        with self.assertRaises(Exception):
            mock_list_trace_01()
        # test_list_trace APPBUILDER_TRACE_DEBUG = false
        os.environ["APPBUILDER_TRACE_DEBUG"] = "false"
        with self.assertRaises(Exception):
            mock_list_trace_01()
        with self.assertRaises(TestException):
            mock_list_trace_02()

        os.environ["APPBUILDER_SDK_TRACE_ENABLE"] = "false"
        with self.assertRaises(Exception):
            mock_list_trace_02()


if __name__ == '__main__':
    unittest.main()
