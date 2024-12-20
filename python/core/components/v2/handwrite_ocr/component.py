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

r"""手写文字识别组件"""
import base64
from typing import Optional
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component
from appbuilder.core.components.v2.handwrite_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core import utils
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace

class HandwriteOCR(Component):
    r""" 手写文字识别组件
    
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

    name = "handwriting_ocr"
    version = "v1"
    manifests = [
        {
            "name": "handwriting_ocr",
            "description": "需要对图片中手写体文字进行识别时，使用该工具，不支持PDF文件，如果用户没有提供图片文件，应引导用户提供图片，而不是尝试使用该工具",
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
        r"""
        输入图片并识别其中的文字
        
        Args:
            message (Message): 输入图片或图片url下载地址用于执行识别操作.例如: Message(content={"raw_image": b"..."}) 或 Message(content={"url": "https://image/download/url"}).
            timeout (float, optional): HTTP超时时间. 默认为None.
            retry (int, optional): HTTP重试次数. 默认为0.
        
        Returns:
            Message: 手写体模型识别结果.
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
        return Message(content=out.model_dump())

    @components_run_stream_trace
    def tool_eval(self,
                  file_names: Optional[list] = [],
                  **kwargs):
        """
        工具评估函数
        Args:
            file_names (Optional[list]): 待识别文件的文件名列表
            **kwargs: 其他参数
        
        Raises:
            InvalidRequestArgumentError: 请求格式错误，文件url不存在
        
        Yields:
            Generator[Output]: 生成器，每次迭代产生一个输出对象
        """
        traceid = kwargs.get("_sys_traceid", "")
        result = ""
        
        sys_file_names = file_names
        if not sys_file_names:
            sys_file_names = kwargs.get('_sys_file_names', [])

        sys_file_urls = kwargs.get('_sys_file_urls', {})

        for file_name in sys_file_names:
            if utils.is_url(file_name):
                file_url = file_name
            else:
                file_url = sys_file_urls.get(file_name, None)
            if file_url is None:
                raise InvalidRequestArgumentError(f"request format error, file {file_name} url does not exist")
            req = HandwriteOCRRequest()
            req.url = file_url
            req.recognize_granularity = "big"
            req.probability = "false"
            req.detect_direction = "true"
            req.detect_alteration = "true"
            response = self._recognize(req, request_id=traceid)
            text = "".join([w.words for w in response.words_result])
            result += f"{file_name}的手写识别结果是：{text} "

        llm_result = self.create_output(
            type = "text",
            visible_scope= "llm",
            text=result,
            name="llm_text"
        )
        yield llm_result

        user_result = self.create_output(
            type = "text",
            visible_scope= "user",
            text="",
            name="user_text"
        )
        yield user_result


    def _recognize(
        self, 
        request: HandwriteOCRRequest, 
        timeout: float = None, 
        retry: int = 0,
        request_id: str = None,
    ) -> HandwriteOCRResponse:
        r"""调用底层接口进行通用文字识别
                    参数:
                       request (obj: `HandwriteOCRRequest`) : 通用文字识别输入参数

                   返回：
                       response (obj: `HandwriteOCRResponse`): 通用文字识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")
        data = request.model_dump()
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/handwriting")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        ocr_response = HandwriteOCRResponse(**data)
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

