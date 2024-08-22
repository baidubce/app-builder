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
import appbuilder

class TestOralQueryGeneration(unittest.TestCase):
    def test_normal_case(self):
        model_name = "ERNIE-3.5-8K"
        text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
                '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
                '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
                '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
                '，实时视频分享您的生活。')

        query_generation = appbuilder.OralQueryGeneration(model=model_name)
        msg = appbuilder.Message(content=text)
        out = query_generation(msg)

        self.assertIn("OPPO", str(out.content))
        

if __name__ == '__main__':
    unittest.main()
