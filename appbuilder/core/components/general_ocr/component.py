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

r"""general ocr component."""
import base64
import json
import os.path

from appbuilder.core import utils
from appbuilder.core._client import HTTPClient


from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component
from appbuilder.core.components.general_ocr.model import *
from appbuilder.core.message import Message


class GeneralOCR(Component):
    r"""
    提供通用文字识别能力，在通用文字识别的基础上，提供更高精度的识别服务，支持更多语种识别（丹麦语、荷兰语、马来语、
    瑞典语、印尼语、波兰语、罗马尼亚语、土耳其语、希腊语、匈牙利语、泰语、越语、阿拉伯语、印地语及部分中国少数民族语言），
    并将字库从1w+扩展到2w+，能识别所有常用字和大部分生僻字。

    Examples:

    .. code-block:: python

        import appbuilder

        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'

        general_ocr = appbuilder.GeneralOCR()
        with open("./general_ocr_test.png", "rb") as f:
            out = general_ocr.run(appbuilder.Message(content={"raw_image": f.read()}))
        print(out.content)

     """
    name = "general_ocr"
    version = "v1"

    manifests = [
        {
            "name": "general_ocr",
            "description": "提供更高精度的通用文字识别能力，能够识别图片中的文字，不支持html后缀文件的输入",
            "parameters": {
                "type": "object",
                "properties": {
                    "img_url": {
                        "type": "string",
                        "description": "待识别图片的url,根据该url能够获取图片"
                    },
                    "img_name": {
                        "type": "string",
                        "description": "待识别图片的文件名,用于生成图片url"
                    },
                },
                "anyOf": [
                    {
                        "required": [
                            "img_url"
                        ]
                    },
                    {
                        "required": [
                            "img_name"
                        ]
                    }
                ]
            }
        }
    ]

    @HTTPClient.check_param
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 输入图片并识别其中的文字

                    参数:
                       message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
                       或 Message(content={"url": "https://image/download/url"}).
                       timeout (float, 可选): HTTP超时时间
                       retry (int, 可选)： HTTP重试次数

                     返回: message (obj: `Message`): 模型识别结果. 举例: Message(content={"words_result":[{"words":"100"},
                     {"words":"G8"}]})
        """
        inp = GeneralOCRInMsg(**message.content)
        request = GeneralOCRRequest()
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        if inp.url:
            request.url = inp.url
        request.detect_direction = "true"
        request.language_type = "auto_detect"
        result = self._recognize(request, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = GeneralOCROutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(
        self,
        request: GeneralOCRRequest,
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ) -> GeneralOCRResponse:
        r"""调用底层接口进行通用文字识别
                   参数:
                       request (obj: `GeneralOCRRequest`) : 通用文字识别输入参数

                   返回：
                       response (obj: `GeneralOCRResponse`): 通用文字识别返回结果
               """
        if not request.image and not request.url and not request.pdf_file and not request.ofd_file:
            raise ValueError(
                "request format error, one of image or url or must pdf_file or ofd_file be set")
        data = GeneralOCRRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/accurate_basic")
        response = self.http_client.session.post(
            url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        ocr_response = GeneralOCRResponse.from_json(payload=json.dumps(data))
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

    def tool_eval(self, name: str, streaming: bool, **kwargs):
        """
        general_ocr for function call
        """
        traceid = kwargs.get("traceid")
        img_url = kwargs.get("img_url", None)
        if not img_url:
            file_urls = kwargs.get("file_urls", {})
            img_path = kwargs.get("img_name", None)
            if not img_path:
                raise InvalidRequestArgumentError(
                    "request format error, file name is not set")
            img_name = os.path.basename(img_path)
            img_url = file_urls.get(img_name, None)
            if not img_url:
                raise InvalidRequestArgumentError(
                    f"request format error, file {img_name} url does not exist")
        req = GeneralOCRRequest(url=img_url)
        req.detect_direction = "true"
        req.language_type = "auto_detect"
        result = proto.Message.to_dict(self._recognize(req, request_id=traceid))
        results = {
            "识别结果": " \n".join(item["words"] for item in result["words_result"])
        }
        res = json.dumps(results, ensure_ascii=False, indent=4)
        if streaming:
            yield {
                "type": "text",
                "text": res,
                "visible_scope": 'llm',
            }
            yield {
                "type": "text",
                "text": "",
                "visible_scope": 'user',
            }
        else:
            return res
