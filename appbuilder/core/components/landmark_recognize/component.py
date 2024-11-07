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

r"""landmark recognize component."""
import base64

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.landmark_recognize.model import *
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class LandmarkRecognition(Component):
    r"""
    识别地标组件，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的地标识别结果

    Examples:

    .. code-block:: python

        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = '...'
        landmark_recognize = appbuilder.LandmarkRecognition()
        with open("xxxx.jpg", "rb") as f:
            inp = appbuilder.Message(content={"raw_image": f.read()})
            out = landmark_recognize.run(inp)
            # 打印识别结果
            print(out.content) # eg: {"landmark": "狮身人面相"}
     """

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        执行地标识别任务
        
        Args:
            message (Message): 输入消息对象，包含待识别的图片或图片URL。
                例如：Message(content={"raw_image": b"..."}) 或 Message(content={"url": "https://image/download/url"})。
            timeout (float, optional): HTTP请求的超时时间。默认为None。
            retry (int, optional): HTTP请求的重试次数。默认为0。
        
        Returns:
            Message: 地标识别结果的消息对象。
                例如：Message(content={"landmark": b"狮身人面像"})
        """
        inp = LandmarkRecognitionInMsg(**message.content)
        request = LandmarkRecognitionRequest()
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        if inp.url:
            request.url = inp.url
        response = self.__recognize(request, timeout, retry)
        out = LandmarkRecognitionOutMsg(landmark=response.result.get("landmark", ""))
        return Message(content=out.model_dump())

    def __recognize(self, request: LandmarkRecognitionRequest, timeout: float = None,
                    retry: int = 0) -> LandmarkRecognitionResponse:
        r"""调用底层接口进行地标识别

            参数:
                request (obj: `LandmarkRecognitionRequest`) : 地标识别输入参数

            返回：
                response (obj: `LandmarkRecognitionResponse`): 地标识别返回结果
        """

        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")
        data = LandmarkRecognitionRequest.to_dict(request)
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/landmark")
        response = self.http_client.session.post(url, data=data, timeout=timeout, headers=headers)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__.__check_service_error(request_id, data)
        return LandmarkRecognitionResponse(data, request_id=request_id)

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


