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
from appbuilder.tests.component_schemas import text_schema, url_schema, image_schema, code_schema, file_schema, oral_text_schema, references_schema, chart_schema, audio_schema, plan_schema, function_call_schema

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
        image_url = "https://bj.bcebos.com/v1/appbuilder/test_handw"\
                    "rite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8"\
                    "m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2"\
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
        image_url=("https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?"
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
        return {"text": ["Hello"]}

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
        image_url = "https://bj.bcebos.com/v1/appbuilder/table_ocr_test.png?"\
            "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T12%3A37%3A09Z%2F-1%2Fhost%2Fab528a5a9120d328dc6d18c6"\
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
        audio_file_url ="https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
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
            "text":text
        }
    
    def schemas(self):
        return [text_schema]
    
    def outputs(self):
        return {"text": ["OPPO"]}

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
}