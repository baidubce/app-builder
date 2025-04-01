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
from appbuilder.core.component import Component
from appbuilder.tests.component_schemas import text_schema, url_schema, image_schema, code_schema, file_schema, \
    oral_text_schema, references_schema, chart_schema, audio_schema, plan_schema, function_call_schema


class Case():
    def init_args(self):
        return {}

    def inputs(self):
        return NotImplementedError()

    def outputs(self):
        return {}

    def schemas(self):
        return NotImplementedError()

    def envs(self):
        return {}


class AnimalRecognitionCase(Case):
    def inputs(self):
        return {
            "img_name": "",
            "img_url": "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                       "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                       "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                       "62cf937c03f8c5260d51c6ae"
        }

    def outputs(self):
        return {"text": ["熊猫"]}

    def schemas(self):
        return [text_schema]


class ASRCase(Case):
    def inputs(self):
        return {
            "file_url": "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                        "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                        "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
        }

    def outputs(self):
        return {"text": ["北京科技馆"]}

    def schemas(self):
        return [text_schema]


class TreeMindCase(Case):
    def inputs(self):
        return {"query": "生成一份年度总结的思维导图"}

    def schemas(self):
        return [text_schema, url_schema]


class ImageUnderstandCase(Case):
    def inputs(self):
        return {
            "img_url": "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                       "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                       "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                       "62cf937c03f8c5260d51c6ae",
            "img_name": "test_img.jpg"
        }

    def outputs(self):
        return {"text": ["熊猫"]}

    def schemas(self):
        return [text_schema]


class Text2ImageCase(Case):
    def inputs(self):
        return {"query": "生成一张熊猫图片"}

    def schemas(self):
        return [url_schema]


class StyleRewriteCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {"query": "文心大模型发布新版"}

    def schemas(self):
        return [text_schema]


class QRcodeOCRCase(Case):
    def inputs(self):
        image_url = "https://bj.bcebos.com/v1/appbuilder/qrcode_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-" \
                    "01-24T12%3A45%3A13Z%2F-1%2Fhost%2Ffc43d07b41903aeeb5a023131ba6" \
                    "e74ab057ce26d50e966dc31ff083e6a9c41b"
        return {
            "file_names": ["text"],
            "_sys_file_urls": {"text": image_url}
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["ocr文字识别"]}


class HallucinationDetectionCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": '澳门新麻蒲烤肉店每天开门吗？',
            "context": ('澳门美食： 澳门新麻蒲韩国烤肉店\n'
                        '在澳门一年四季之中除了火锅，烤肉也相当受欢迎。提到韩烧，有一间令我印象最深刻，就是号称韩国第一的烤肉店－新麻蒲韩国烤肉店，光是韩国的分店便多'
                        '达四百多间，海外分店更是遍布世界各地，2016年便落户澳门筷子基区，在原本已经食肆林立的地方一起百花齐放！店内的装修跟韩国分店还完度几乎没差，让'
                        '食客彷如置身于韩国的感觉，还要大赞其抽风系统不俗，离开时身上都不会沾上烤肉味耶！\n'
                        '时间：周一至周日 下午5:00 - 上午3:00\n'
                        '电话：＋853 2823 4012\n'
                        '地址：澳门筷子基船澳街海擎天第三座地下O号铺96号\n'
                        '必食推介:\n'
                        '护心肉二人套餐\n'
                        '来新麻蒲必试的有两样东西，现在差不多每间烤肉店都有炉边烤蛋，但大家知道吗？原来新麻蒲就是炉边烤蛋的开创者，既然是始祖，这已经是个非吃不可的理'
                        '由！还有一款必试的就是护心肉，即是猪的横隔膜与肝中间的部分，每头猪也只有200克这种肉，非常珍贵，其味道吃起来有种独特的肉香味，跟牛护心肉一样'
                        '精彩！\n'
                        '秘制猪皮\n'
                        '很多怕胖的女生看到猪皮就怕怕，但其实猪皮含有大量胶原蛋白，营养价值很高呢！这里红通通的猪皮还经过韩国秘制酱汁处理过，会有一点点辣味。烤猪皮的'
                        '时候也需特别注意火侯，这样吃起来才会有外脆内Q的口感！'),
            "answer": '澳门新麻蒲烤肉店并不是每天开门，周日休息。'
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["存在幻觉"]}


