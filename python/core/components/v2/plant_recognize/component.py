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
from typing import Generator, Union
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from appbuilder.core.components.plant_recognize.model import TOP_NUM, BAIKE_NUM



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
    name = "plant_rec"
    version = "v1"
    manifests = [
        {
            "name": "plant_rec",
            "description": "用于识别图片中植物类别",
            "parameters": {
                "type": "object",
                "properties": {
                    "img_name": {
                        "type": "string",
                        "description": "待识别图片的文件名"
                    },
                    "img_url": {
                        "type": "string",
                        "description": "待识别图片的url"
                    }
                },
                "anyOf": [
                    {
                        "required": [
                            "img_name"
                        ]
                    },
                    {
                        "required": [
                            "img_url"
                        ]
                    }
                ]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        输入图片并识别其中的植物
        
        Args:
            message (Message): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
            或 Message(content={"url": "https://image/download/uel"}).
            timeout (float, optional): HTTP超时时间，默认为None
            retry (int, optional): HTTP重试次数，默认为0
        
        Returns:
            Message: 模型识别结果
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

    def __recognize(
        self,
        request: PlantRecognitionRequest,
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ) -> PlantRecognitionResponse:
        r"""调用底层接口植物识别

            参数:
                request (obj: `PlantRecognitionRequest`) : 植物识别输入参数

            返回：
                response (obj: `PlantRecognitionResponse`): 植物识别返回结果
        """
        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")
        data = PlantRecognitionRequest.to_dict(request)
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/plant")
        response = self.http_client.session.post(url, data=data, timeout=timeout, headers=headers)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__.__check_service_error(request_id, data)
        return PlantRecognitionResponse(data, request_id=request_id)

    @components_run_stream_trace
    def tool_eval(
        self,
        img_name: str = "",
        img_url: str = "",
        **kwargs,
    ) -> Union[Generator[str, None, None], str]:
        """
        用于工具的执行，通过调用底层接口进行植物识别
        
        Args:
            name (str): 工具名
            streaming (bool): 是否流式返回
            origin_query (str): 用户原始query
            **kwargs: 工具调用的额外关键字参数
        
        Returns:
            Union[Generator[str, None, None], str]: 植物识别结果，包括识别出的植物类别和相应的置信度信息
        """
        traceid = kwargs.get("_sys_traceid", "")
        file_urls = kwargs.get("_sys_file_urls", {})
        rec_res = self._recognize_w_post_process(img_name, img_url, file_urls, request_id=traceid)

        rec_res = self.create_output(
            type="text",
            text=rec_res,
        )
        yield rec_res

    def _recognize_w_post_process(self, img_name, img_url, file_urls, request_id=None):
        r"""调底层接口对图片或图片url进行植物识别，并返回类别及其置信度
            参数:
               img_name (str): 图片文件名
               img_url (str): 图片url
               file_urls (dict): 文件名与对应文件url的映射
            返回：
               str: 植物识别结果，包括识别出的动物类别和相应的置信度信息
         """
        req = PlantRecognitionRequest()
        if img_name in file_urls:
            req.url = file_urls[img_name]
        if img_url:
            if img_url in file_urls:
                img_url = file_urls[img_url]
            req.url = img_url
        req.top_num = TOP_NUM
        req.baike_num = BAIKE_NUM
        result = self.__recognize(req, request_id=request_id)
        result_dict = proto.Message.to_dict(result)
        rec_res = "模型识别结果为：\n"
        for rec_info in result_dict['result']:
            rec_res += "类别: {} 置信度: {}\n".format(rec_info['name'], rec_info['score'])
        return rec_res

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


