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

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
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
        # 配置测试环境
        try:
            subprocess.check_output(['python3','-m','pip', 'install', 'sentry-sdk==1.44.1'])
        except Exception as e:
            print('pip uninstall sentry-sdk failed')

        os.environ["ENABLE_SENTRY_TRACE"] = "true"
        os.environ["SENTRY_DSN"] = "test"

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
            play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model='eb-4')
            msg = appbuilder.Message({
                "name": "小明",
                "bot_name": "机器人",
                "bot_type": "聊天机器人",
                "bot_function": "聊天",
                "bot_question": "你好吗？"
            })

            answer = play.run(message=msg, stream=False, temperature=1)
            print(f"Playground Answer: {answer}")

            # test Components tool_eval
            audio_file_url = ("https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1"
                                "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost"
                                "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411")
            asr = appbuilder.ASR()
            raw_audio = requests.get(audio_file_url).content
            inp = appbuilder.Message(content={"raw_audio": raw_audio})
            result = asr.tool_eval(name="asr", streaming=True, file_url=audio_file_url)
            for res in result:
                print(f"ASR Tool_Eval Result: {res}")

        # 清理测试环境
        try:
            subprocess.check_output(['python3','-m','pip', 'uninstall', 'sentry-sdk', '-y'])
        except Exception as e:
            print('pip uninstall sentry-sdk failed')

if __name__ == '__main__':
    unittest.main()