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

r"""图像内容理解"""
import base64
import time

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.image_understand.model import *


class ImageUnderstand(Component):
    r"""
    图像内容理解组件，即对于输入的一张图片（可正常解码，且长宽比适宜）与问题，输出对图片的描述

    Examples:

    .. code-block:: python
       import os
       import appbuilder
       os.environ["GATEWAY_URL"] = "..."
       os.environ["APPBUILDER_TOKEN"] = "..."
       # 从BOS存储读取样例文件
       image_url = "https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bfe25c372b7e56e6"
       # 输入参数为一张图片
      inp = Message(content={"url": image_url, "question": "图片里内容是什么?"})
      # 进行图像内容理解
      image_understand = ImageUnderstand()
      out = image_understand.run(inp)
      # 打印识别结果
      print(out.content)
     """

    @HTTPClient.check_param
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 执行图像内容理解

             参数:
                message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"...", "question": "图片主要内容是什么？"})
                或 Message(content={"url": "https://image/download/url", "question": "图片主要内容是什么？"}).
                timeout (float, 可选): HTTP超时时间
                retry (int, 可选)： HTTP重试次数
              返回:
                 message (obj: `Message`): 模型识别结果.
        """
        inp = ImageUnderstandInMsg(**message.content)
        request = ImageUnderstandRequest()
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        if inp.url:
            request.url = inp.url
        if inp.question == "":
            raise ValueError("question is empty")
        if len(inp.question) > 100:
            raise ValueError("question length biggger then 100")
        request.question = inp.question
        response = self.__recognize(request, timeout, retry)
        out = ImageUnderstandOutMsg(description=response.result.description_to_llm)
        return Message(content=out.dict())

    def __recognize(self, request: ImageUnderstandRequest, timeout: float = None,
                    retry: int = 0) -> ImageUnderstandResponse:
        r"""调用底层接口进行图像内容理解

            参数:
                request (obj: `ImageUnderstandRequest`) : 图像内容理解输入

            返回：
                response (obj: `ImageUnderstandResponse`): 图像内容理解输出
        """
        if not request.image and not request.url:
            raise ValueError("one of image or url must be set")
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        data = ImageUnderstandRequest.to_dict(request)
        headers = self.http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/image-understanding/request")
        response = self.http_client.session.post(url, json=data, timeout=timeout, headers=headers)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__.__check_service_error(request_id, data)
        task = ImageUnderstandTask(data, request_id=request_id)
        task_id = task.result.get("task_id", "")
        if task_id == "":
            raise AppBuilderServerException(request_id=request_id, service_err_message="empty task_id")
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/image-understanding/get-result")
        while True:
            response = self.http_client.session.post(url, json={"task_id": task_id}, timeout=timeout, headers=headers)
            self.http_client.check_response_header(response)
            data = response.json()
            self.http_client.check_response_json(data)
            request_id = self.http_client.response_request_id(response)
            self.__class__.__check_service_error(request_id, data)
            # 处理成功
            response = ImageUnderstandResponse(data)
            if response.result.ret_code == 0:
                return ImageUnderstandResponse(data)
            # 还在处理中
            if response.result.ret_code == 1:
                # 避免触发限流（>1QPS），等待1.1秒
                time.sleep(1.1)

    @staticmethod
    def __check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查

            参数:
                request (dict) : 地标识别body返回
            返回：
                无
        """
        if "ret_code" in data and data["ret_code"] > 1:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("ret_code"),
                service_err_message=data.get("ret_msg")
            )

