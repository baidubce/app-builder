
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


# -*- coding: utf-8 -*-
"""
菜品识别组件.
"""
import base64

from appbuilder.core.message import Message
from appbuilder.core.component import Component
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.dish_recognize.model import *
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class DishRecognition(Component):
    """
    菜品识别组件，适用于识别只含有单个菜品的图片，返回识别的菜品名称和卡路里信息
    
    Examples:

    .. code-block:: python

        import appbuilder

        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'

        dish_recognition = appbuilder.DishRecognition()

        with open("xxxx.jpg", "rb") as f:
            resp = dish_recognition(appbuilder.Message({"raw_image": f.read()}))
            # 输出示例 {'result': [{'name': '剁椒鱼头', 'calorie': '127'}]}
            print(resp.content)
    """

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        根据输入图片进行菜品识别。

        Args:
            message (Message): 输入待识别图片，支持传图片二进制流和图片URL。
            timeout (float, optional): 请求超时时间，默认为 None。
            retry (int, optional): 重试次数，默认为 0。

        Returns:
            Message: 包含菜品识别结果的输出消息。例如，Message(content={'result': [{'name': '剁椒鱼头', 'calorie': '127'}]})

        """
        inp = DishRecognitionInMsg(**message.content)
        req = DishRecognitionRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        result = self._recognize(req, timeout=timeout, retry=retry)
        result_dict = proto.Message.to_dict(result)
        out = DishRecognitionOutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(self, request: DishRecognitionRequest, timeout: float = None,
                   retry: int = 0) -> DishRecognitionResponse:
        """
        发起食物识别请求并返回识别结果。

        :param request: 包含执行识别所需信息的 DishRecognitionRequest 对象。
        :param timeout: 请求超时时间（秒），默认为 None。
        :param retry: 请求失败时的重试次数，默认为 0。
        :return: 包含食物识别结果的响应对象。
        """
        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")
        if not request.top_num:
            request.top_num = 1
        if not request.filter_threshold:
            request.filter_threshold = 0.95
        request_data = DishRecognitionRequest.to_dict(request)
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'

        url = self.http_client.service_url("/v1/bce/aip/image-classify/v2/dish")
        response = self.http_client.session.post(url, headers=headers, data=request_data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        if "error_code" in data and "error_msg" in data:
            raise AppBuilderServerException(request_id=request_id, service_err_code=data["error_code"], service_err_message=data["error_msg"])
        return DishRecognitionResponse(data)
