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

r"""手写体识别组件"""
import base64

from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.component import Component
from appbuilder.core.components.handwrite_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient

class HandwriteOCR(Component):
    r""" 手写体识别识别
    Examples:

    .. code-block:: python
        import os
        import appbuilder
        os.environ["GATEWAY_URL"] = "..."
        os.environ["APPBUILDER_TOKEN"] = "..."
        # 从BOS存储读取样例文件
        image_url="https://bj.bcebos.com/v1/appbuilder/test_handwrite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b"
        # 输入参数为一张图片
        inp = appbuilder.Message(content={"url": image_url})
        # 进行植物识别
        handwrite_ocr = HandwriteOCR()
        out = handwrite_ocr.run(inp)
        # 打印识别结果
        print(out.content)
     """

    @HTTPClient.check_param
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 输入图片并识别其中的文字

                参数:
                    message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
                       或 Message(content={"url": "https://image/download/url"}).
                       timeout (float, 可选): HTTP超时时间
                       retry (int, 可选)： HTTP重试次数

                 返回:
                    message (obj: `Message`): 手写体模型识别结果.
        """
        inp = HandwriteOCRInMsg(**message.content)
        request = HandwriteOCRRequest()
        if inp.url:
            request.url = inp.url
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        request.recognize_granularity = "big"
        request.probability = "false"
        request.detect_direction = "true"
        request.detect_alteration = "true"
        response = self._recognize(request, timeout, retry)
        out = HandwriteOCROutMsg()
        out.direction = response.direction
        [out.contents.append(
            Content(text=w.words,
                    position=Position(
                        left=w.location.left,
                        top=w.location.top,
                        width=w.location.width,
                        height=w.location.height
                    )))
            for w in response.words_result]
        return Message(content=dict(out))

    def _recognize(self, request: HandwriteOCRRequest, timeout: float = None, retry: int = 0) -> HandwriteOCRResponse:
        r"""调用底层接口进行通用文字识别
                    参数:
                       request (obj: `HandwriteOCRRequest`) : 通用文字识别输入参数

                   返回：
                       response (obj: `HandwriteOCRResponse`): 通用文字识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("one of image or url must be set")
        data = HandwriteOCRRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/handwriting")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        ocr_response = HandwriteOCRResponse(data)
        ocr_response.request_id = request_id
        return ocr_response

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request (dict) : 通用文字识别body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )


