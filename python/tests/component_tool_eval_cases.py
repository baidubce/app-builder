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

class AnimalRecognitionCase:
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

class ASRCase:
    def inputs(self):
        return {
            "file_url": "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                        "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                            "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
        }
    def outputs(self):
        return {"text": ["北京科技馆"]}

class TreeMindCase:
    def inputs(self):
        return {"query": "生成一份年度总结的思维导图"}
    
class ImageUnderstandCase:
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

component_tool_eval_cases = {
    "AnimalRecognition": AnimalRecognitionCase,
    "ImageUnderstand": ImageUnderstandCase,
    "ASR": ASRCase,
    "TreeMind": TreeMindCase
}