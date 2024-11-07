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

"""doc_crop_enhance component."""

import base64
import json

from appbuilder.core.component import Component
from appbuilder.core._client import HTTPClient
from appbuilder.core.components.doc_crop_enhance.model import *
from appbuilder.core.message import Message
from appbuilder.core._exception import *
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace

enhance_type_set = [0, 1, 2, 3]


class DocCropEnhance(Component):
    r"""
       对图片中的文件、卡证、票据等内容进行四角点检测定位，提取主体内容并对其进行矫正，同时可选图片增强效果进一步提升图片清晰度，
       达到主体检测矫正并增强的目的，提升图片整体质量

       Examples:

       .. code-block:: python

           import appbuilder

           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           doc_crop_enhance = appbuilder.DocCropEnhance()
           with open("./doc_enhance_test.png", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

    """
    
    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, enhance_type: int = 0, timeout: float = None, retry: int = 0) -> Message:
        r"""
        文档矫正增强
        
        Args:
            message (Message): 输入图片或图片url下载地址用于执行操作。举例: Message(content={"raw_image": b"...",
            "enhance_type": 3})或 Message(content={"url": "https://image/download/url"})。
            enhance_type (int, 可选): 选择是否开启图像增强功能，如开启可选择增强效果，可选值如下：
                - 0：默认值，不开启增强功能
                - 1：去阴影
                - 2：增强并锐化
                - 3：黑白滤镜。
            timeout (float, 可选): HTTP超时时间
            retry (int, 可选): HTTP重试次数
        
        Returns:
            Message: 识别结果。举例: Message(name=msg, content={'image_processed': '...',
            'points': [{'x': 220, 'y': 705}, {'x': 240, 'y': 0}, {'x': 885, 'y': 2}, {'x': 980, 'y': 759}]},
            mtype=dict)
        """
        inp = DocCropEnhanceInMsg(**message.content)
        req = DocCropEnhanceRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        req.scan_type = 3
        if enhance_type not in enhance_type_set:
            raise InvalidRequestArgumentError(f"mismatched argument enhance_type, expected enhance_type in {enhance_type_set}")
        req.enhance_type = enhance_type
        result = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = DocCropEnhanceOutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(self, request: DocCropEnhanceRequest, timeout: float = None,
                   retry: int = 0) -> DocCropEnhanceResponse:
        r"""文档矫正增强调用
                   参数:
                       request (obj: `DocCropEnhanceRequest`) : 文档矫正增强输入参数
                   返回：
                       response (obj: `DocCropEnhanceResponse`): 文档矫正增强返回结果
               """
        if not request.image and not request.url:
            raise ValueError("request argument error, one of image or url must be set")

        req = json.dumps(DocCropEnhanceRequest.to_dict(request))
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/json'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/doc_crop_enhance")
        response = self.http_client.session.post(url, headers=headers, data=req, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        res = DocCropEnhanceResponse.from_json(json.dumps(data))
        res.request_id = request_id
        return res

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request (dict) : 文档矫正增强body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )
