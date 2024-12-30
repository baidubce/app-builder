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
from appbuilder import AppbuilderInstrumentor, StyleRewrite
from appbuilder.core.components.v2 import StyleRewrite as StyleRewriteV2

logging.basicConfig(level=logging.INFO)

class TestAppbuilderForSentryOff(unittest.TestCase):
    def test_sentry_normal(self):
        """
        测试Sentry的追踪功能是否正常。
        
        Args:
            无。
        
        Returns:
            无返回值。
        
        Raises:
            ImportError: 如果未安装sentry-sdk库，则抛出此异常。
        
        """
        try:
            subprocess.check_output(['python3','-m','pip', 'install', 'sentry-sdk==1.44.1'])
        except Exception as e:
            print('pip uninstall sentry-sdk failed')

        os.environ["ENABLE_SENTRY_TRACE"] = "true"
        os.environ["SENTRY_DSN"] = "test"
        os.environ["APPBUILDER_TRACE_DEBUG"] = "true"

        # 启动跟踪器(仅测试Sentry Trace功能)
        tracer = AppbuilderInstrumentor()
        tracer._instrument()
        # 启动Sentry
        try:
            import sentry_sdk
        except ImportError:
            raise ImportError("Please install `sentry-sdk` first.")
        try:
            sentry_sdk.init(
                dsn="https://c6f17a6bb2163ad7b10760e70cfdba16@appsentry-sandbox.now.baidu-int.com/59",
                traces_sample_rate=1.0,
            )
            logging.info("Sentry SDK is initialized successfully.")
            # _patch_sentry_sdk_trace_id()
            logging.info("Patch_sentry_sdk_trace_id is initialized successfully.")
        except Exception as e:
            print(e)
        # 启动事务
        with sentry_sdk.start_transaction(op="task", name="UT-Components-trace-test"):
            # test Components run
            sr = StyleRewrite(model="ERNIE-3.5-8K")
            text = "成都是个包容的城市"
            style = "直播话术"
            msg = appbuilder.Message(content=text)
            run_out = sr.run(message=msg, style=style)
            print(run_out)
            sr = StyleRewrite(model="ERNIE-3.5-8K")
            tool_eval_out = sr.tool_eval(name="name", query=text, style=style, streaming=True)
            for res in tool_eval_out:
                print(res)

            # test Components v2 tool_eval
            sr_v2 = StyleRewriteV2(model="ERNIE-3.5-8K")
            text = "成都是个包容的城市"
            style = "直播话术"
            tool_eval_out = sr_v2.tool_eval(query=text, style=style)
            for res in tool_eval_out:
                print(res)

        # 清理测试环境
        try:
            subprocess.check_output(['python3','-m','pip', 'uninstall', 'sentry-sdk', '-y'])
        except Exception as e:
            print('pip uninstall sentry-sdk failed')
        del os.environ["ENABLE_SENTRY_TRACE"]
        del os.environ["SENTRY_DSN"]
        del os.environ["APPBUILDER_TRACE_DEBUG"]
        

if __name__ == '__main__':
    unittest.main()