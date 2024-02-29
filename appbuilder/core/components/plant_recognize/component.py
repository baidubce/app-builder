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

r"""植物识别组件"""
import base64

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.plant_recognize.model import *


class PlantRecognition(Component):
    r"""
    植物识别组件，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的植物识别结果

    Examples:

    .. code-block:: python
        import os
        import requests
        import appbuilder

        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
        image_url = "https://bj.bcebos.com/v1/appbuilder/palnt_recognize_test.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T09%3A51%3A03Z%2F-1%2Fhost%2Faa2217067f78f0236c8262cdd89a4b4f4b2188d971ca547c53d01742af4a2cbe"

        # 从BOS存储读取样例文件
        raw_image = requests.get(image_url).content
        inp = appbuilder.Message(content={"raw_image": raw_image})
        # inp = Message(content={"url": image_url})

        # 运行植物识别
        plant_recognize = appbuilder.PlantRecognition()
        out = plant_recognize.run(inp)
        # 打印识别结果
        print(out.content)
     """

    @HTTPClient.check_param
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 输入图片并识别其中的植物

             参数:
                message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
                或 Message(content={"url": "https://image/download/uel"}).
                timeout (float, 可选): HTTP超时时间
                retry (int, 可选)： HTTP重试次数

              返回:
                 message (obj: `Message`): 模型识别结果.
        """
        inp = PlantRecognitionInMsg(**message.content)
        request = PlantRecognitionRequest()
        if inp.url:
            request.url = inp.url
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        request.top_num = 5
        request.baike_num = 0
        response = self.__recognize(request, timeout, retry)
        plant_score_list = []
        [plant_score_list.append(PlantScore(name=plant.name, score=plant.score)) for plant in response.result]
        out = PlantRecognitionOutMsg(plant_score_list=plant_score_list)
        return Message(content=out.model_dump())

    def __recognize(self, request: PlantRecognitionRequest, timeout: float = None, retry: int = 0) \
            -> PlantRecognitionResponse:
        r"""调用底层接口植物识别

            参数:
                request (obj: `PlantRecognitionRequest`) : 植物识别输入参数

            返回：
                response (obj: `PlantRecognitionResponse`): 植物识别返回结果
        """
        if not request.image and not request.url:
            raise ValueError("one of image or url must be set")
        data = PlantRecognitionRequest.to_dict(request)
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/plant")
        response = self.http_client.session.post(url, data=data, timeout=timeout, headers=headers)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__.__check_service_error(request_id, data)
        return PlantRecognitionResponse(data, request_id=request_id)

    @staticmethod
    def __check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查

            参数:
                request (dict) : 地标识别body返回
            返回：
                无
        """

        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )


