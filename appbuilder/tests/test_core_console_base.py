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
import os
import unittest

from appbuilder.core.console.base import ConsoleLLMMessage,ConsoleCompletionResponse
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.llms.base import CompletionResponse, LLMMessage
from appbuilder.core.message import Message  


# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
@unittest.skip(reason="暂时跳过")
class TestCoreConsoleBase(unittest.TestCase):
    def test_ConsoleLLMMessage_init(self):
        message=Message()
        llmMessage=LLMMessage(message)
        clm=ConsoleLLMMessage(llmMessage)
        self.assertIsInstance(clm,ConsoleLLMMessage)
        
    def test_ConsoleCompletionResponse_init(self):
        # 测试stream=True
        cr=CompletionResponse()
        ccr=ConsoleCompletionResponse(response=cr,stream=True)
        
        

if __name__ == '__main__':
    unittest.main()