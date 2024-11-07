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
import appbuilder
import appbuilder
class LoadConfig(object):
    """
    config
    """
    def __init__(self):
        """
        初始化函数，读取配置文件并设置实例属性。
        """
        self.token = os.environ.get("APPBUILDER_TOKEN", "")
        self.console_url = os.environ.get("GATEWAY_URL", "https://appbuilder.baidu.com")
        self.cookie =  os.environ.get("COOKIE", "")
        self.csrftoken = os.environ.get('CSRFTOKEN', "")

        log.info("token: %s" % self.token)
        log.info("console_url: %s" % self.console_url)
        log.info("cookie: %s" % self.cookie)
        log.info("csrftoken: %s" % self.csrftoken)

import random
import string
import os

class Utils(object):
    """
    utils 方法父类
    """
    @staticmethod
    def get_random_string(str_len, prefix=None):
        """
        生成随机字符串，可指定前缀
        """
        gen_name = ''.join(
            random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
        )
        if prefix:
            name = str(prefix) + gen_name
        else:
            name = gen_name
        return name

    @staticmethod
    def get_data_file(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_file_path = os.path.join(current_dir, "data", filename)
        return full_file_path

from appbuilder.utils.logger_util import get_logger
from appbuilder.core._exception import ModelNotSupportedException
log = get_logger(__name__)

text = "用户:喂我想查一下我的话费\n坐席:好的女士您话费余的话还有87.49元钱\n用户:好的知道了谢谢\n坐席:嗯不客气祝您生活愉快再见"

models = appbuilder.get_model_list("", ["chat"], True)

file_bos_url = ("https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/[测试]超市收入明细表格.xlsx?authorization=bce-"
                "auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T09%3A51%3A14Z/-1/host/1802a9c9142ef328d61e7673db7"
                "c1f05842b2af93d18a02ac7ef7aa6f64db54e")
err_file_bos_url = ("https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/[测试]超市收入明细表格.xlsx?authorization="
                    "bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T09%3A51%3A14Z/-1/host/1802a9c9142ef328d6"
                    )

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestExcel2figure(unittest.TestCase):
    # @parameterized.expand([
    #     param("ERNIE-Bot 4.0", "2020年各个月份的利润分别是多少？使用条形图绘制出来", file_bos_url),
    # ] + [param(model, "2020年各个月份的利润分别是多少？使用条形图绘制出来", file_bos_url) for model in models if
    #      model not in ["Yi-34B-Chat", "ChatLaw", "BLOOMZ-7B", "Qianfan-BLOOMZ-7B-compressed"]])
    # def test_normal_case(self, model_name, query, excel_file_url):
    #     """
    #     正常用例
    #     """
    #     # 创建 component 对象，推荐使用 ERNIE-Bot 4.0 获取更稳定的画图效果
    #     component = appbuilder.Excel2Figure(model=model_name)

    #     # 准备 excel 文件链接，该链接需要是公网可访问的地址
    #     # 针对 excel 文件内容绘制图表
    #     result = component.run(appbuilder.Message({
    #         "query": query,
    #         "excel_file_url": excel_file_url,
    #     }))

    #     # 输出运行结果
    #     content = result.content
    #     if model_name == "ERNIE-Bot 4.0":
    #         assert content, "未获取到图片地址"
    #     time.sleep(1)
            
    def test_abnormal_case(self):
        """
        异常用例
        """
        # test Model[aaa] not available
        with self.assertRaises(ModelNotSupportedException):
            builder = appbuilder.Excel2Figure(model="aaa")

        # test query and excel_file_url error
        test_list=[
            {
                "excel_file_url": file_bos_url
            },
            {
                "query": "2020年各个月份的利润分别是多少？使用条形图绘制出来",
            }
        ]
        for item in test_list:
            try:
                builder = appbuilder.Excel2Figure(model="ERNIE-Bot 4.0")
                res = builder(builder.run(appbuilder.Message(item)))
            except Exception as e:
                assert "1 validation error for Excel2FigureArgs" in str(e)

        try:
            builder = appbuilder.Excel2Figure(model="ERNIE-Bot 4.0")
            res = builder(builder.run(appbuilder.Message({
                "query": "2020年各个月份的利润分别是多少？使用条形图绘制出来"*30,
                "excel_file_url": file_bos_url
            })))
        except Exception as e:
            assert "1 validation error for Excel2FigureArgs" in str(e)
            
    def test_check_model_and_get_model_url(self):
        with self.assertRaises(ModelNotSupportedException):
            e2f=appbuilder.Excel2Figure(model="Yi-34B-Chat")
        with self.assertRaises(ValueError):
            e2f=appbuilder.Excel2Figure(model="")

    def test_run(self):
        e2f=appbuilder.Excel2Figure(model="Llama-2-7B-Chat")   
        msg=appbuilder.Message({
            "query": "2019年各个月份的利润分别是多少？",
            "excel_file_url": file_bos_url
        })
        result_msg=e2f.run(msg)
        
    def test_tool_eval(self):
        e2f=appbuilder.Excel2Figure(model="Llama-2-7B-Chat")   
        # with self.assertRaises(RuntimeError) as context:
        te=e2f.tool_eval(
                streaming=False,
                origin_query="",
                file_urls={'test1':'test1','test2':'test2'}
                )
        with self.assertRaises(RuntimeError):
            next(te)

        te=e2f.tool_eval(
                streaming=False,
                origin_query="2019年各个月份的利润分别是多少？",
                file_urls={'[测试]超市收入明细表格.xlsx':file_bos_url}
                )
        with self.assertRaises(RuntimeError): 
            res=next(te)
        
        
if __name__ == '__main__':
    unittest.main()