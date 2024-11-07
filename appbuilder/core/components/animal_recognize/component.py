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

"""animal recognize component."""

import base64
import json

from appbuilder.core.component import Component
from appbuilder.core.components.animal_recognize.model import *
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException
from typing import Generator, Union
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace

TOP_NUM = 1
BAIKE_NUM = 0


class AnimalRecognition(Component):
    r"""
       用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出动物识别结果。

       Examples:

       .. code-block:: python

           import appbuilder
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           animal_recognition = appbuilder.AnimalRecognition()
           with open("./animal_recognition_test.png", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

        """
    name = "animal_rec"
    version = "v1"
    manifests = [
        {
            "name": "animal_rec",
            "description": "用于识别图片中动物类别，可识别近八千种动物",
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
        根据输入消息运行动物识别功能
        
        Args:
            message (Message): 输入的消息对象，其中应包含需要识别的图像数据或URL
            timeout (float, optional): 超时时间，单位为秒。默认为None，表示无超时限制。Defaults to None.
            retry (int, optional): 重试次数。默认为0，表示不重试。Defaults to 0.
        
        Returns:
            Message: 识别结果的消息对象
        
        """
        inp = AnimalRecognitionInMsg(**message.content)
        req = AnimalRecognitionRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        req.top_num = 6
        req.baike_num = 0
        result = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = AnimalRecognitionOutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(
        self,
        request: AnimalRecognitionRequest,
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ) -> AnimalRecognitionResponse:
        r"""调用底层接口进行动物识别

                   参数:
                       request (obj: `AnimalRecognitionRequest`) : 动物识别输入参数
                   返回：
                       response (obj: `AnimalRecognitionResponse`): 动物识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")

        data = AnimalRecognitionRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/animal")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        animalRes = AnimalRecognitionResponse.from_json(json.dumps(data))
        animalRes.request_id = request_id
        return animalRes

    @components_run_stream_trace
    def tool_eval(
        self,
        name: str,
        streaming: bool,
        origin_query: str,
        **kwargs,
    ) -> Union[Generator[str, None, None], str]:
        """
        用于工具的执行，通过调用底层接口进行动物识别。
        
        Args:
            name (str): 工具名。
            streaming (bool): 是否流式返回。
            origin_query (str): 用户原始query。
            **kwargs: 工具调用的额外关键字参数。
        
        Returns:
            Union[Generator[str, None, None], str]: 动物识别结果，包括识别出的动物类别和相应的置信度信息。
        """
        traceid = kwargs.get("traceid")
        img_name = kwargs.get("img_name", "")
        img_url = kwargs.get("img_url", "")
        file_urls = kwargs.get("file_urls", {})
        rec_res = self._recognize_w_post_process(img_name, img_url, file_urls, request_id=traceid)
        if streaming:
            yield rec_res
        else:
            return rec_res

    def _recognize_w_post_process(self, img_name, img_url, file_urls, request_id=None) -> str:
        r"""调底层接口对图片或图片url进行动物识别，并返回类别及其置信度
                   参数:
                       img_name (str): 图片文件名
                       img_url (str): 图片url
                       file_urls (dict): 文件名与对应文件url的映射
                   返回：
                       str: 动物识别结果，包括识别出的动物类别和相应的置信度信息
        """
        req = AnimalRecognitionRequest()
        if img_name in file_urls:
            req.url = file_urls[img_name]
        if img_url:
            if img_url in file_urls:
                img_url = file_urls[img_url]
            req.url = img_url
        req.top_num = TOP_NUM
        req.baike_num = BAIKE_NUM
        result = self._recognize(req, request_id=request_id)
        result_dict = proto.Message.to_dict(result)
        rec_res = "模型识别结果为：\n"
        for rec_info in result_dict['result']:
            rec_res += "类别: {} 置信度: {}\n".format(rec_info['name'], rec_info['score'])
        return rec_res

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request_id (str) : 请求ID
                data (dict) : 动物识别body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )
