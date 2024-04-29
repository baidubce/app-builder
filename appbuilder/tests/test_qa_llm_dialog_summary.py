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

import unittest
import os
import time
import appbuilder
import requests
from parameterized import parameterized, param
import appbuilder
from appbuilder import Message

from pytest_config import LoadConfig
conf = LoadConfig()

from pytest_utils import Utils
util = Utils()

from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"
models = appbuilder.get_model_list("", ["chat"], True)


@unittest.skip(reason="消耗过多时间")
# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestDialogSummaryComponent(unittest.TestCase):
    @parameterized.expand([
        # 20240311千帆模型改名兼容
        # eb-turbo-appbuilder
        param("eb-turbo-appbuilder", text, None, None),
        # EB-turbo-AppBuilder专用版
        param("EB-turbo-AppBuilder专用版", text, None, None),
        # ernie_speed_appbuilder
        param("ernie_speed_appbuilder", text, None, None),
        # ERNIE Speed-AppBuilder
        param("ernie_speed_appbuilder", text, None, None),

        param(models[0], text, True, None),
        param(models[0], text, False, 0.1),
        param(models[0], text, False, 0.99),
        # 字符
        param(models[0], "客户：你好，我购买的新笔记本电脑出现了无法连接无线网络的问题。\n客服：你好，很"
                                        "抱歉听到你遇到了网络问题。请问你尝试过重新启动路由器和笔记本电脑吗？\n客户：是的，我已经"
                                        "尝试过，但问题仍然存在。\n客服：明白了。请问其他设备是否能够成功连接到同一网络？\n客户："
                                        "是的，我的手机和平板电脑都可以正常连接。\n客服：感谢你的反馈。在笔记本电脑无法连接网络时，"
                                        "你是否收到了任何错误消息？\n客户：是的，我收到了一个提示说“无法获得有效的IP地址”。\n客服"
                                        "：好的，这是有关IP地址分配的问题。请尝试手动分配一个IP地址并查看是否解决问题。我可以为你"
                                        "提供详细的步骤。\n客户：好的，我愿意尝试。\n客户：我按照你提供的步骤手动分配了IP地址，但"
                                        "问题依然存在。\n客服：谢谢你的尝试。我们可能需要进一步检查网络设置。你是否同意进行远程连"
                                        "接以便我查看电脑的网络配置？\n客户：可以。\n客服：我发现你的网络配置正常，但存在一个驱动"
                                        "程序更新可能会解决的问题。你是否同意我协助你更新网络驱动程序？\n客户：好的，请帮我更新。"
                                        "\n客户：感谢你的帮助，更新后问题已经解决了。我现在可以正常连接到无线网络了。\n客服：太好"
                                        "了，我很高兴能够帮到你。如果还有其他问题，随时告诉我。\n客户：其实，我还有一个关于电池寿"
                                        "命的问题。最近感觉电池很快就耗尽了。\n客服：明白了，电池寿命问题也很重要。你可以尝试通过"
                                        "减少屏幕亮度和关闭一些背景应用来延长电池寿命。另外，我可以为你提供一些建议，帮你优化电池使"
                                        "用。", None, None),
    ] + [param(model, text, None, None) for model in models if
         model not in ["Yi-34B-Chat", "ChatLaw", "BLOOMZ-7B", "Qianfan-BLOOMZ-7B-compressed"]])
    def test_normal_case(self, model_name, text, stream, temperature):
        """
        正常用例
        """
        builder = appbuilder.DialogSummary(model=model_name)
        msg = Message(content=text)
        input_params = {}

        if stream is not None:
            input_params["stream"] = stream
        if temperature is not None:
            input_params["temperature"] = temperature

        res = builder(msg, **input_params)

        if stream:
            content = "".join([i for i in res.content])
        else:
            content = res.content
        assert "诉求" in content
        assert "回应" in content
        assert "解决情况" in content
        time.sleep(10)

    @parameterized.expand([
        # timeout为0
        param("eb-turbo-appbuilder", "客户：你好，我购买的新笔记本电脑出现了无法连接无线网络的问题。\n客服：你好，很"
                                            "抱歉听到你遇到了网络问题。请问你尝试过重新启动路由器和笔记本电脑吗？\n客户：是的，我已经"
                                            "尝试过，但问题仍然存在。\n客服：明白了。请问其他设备是否能够成功连接到同一网络？\n客户："
                                            "是的，我的手机和平板电脑都可以正常连接。\n客服：感谢你的反馈。在笔记本电脑无法连接网络时，"
                                            "你是否收到了任何错误消息？\n客户：是的，我收到了一个提示说“无法获得有效的IP地址”。\n客服"
                                            "：好的，这是有关IP地址分配的问题。请尝试手动分配一个IP地址并查看是否解决问题。我可以为你"
                                            "提供详细的步骤。\n客户：好的，我愿意尝试。\n客户：我按照你提供的步骤手动分配了IP地址，但"
                                            "问题依然存在。\n客服：谢谢你的尝试。我们可能需要进一步检查网络设置。你是否同意进行远程连"
                                            "接以便我查看电脑的网络配置？\n客户：可以。\n客服：我发现你的网络配置正常，但存在一个驱动"
                                            "程序更新可能会解决的问题。你是否同意我协助你更新网络驱动程序？\n客户：好的，请帮我更新。"
                                            "\n客户：感谢你的帮助，更新后问题已经解决了。我现在可以正常连接到无线网络了。\n客服：太好"
                                            "了，我很高兴能够帮到你。如果还有其他问题，随时告诉我。\n客户：其实，我还有一个关于电池寿"
                                            "命的问题。最近感觉电池很快就耗尽了。\n客服：明白了，电池寿命问题也很重要。你可以尝试通过"
                                            "减少屏幕亮度和关闭一些背景应用来延长电池寿命。另外，我可以为你提供一些建议，帮你优化电池使"
                                            "用。" * 100),
    ])
    def test_abnormal_case(self, model_name, text):
        """
        异常用例
        """
        try:
            builder = appbuilder.DialogSummary(model=model_name)
            msg = Message(content=text)
            res = builder(msg)
            content = res.content
            assert False, "未捕获到错误信息"
        except Exception as e:
            print(e)

    
if __name__ == '__main__':
    unittest.main()