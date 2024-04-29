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
import appbuilder

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestDialogSummary(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。
        
        Args:
            无参数，默认值为空。
        
        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.model_name = "ERNIE Speed-AppBuilder"
        self.node = appbuilder.DialogSummary(model=self.model_name)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数"""
        dialog_text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
        msg = appbuilder.Message(dialog_text)
        summary = self.node(msg)
        self.assertIsNotNone(summary)

    def test_run_with_stream_and_temperature(self):
        """测试不同的 stream 和 temperature 参数值"""
        dialog_text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
        msg = appbuilder.Message(dialog_text)
        summary = self.node(msg, stream=False, temperature=0.5)
        self.assertIsNotNone(summary)

    def test_run_with_model_names(self):
        """测试不同的 stream 和 temperature 参数值"""

        chats = appbuilder.get_model_list(api_type_filter=["chat"])
        self.assertTrue("EB-turbo-AppBuilder专用版" in chats)

        appbuilder.DialogSummary(model="EB-turbo-AppBuilder专用版")

        with self.assertRaises(Exception):
            appbuilder.DialogSummary(model="")

if __name__ == '__main__':
    unittest.main()