class HandWriteOCRCase(Case):
    def inputs(self):
        image_url = "https://bj.bcebos.com/v1/appbuilder/test_handw" \
                    "rite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8" \
                    "m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2" \
                    "F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b"
        return {
            "file_names": ["text"],
            "_sys_file_urls": {"text": image_url}
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["银杏树"]}


class MixCardOCRCase(Case):
    def inputs(self):
        image_url = ("https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?"
                     "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T06"
                     "%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe"
                     "1865e4393da5a3515e90d72d81ef18296bd29598")
        return {
            "file_names": ["test"],
            "_sys_file_urls": {"test": image_url}
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["北京市公安局"]}


class TranslationCase(Case):
    def inputs(self):
        return {
            "q": "你好",
            "to_lang": "en",
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["hello"]}


class GeneralOCRCase(Case):
    def inputs(self):
        return {
            "img_url": "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                       "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                       "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                       "857a27513734d765495f89ffa5f73",
            "img_name": "test_img.jpg"
        }

    def outputs(self):
        return {"text": ["识别结果"]}

    def schemas(self):
        return [text_schema]


class TableOCRCase(Case):
    def inputs(self):
        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6" \
                    "064079145ff4698856f477b820147768fc2187d3"
        return {
            "file_names": [image_url]
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["http"]}


class Text2ImageCase(Case):
    def inputs(self):
        return {
            'query': '生成一张小猫图片',
        }

    def schemas(self):
        return [image_schema]


class StyleWritingCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "帮我写一篇关于足球的文案",
            "style": "小红书",
            "length": 100,
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["足球"]}


class TreeMindCase(Case):
    def inputs(self):
        return {
            "query": "生成一份年度总结的思维导图"
        }

    def schemas(self):
        return [text_schema, url_schema, image_schema]


class PlantRecognitionCase(Case):
    def inputs(self):
        img_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                  "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                  "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                  "62cf937c03f8c5260d51c6ae"
        img_name = "test_img.jpg"
        return {
            "img_url": img_url,
            "img_name": img_name
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["非植物"]}


class ASRCase(Case):
    def inputs(self):
        audio_file_url = "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                         "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                         "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"

        return {
            "file_url": audio_file_url
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["北京科技馆"]}


class ObjectRecognitionCase(Case):
    def inputs(self):
        img_url = "https://bj.bcebos.com/v1/appbuilder/object_recognize_test.png?" \
                  "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                  "11T11%3A00%3A19Z%2F-1%2Fhost%2F2c31bf29205f61e58df661dc80af31a1dc" \
                  "1ba1de0a8f072bc5a87102bd32f9e3"
        return {
            "img_url": img_url
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["苹果"]}


class SimilarQuestionCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "我想吃冰淇淋，哪里的冰淇淋比较好吃？"
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["冰淇淋"]}


class OralQueryGenerationCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
                '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
                '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
                '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
                '，实时视频分享您的生活。')
        return {
            "text": text
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["OPPO"]}


class QueryRewriteCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "我想吃冰淇淋，哪里的冰淇淋比较好吃？",
            "rewrite_type": "带机器人回复"
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["冰淇淋"]}


