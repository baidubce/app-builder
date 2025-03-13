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
import requests
import base64
import unittest
import appbuilder
from appbuilder.core.components.v2 import GeneralOCR
from appbuilder.core.component import ComponentOutput
from appbuilder.core._exception import InvalidRequestArgumentError

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestGeneralOCR(unittest.TestCase):
    def setUp(self) -> None:
        self.com = GeneralOCR()

    def test_run(self):
        img_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                    "857a27513734d765495f89ffa5f73"
        raw_image = requests.get(img_url).content
        image_base64 = base64.b64encode(raw_image)
        message = appbuilder.Message(content={"image_base64": image_base64})
        output = self.com.run(message)
        print(output)

    def test_tool_eval(self):
        img_url = "https://bj.bcebos.com/v1/appbuilder/general_ocr_test.png?" \
                    "authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-" \
                    "11T10%3A59%3A17Z%2F-1%2Fhost%2F081bf7bcccbda5207c82a4de074628b04ae" \
                    "857a27513734d765495f89ffa5f73"
        result = self.com.tool_eval(img_url=img_url, img_name="")
        for res in result:
            assert isinstance(res, ComponentOutput)
            print(res.content)

    def test_error_tool_eval(self):
        result = self.com.tool_eval(img_url='', img_name='')
        with self.assertRaises(InvalidRequestArgumentError):
            list(result)

        result = self.com.tool_eval(img_url='', img_name='test.jpg')
        with self.assertRaises(InvalidRequestArgumentError):
            list(result)

    def test_run_pdf_base64(self):
        pdf_url = "https://bj.bcebos.com/agi-dev-platform-sdk-test/8、质量流量计.pdf"
        raw_pdf = requests.get(pdf_url).content
        pdf_base64 = base64.b64encode(raw_pdf)
        general_ocr = GeneralOCR()
        out = general_ocr.run(appbuilder.Message(content={"pdf_base64": pdf_base64, "pdf_file_num": "3"}))
        self.assertIsInstance(out, appbuilder.Message)

    def test_run_pdf_url(self):
        pdf_url = "https://bj.bcebos.com/agi-dev-platform-sdk-test/8、质量流量计.pdf"
        general_ocr = GeneralOCR()
        out = general_ocr.run(appbuilder.Message(content={"pdf_url": pdf_url, "pdf_file_num": "5"}))
        self.assertIsInstance(out, appbuilder.Message)

    def test_tool_eval_pdf_url(self):
        pdf_url = "https://bj.bcebos.com/agi-dev-platform-sdk-test/8、质量流量计.pdf"
        result = self.com.tool_eval(pdf_url=pdf_url)
        for iter in result:
            self.assertIsInstance(iter, ComponentOutput)

    def test_tool_eval_none_input(self):
        result = self.com.tool_eval(pdf_name="test.pdf")
        with self.assertRaises(InvalidRequestArgumentError):
            list(result)

    def test_rotated_image(self):
        image_url = "https://bj.bcebos.com/agi-dev-platform-sdk-test/8、质量流量计-1_rotated_page-0001.jpg"
        out = self.com.run(appbuilder.Message(content={
            "image_url": image_url, 
            "detect_direction": "true", 
            "multidirectional_recognize": "false"}
        ))
        self.assertIsInstance(out, appbuilder.Message)
    

if __name__ == "__main__":
    unittest.main()
