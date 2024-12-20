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

r"""身份证混贴识别组件"""
import base64
import json
from typing import Optional
from appbuilder.core import utils
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component
from appbuilder.core.components.v2.mix_card_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class MixCardOCR(Component):
    r""" 身份证混贴识别组件

    Examples:

    .. code-block:: python

        import os
        import requests
        import appbuilder

        os.environ["GATEWAY_URL"] = "..."
        os.environ["APPBUILDER_TOKEN"] = "..."
        # 从BOS存储读取样例文件
        image_url="https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T06%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe1865e4393da5a3515e90d72d81ef18296bd29598"
        raw_image = requests.get(image_url).content
        # 输入参数为一张图片
        inp = appbuilder.Message(content={"raw_image": raw_image})
        # 进行识别
        mix_card_ocr = MixCardOCR()
        out = mix_card_ocr.run(inp)
        # 打印识别结果
        print(out.content)
     """

    name = "mixcard_ocr"
    version = "v1"
    manifests = [
        {
            "name": "mixcard_ocr",
            "description": "当身份证正反面在同一张图片上，需要识别图片中身份证正反面所有字段时，使用该工具",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "待识别文件的文件名"
                    }
                },
                "required": ["file_names"]
            }
        }
    ]


    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        执行身份证识别操作

        Args:
            message (Message): 包含待识别图片或图片下载URL的Message对象.
                示例: Message(content={"raw_image": b"..."}) 或 Message(content={"url": "https://image/download/url"}).
            timeout (float, 可选): HTTP请求的超时时间，默认为None.
            retry (int, 可选): HTTP请求的重试次数，默认为0.

        Returns:
            Message: 包含身份证识别结果的Message对象.
        """
        inp = MixCardOCRInMsg(**message.content)
        request = MixCardOCRRequest()
        if inp.url:
            request.url = inp.url
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        request.detect_risk = "false"
        request.detect_quality = "false"
        request.detect_photo = "false"
        request.detect_card = "false"
        response = self._recognize(request, timeout, retry)
        out = MixCardOCROutMsg()
        for res in response.words_result:
            card_type = res.card_info.card_type
            if card_type != "idcard_back" and card_type != "idcard_front":
                continue
            ref = out.front
            if card_type == "idcard_back":
                ref = out.back
            loc = res.card_info.card_location
            ref.position = MixCardPosition(
                left=loc.left, top=loc.top, width=loc.width, height=loc.height)
            for key, val in res.card_result.items():
                position = MixCardPosition(left=val.location.left, top=val.location.top, width=val.location.width,
                                           height=val.location.height)
                ref.fields.append(MixCardField(
                    key=key, value=val.words, position=position))
        out.direction = response.direction
        return Message(content=out.model_dump())

    def _recognize(self, request: MixCardOCRRequest, timeout: float = None, retry: int = 0, request_id: str = None) -> MixCardOCRResponse:
        r"""调用底层身份证混贴识别
                参数:
                    request (obj: `GeneralOCRRequest`) : 通用文字识别输入参数

                返回：
                    response (obj: `GeneralOCRResponse`): 通用文字识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError(
                "request format error, one of image or url must be set")
        data = request.model_dump()
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/multi_idcard")
        response = self.http_client.session.post(
            url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        response = MixCardOCRResponse(**data)
        response.request_id = request_id
        return response

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

    @components_run_stream_trace
    def tool_eval(self,
                  file_names: Optional[list] = [],
                  **kwargs):
        """
        对指定文件进行OCR识别。

        Args:
            file_names (Optional[List], optional): 要识别的文件名列表。 
            **kwargs: 其他参数。

        Returns:
            ComponentOutput: 识别结果。

        Raises:
            InvalidRequestArgumentError: 如果请求格式错误，即文件URL不存在时抛出。

        """
        result = {}

        traceid = kwargs.get("_sys_traceid", "")

        sys_file_names = file_names
        if not sys_file_names:
            sys_file_names = kwargs.get("_sys_file_names", [])

        sys_file_urls = kwargs.get("_sys_file_urls", {})

        for file_name in sys_file_names:
            if utils.is_url(file_name):
                file_url = file_name
            else:
                file_url = sys_file_urls.get(file_name, None)
            if file_url is None:
                raise InvalidRequestArgumentError(
                    f"request format error, file {file_name} url does not exist")

            request = MixCardOCRRequest()
            request.url = file_url
            request.detect_risk = "false"
            request.detect_quality = "false"
            request.detect_photo = "false"
            request.detect_card = "false"
            response = self._recognize(request, request_id=traceid)
            out = MixCardOCROutMsg()
            for res in response.words_result:
                card_type = res.card_info.card_type
                if card_type != "idcard_back" and card_type != "idcard_front":
                    continue
                ref = out.front
                if card_type == "idcard_back":
                    ref = out.back
                for key, val in res.card_result.items():
                    ref.fields.append(MixCardField(
                        key=key, value=val.words, position=None))
            out.direction = response.direction
            result[file_name] = out.model_dump()

        result = json.dumps(result, ensure_ascii=False)
        llm_result = self.create_output(
            type="text",
            visible_scope="llm",
            text={"info": result},
            name="llm_text"
        )
        yield llm_result

        user_result = self.create_output(
            type="text",
            visible_scope="user",
            text="",
            name="user_text"
        )
        yield user_result