class Nl2pandasComponentCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "给我一份2020年到2022年每年的销售额",
            "table_info": '''表格列信息如下：
                学校名 : 清华附小 , 字符串类型，代表小学学校的名称
                所属地区 : 西城区 , 字符串类型，表示该小学学校所在的位置
                创办时间 : 1998 , 数字值类型，表示该小学学校的创办时间
                类别 : 公立小学 , 字符串类型，表示该小学学校所在的类别
                学生人数 : 2000 , 数字值类型，表示该小学学校的学生数量
                教职工人数 : 140 , 数字值类型，表示该小学学校的教职工数量
                教学班数量 : 122 , 数字值类型，表示该小学学校的教学班数量
                '''
        }

    def schemas(self):
        return [text_schema]


class DialogSummaryCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "请给我总结一下这段对话",
        }

    def schemas(self):
        return [text_schema]


class MRCCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "残疾人怎么办相关证件",
            "context_list": [
                """如何办理残疾人通行证一、残疾人通行证办理条件：
                1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
                2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）、C5（右下肢、双下肢残疾）的机动车驾驶证，
                听力残疾人驾驶证须有“驾驶机动车应佩戴助听设备”的批注（批注请到各车管分所办理）；""",
                """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
北京市无障碍环境建设促进中心（北京市残疾人辅助器具资源中心），咨询电话：63547715 或68397831。三、所需材料：1、
有效的身份证明原件和复印件；2、残疾人证原件和复印件；3、驾驶证原件和复印件；
4、车辆行驶证原件和复印件；5、有效的机动车交强险凭证。"""
            ]
        }

    def schemas(self):
        return [text_schema]


class IsComplexQueryCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？",
        }

    def schemas(self):
        return [text_schema]

    def outputs(self):
        return {"text": ["复杂问题"]}


class QAPairMiningCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "2017年，工商银行根据外部宏观环境变化...",
        }

    def schemas(self):
        return [text_schema]


class QueryDecompositionCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "吸塑包装盒在工业化生产和物流运输中分别有什么重要性？",
        }

    def schemas(self):
        return [text_schema]


class TagExtractionCase(Case):
    def init_args(self):
        return {"model": "ERNIE-3.5-8K"}

    def inputs(self):
        return {
            "query": "本实用新型公开了一种可利用热能的太阳能光伏光热一体化组件，包括太阳能电池，还包括有吸热板，太阳能电池粘附在吸热板顶面，吸热板内嵌入有热电材料制成的内芯，吸热板底面设置有蛇形管。本实用新型结构紧凑，安装方便，能充分利用太阳能电池散发的热能，具有较高的热能利用率。",
        }

    def schemas(self):
        return [text_schema]


component_tool_eval_cases = {
    "AnimalRecognition": AnimalRecognitionCase,
    "ImageUnderstand": ImageUnderstandCase,
    "ASR": ASRCase,
    "TreeMind": TreeMindCase,
    "StyleRewrite": StyleRewriteCase,
    "HallucinationDetection": HallucinationDetectionCase,
    "QRcodeOCR": QRcodeOCRCase,
    "HandwriteOCR": HandWriteOCRCase,
    "MixCardOCR": MixCardOCRCase,
    "Translation": TranslationCase,
    "GeneralOCR": GeneralOCRCase,
    "TableOCR": TableOCRCase,
    "Text2Image": Text2ImageCase,
    "StyleWriting": StyleWritingCase,
    "TreeMind": TreeMindCase,
    "PlantRecognition": PlantRecognitionCase,
    "ASR": ASRCase,
    "ObjectRecognition": ObjectRecognitionCase,
    "SimilarQuestion": SimilarQuestionCase,
    "OralQueryGeneration": OralQueryGenerationCase,
    "QueryRewrite": QueryRewriteCase,
    "Nl2pandasComponent": Nl2pandasComponentCase,
    "DialogSummary": DialogSummaryCase,
    "MRC": MRCCase,
    "IsComplexQuery": IsComplexQueryCase,
    "QAPairMining": QAPairMiningCase,
    "QueryDecomposition": QueryDecompositionCase,
    "TagExtraction": TagExtractionCase,
}