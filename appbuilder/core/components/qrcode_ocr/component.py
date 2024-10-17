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

"""qrcode ocr component."""

import base64
import json

from appbuilder.core import utils
from appbuilder.core.component import Component
from appbuilder.core.components.qrcode_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class QRcodeOCR(Component):
    r"""
       对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息。


       Examples:

       .. code-block:: python

           import appbuilder
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           qrcode_ocr = appbuilder.QRcodeOCR()
           with open("./qrcode_ocr_test.png", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read(),"location": "true"}))
           print(out.content)

        """

    name = "qrcode_ocr"
    version = "v1"
    manifests = [
        {
            "name": "qrcode_ocr",
            "description": "需要对图片中的二维码、条形码进行检测和识别，返回存储的文字信息及其位置信息，使用该工具",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "待识别文件的文件名"
                    },
                    "location": {
                        "type": "string",
                        "description": "是否输出二维码/条形码位置信息"
                    }
                },
                "required": ["file_names"]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, location: str = "true", timeout: float = None, retry: int = 0) -> Message:
        """
        执行二维码识别操作。
        
        Args:
            message (Message): 输入的图片或图片URL下载地址，用于执行识别操作。例如：
                Message(content={"raw_image": b"...", "location": ""}) 或
                Message(content={"url": "https://image/download/url"})。
            location (str, 可选): 是否需要返回二维码位置信息，默认为 "true"。
            timeout (float, 可选): HTTP请求的超时时间。
            retry (int, 可选): HTTP请求的重试次数。
        
        Returns:
            Message: 识别结果，包含识别到的二维码信息。例如：
                Message(name=msg, content={'codes_result': [{'type': 'QR_CODE', 'text': ['http://weixin.qq.com/r/cS7M1PHE5qyZrbW393tj'],
                    'location': {'top': 63, 'left': 950, 'width': 220, 'height': 211}}, ...]}, mtype=dict)
        
        Raises:
            InvalidRequestArgumentError: 如果 location 参数非法，将抛出该异常。
        """
        inp = QRcodeInMsg(**message.content)
        req = QRcodeRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        if not isinstance(location, str) or location not in ('true', 'false'):
            raise InvalidRequestArgumentError(
                f"illegal location, expected location is 'true' or 'false', got {location}")
        req.location = location
        result = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = QRcodeOutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(self, request: QRcodeRequest, timeout: float = None,
                   retry: int = 0, request_id: str = None) -> QRcodeResponse:
        r"""调用二维码识别底层能力
                   参数:
                       request (obj: `QRcodeRequest`) : 二维码识别输入参数
                   返回：
                       response (obj: `QRcodeResponse`): 二维码识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError(
                "request format error, one of image or url must be set")

        data = QRcodeRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = 'application/json'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/qrcode")
        response = self.http_client.session.post(
            url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        res = QRcodeResponse.from_json(json.dumps(data))
        res.request_id = request_id
        return res

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request (dict) : 二维码识别body返回
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
    def tool_eval(self, name: str, streaming: bool, **kwargs):
        """
        评估工具函数
        
        Args:
            name (str): 工具名称
            streaming (bool): 是否流式输出
            **kwargs: 其他关键字参数
        
        Keyword Args:
            traceid (str): 请求的traceid
            file_names (List[str]): 文件名列表
            locations (str): 是否需要获取位置信息，可选值为'true'或'false'，默认为'false'
            file_urls (Dict[str, str]): 文件名到文件URL的映射
        
        Returns:
            Union[str, Generator[Dict[str, Any], None, None]]: 如果streaming为True，则返回一个生成器，生成两个字典，分别代表LLM和用户可见的内容；
                                                              如果streaming为False，则返回一个JSON字符串，包含评估结果
        
        Raises:
            InvalidRequestArgumentError: 如果请求格式错误，或者位置信息不合法，则抛出该异常
        """
        result = {}
        traceid = kwargs.get("traceid")
        file_names = kwargs.get("file_names", None)
        location = kwargs.get("locations", "false")
        if not file_names:
            file_names = kwargs.get("files")

        file_urls = kwargs.get("file_urls", {})
        for file_name in file_names:
            if utils.is_url(file_name):
                file_url = file_name
            else:
                file_url = file_urls.get(file_name, None)
            if file_url is None:
                raise InvalidRequestArgumentError(
                    f"request format error, file {file_name} url does not exist")
            req = QRcodeRequest()
            req.url = file_url
            if not isinstance(location, str) or location not in ("true", "false"):
                raise InvalidRequestArgumentError(
                    f"illegal location, expected location is 'true' or 'false', got {location}"
                )
            req.location = location
            resp = self._recognize(req, request_id=traceid)
            result[file_name] = [
                item["text"] for item in proto.Message.to_dict(resp).get("codes_result", [])
            ]

        result = json.dumps(result, ensure_ascii=False)
        if streaming:
            yield {
                "type": "text",
                "text": result,
                "visible_scope": 'llm',
            }
            yield {
                "type": "text",
                "text": "",
                "visible_scope": "user",
            }
        else:
            return result
