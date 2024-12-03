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
        return {"model": "Qianfan-Agent-Speed-8k"}
    
    def inputs(self):
        return {"query": "文心大模型发布新版"}

    def schemas(self):
        return [text_schema]


class HallucinationDetectionCase(Case):
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


component_tool_eval_cases = {
    "AnimalRecognition": AnimalRecognitionCase,
    "ImageUnderstand": ImageUnderstandCase,
    "ASR": ASRCase,
    "TreeMind": TreeMindCase,
    "StyleRewrite": StyleRewriteCase,
    "HallucinationDetection": HallucinationDetectionCase
}