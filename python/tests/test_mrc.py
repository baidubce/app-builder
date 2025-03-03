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
import time

class TestMRC(unittest.TestCase):
    def setUp(self):
        '''
        return mrc class
        '''
        # 设置环境变量和初始化TestMRCComponent实例
        self.model_name = "ERNIE-3.5-8K"
        self.mrc = appbuilder.MRC(model=self.model_name)

    def test_mrc_with_custom_context_list(self):
        """测试run方法使用自定义格式context_out_list"""
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        context_list = appbuilder.Message(["""如何办理残疾人通行证一、残疾人通行证办理条件：
        1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
        2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）、C5（右下肢、双下肢残疾）的机动车驾驶证，
        听力残疾人驾驶证须有“驾驶机动车应佩戴助听设备”的批注（批注请到各车管分所办理）；""",
                            """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
        C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
        北京市无障碍环境建设促进中心（北京市残疾人辅助器具资源中心），咨询电话：63547715 或68397831。三、所需材料：1、
        有效的身份证明原件和复印件；2、残疾人证原件和复印件；3、驾驶证原件和复印件；
        4、车辆行驶证原件和复印件；5、有效的机动车交强险凭证。"""])
        answer = self.mrc(msg, context_list)
        self.assertIsNotNone(answer)
        time.sleep(1) 

    def test_mrc_with_invalid_context(self):
        """测试run方法使用无效格式的context_list"""
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        context_list = appbuilder.Message("无效样式")
        self.mrc(msg, context_list)
        time.sleep(1) 

    def test_mrc_with_reject(self):
        """测试拒答功能开启情况"""
        # 测试阅读理解问答
        msg = "残疾人怎么办相关证件"
        msg = appbuilder.Message(msg)
        context_list = appbuilder.Message(["""如何办理残疾人通行证一、残疾人通行证办理条件：
        1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
        2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）、C5（右下肢、双下肢残疾）的机动车驾驶证，
        听力残疾人驾驶证须有“驾驶机动车应佩戴助听设备”的批注（批注请到各车管分所办理）；""",
                            """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
        C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
        北京市无障碍环境建设促进中心（北京市残疾人辅助器具资源中心），咨询电话：63547715 或68397831。三、所需材料：1、
        有效的身份证明原件和复印件；2、残疾人证原件和复印件；3、驾驶证原件和复印件；
        4、车辆行驶证原件和复印件；5、有效的机动车交强险凭证。"""])
        answer = self.mrc(msg, context_list, reject=True, clarify=True, highlight=True, friendly=True,cite=True)
        print(answer)

    def test_tool_eval_valid(self):
        """测试 tool 方法对有效请求的处理。"""
        context_list = ["""如何办理残疾人通行证一、残疾人通行证办理条件：
        1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
        2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）、C5（右下肢、双下肢残疾）的机动车驾驶证，
        听力残疾人驾驶证须有“驾驶机动车应佩戴助听设备”的批注（批注请到各车管分所办理）；""",
                            """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
        C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
        北京市无障碍环境建设促进中心（北京市残疾人辅助器具资源中心），咨询电话：63547715 或68397831。三、所需材料：1、
        有效的身份证明原件和复印件；2、残疾人证原件和复印件；3、驾驶证原件和复印件；
        4、车辆行驶证原件和复印件；5、有效的机动车交强险凭证。"""]
        params = {
            'name': 'mrc',
            'query': '残疾人怎么办相关证件',
            'context_list': context_list
        }
        result = self.mrc.tool_eval(streaming=True, **params)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)
        result = self.mrc.tool_eval(streaming=False, **params)
        res = [item for item in result]

    def test_tool_eval_invalid(self):
        """测试 tool 方法对无效请求的处理。"""
        context_list = ["""如何办理残疾人通行证一、残疾人通行证办理条件：
        1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
        2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）、C5（右下肢、双下肢残疾）的机动车驾驶证，
        听力残疾人驾驶证须有“驾驶机动车应佩戴助听设备”的批注（批注请到各车管分所办理）；""",
                            """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
        C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
        北京市无障碍环境建设促进中心（北京市残疾人辅助器具资源中心），咨询电话：63547715 或68397831。三、所需材料：1、
        有效的身份证明原件和复印件；2、残疾人证原件和复印件；3、驾驶证原件和复印件；
        4、车辆行驶证原件和复印件；5、有效的机动车交强险凭证。"""]
        with self.assertRaises(ValueError):
            params = {
                'name': 'mrc',
                'query': '残疾人怎么办相关证件'
            }
            result = self.mrc.tool_eval(streaming=True, **params)
            next(result)
        
        with self.assertRaises(ValueError):
            params = {
                'name': 'mrc',
                'context_list': context_list
            }
            result = self.mrc.tool_eval(streaming=True, **params)
            next(result)

if __name__ == '__main__':
    unittest.main()
