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
import appbuilder
from appbuilder import Message

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestDialogSummaryComponent(unittest.TestCase):

    def test_run(self):
        model_name = "ERNIE-3.5-8K"
        text = ("客户：你好，我购买的新笔记本电脑出现了无法连接无线网络的问题。客服：你好，很抱歉听到你遇到了"
                "网络问题。请问你尝试过重新启动路由器和笔记本电脑吗？客户：是的，我已经尝试过，但问题仍然存在。客服："
                "明白了。请问其他设备是否能够成功连接到同一网络？客户：是的，我的手机和平板电脑都可以正常连接。客服："
                "感谢你的反馈。在笔记本电脑无法连接网络时，你是否收到了任何错误消息？客户：是的，我收到了一个提示说"
                "“无法获得有效的IP地址”。客服：好的，这是有关IP地址分配的问题。请尝试手动分配一个IP地址并查看是否"
                "解决问题。我可以为你提供详细的步骤。客户：好的，我愿意尝试。客户：我按照你提供的步骤手动分配了IP地址，"
                "但问题依然存在。客服：谢谢你的尝试。我们可能需要进一步检查网络设置。你是否同意进行远程连接以便我查看电脑"
                "的网络配置？客户：可以。客服：我发现你的网络配置正常，但存在一个驱动程序更新可能会解决的问题。你是否同意我"
                "协助你更新网络驱动程序？客户：好的，请帮我更新。客户：感谢你的帮助，更新后问题已经解决了。我现在可以正常连接到"
                "无线网络了。客服：太好了，我很高兴能够帮到你。如果还有其他问题，随时告诉我。客户：其实，我还有一个关于电池寿命的问题。"
                "最近感觉电池很快就耗尽了。客服：明白了，电池寿命问题也很重要。你可以尝试通过减少屏幕亮度和关闭一些背景应用来延长电池寿命。"
                "另外，我可以为你提供一些建议，帮你优化电池使用。")
        stream = None
        temperature = None

        builder = appbuilder.DialogSummary(model=model_name)
        msg = Message(content=text)
        input_params = {}

        if stream is not None:
            input_params["stream"] = stream
        if temperature is not None:
            input_params["temperature"] = temperature

        res = builder(msg, **input_params)
        content = "".join(res.content) if stream else res.content

        self.assertIn("诉求", content)
        self.assertIn("回应", content)
        self.assertIn("解决情况", content)

if __name__ == '__main__':
    unittest.main()
