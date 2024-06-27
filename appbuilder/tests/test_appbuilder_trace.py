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
import requests
import appbuilder
import os

# @unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderTrace(unittest.TestCase):
    def setUp(self):
        from appbuilder.trace import create_tracer_provider, AppbuilderInstrumentor
        os.environ["APPBUILDER_SDK_TRACER_CONSOLE"] = "true"
        os.environ["APPBUILDER_SDK_TRACER_PHOENIX"] = "true"
        tracer_provider = create_tracer_provider()
        instrumentor=AppbuilderInstrumentor()
        instrumentor.instrument(tracer_provider=tracer_provider)
    

    def test_animal_recognize_run(self):
        animal_recognition = appbuilder.AnimalRecognition()
        image_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"
        raw_image = requests.get(image_url).content
        message = appbuilder.Message(content={"raw_image": raw_image})
        # Recognize animal
        output = animal_recognition.run(message)
        self.assertIsNotNone(output)


    def test_animal_recognize_tool_eval(self):
        animal_recognition = appbuilder.AnimalRecognition()
        img_url = "https://bj.bcebos.com/v1/appbuilder/animal_recognize_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T" \
                    "12%3A19%3A16Z%2F-1%2Fhost%2F411bad53034fa8f9c6edbe5c4909d76ecf6fad68" \
                    "62cf937c03f8c5260d51c6ae"
        img_name = "test_img.jpg"
        file_urls = {img_name: img_url}
        result = animal_recognition.tool_eval(name="animal_recognition", streaming=True,
                                            img_name=img_name, file_urls=file_urls, origin_query="")
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)
        


    def test_asr_run(self):
        asr = appbuilder.ASR()
        audio_file_url = "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                              "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                              "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
        raw_audio = requests.get(audio_file_url).content
        inp = appbuilder.Message(content={"raw_audio": raw_audio})
        out = asr.run(inp)
        self.assertIsNotNone(out)
        self.assertIsInstance(out, appbuilder.Message)
        self.assertIn('result', out.content)


    def test_asr_tool_eval(self):
        asr = appbuilder.ASR()
        audio_file_url = "https://bj.bcebos.com/v1/appbuilder/asr_test.pcm?authorization=bce-auth-v1" \
                              "%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T10%3A56%3A41Z%2F-1%2Fhost" \
                              "%2Fa6c4d2ca8a3f0259f4cae8ae3fa98a9f75afde1a063eaec04847c99ab7d1e411"
        result = asr.tool_eval(name="asr", streaming=True, file_url=audio_file_url)
        res = [item for item in result]
        self.assertNotEqual(len(res), 0)


    def test_dish_enhance_run(self):
        dish_recognition = appbuilder.DishRecognition()
        image_url = "https://bj.bcebos.com/v1/appbuilder/dish_recognize_test.jpg?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-11T" \
                    "10%3A58%3A25Z%2F-1%2Fhost%2F7b8fc08b2be5adfaeaa4e3a0bb0d1a1281b10da" \
                    "3d6b798e116cce3e37feb3438"
        raw_image = requests.get(image_url).content
        message = appbuilder.Message({"raw_image": raw_image})
        output_message = dish_recognition(message=message)
        self.assertIsInstance(output_message, appbuilder.Message)


    def test_doc_crop_enhance_run(self):
        doc_crop_enhance = appbuilder.DocCropEnhance()
        image_url = "https://bj.bcebos.com/v1/appbuilder/doc_enhance_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01" \
                    "-24T12%3A51%3A09Z%2F-1%2Fhost%2F2020d2433da471b40dafa933d557a1e" \
                    "be8abf28df78010f865e45dfcd6dc3951"
        raw_image = requests.get(image_url).content
        # Create message with raw_image
        message = appbuilder.Message(content={"raw_image": raw_image})
        # Doc enhance
        output = doc_crop_enhance.run(message)
        self.assertIsNotNone(output)


    def test_text_to_image_run(self):
        text2Image = appbuilder.Text2Image()
        inp = appbuilder.Message(content={"prompt": "上海的经典风景"})
        out = text2Image.run(inp)
        self.assertIsNotNone(out)
        self.assertIsInstance(out, appbuilder.Message)


    def test_playground_run(self):
        model_name = "eb-4"
        self.play = appbuilder.Playground(prompt_template="你好，{name}，我是{bot_name}，{bot_name}是一个{bot_type}，我可以{bot_function}，你可以问我{bot_question}。", model=model_name)
        msg = appbuilder.Message({
            "name": "小明",
            "bot_name": "机器人",
            "bot_type": "聊天机器人",
            "bot_function": "聊天",
            "bot_question": "你好吗？"
        })

        answer = self.play.run(message=msg, stream=False, temperature=1)
        self.assertIsNotNone(answer)

    def test_client_run(self):
        app_id = "aa8af334-df27-4855-b3d1-0d249c61fc08"
        builder = appbuilder.AppBuilderClient(app_id)
        conversation_id = builder.create_conversation()
        msg = builder.run(conversation_id, "你可以做什么？")
        respid = builder.upload_local_file(conversation_id, "./data/qa_appbuilder_client_demo.pdf")


if __name__ == '__main__':
    unittest.main()
            

        

    
        