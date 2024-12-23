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


from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component
from appbuilder.core.components.general_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


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
                    "language_type": {
                        "type": "string",
                        "description": "识别语言类型，'CHN_ENG'为中英文混合，'ENG'为英文， 'JAP'为日语，'KOR'为韩语，'FRE'为法语，'SPA'为西班牙语，'POR'为葡萄牙语，"
                        "'GER'为德语，'ITA'为意大利语，'RUS'为俄语，'DAN'为丹麦语，'DUT'为荷兰语，'MAL'为马来语，'SWE'为瑞典语，'IND'为印尼语，'POL'为波兰语，'ROM'为罗马尼亚语，"
                        "'TUR'为土耳其语，'GRE'为希腊语，'HUN'为匈牙利语，'THA'为泰语，'VIE'为越南语，'ARA'为阿拉伯语，'HIN'为印地语，默认为'CHN_ENG'",
                        "enum": ['CHN_ENG', 'ENG', 'JAP', 'KOR', 'FRE', 'SPA', 'POR', 'GER', 'ITA',
                                 'RUS', 'DAN', 'DUT', 'MAL', 'SWE', 'IND', 'POL', 'ROM', 'TUR', 
                                 'GRE', 'HUN', 'THA', 'VIE', 'ARA', 'HIN'],
                    },
                },
                "anyOf": [
                    {
                        "required": [
                            "img_url",
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
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0, language_type: str = 'CHN_ENG') -> Message:
        """
        在通用文字识别的基础上，提供更高精度的识别服务，支持更多语种识别
        
        Args:
            message (Message): 包含识别任务的输入信息的消息对象。
            timeout (float, optional): 超时时间，单位秒。默认为None，表示不设置超时。
            retry (int, optional): 重试次数。默认为0，表示不重试。
            language_type (str, optional): 识别语言类型，可选值为'CHN_ENG'（中英文）和'CHN'（中文）。默认为'CHN_ENG'。
        
        Returns:
            Message: 包含识别结果的消息对象。
        
        """
        inp = GeneralOCRInMsg(**message.content)
        request = GeneralOCRRequest()
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        if inp.url:
            request.url = inp.url
        request.detect_direction = "true"
        request.language_type = language_type
        result, _ = self._recognize(request, timeout, retry)
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
        return ocr_response, data

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
    def tool_eval(
        self, 
        img_name: str = '',
        img_url: str = '',
        language_type: str = 'CHN_ENG',
        **kwargs
        ):
        """
        对图片中的文字进行识别并返回结果。
        
        Args:
            img_name (str): 图片的文件名。
            img_url (str): 图片的URL地址。
            **kwargs: 其他参数，目前支持以下参数：
                _sys_traceid (str): 系统追踪ID，用于跟踪请求。
                language_type (str): 语言类型，默认为'CHN_ENG'（中英文混合）。
                _sys_file_urls (dict): 文件URL字典，key为文件名，value为文件URL。
                
        Returns:
            Generator: 生成器，每次生成一个包含识别结果的Output对象。
        
        Raises:
            InvalidRequestArgumentError: 如果请求格式错误或文件URL不存在，将抛出此异常。
        
        """
        if not img_name and not img_url:
            raise ValueError(
                "request format error, one of image or url or must pdf_file or ofd_file be set")
        traceid = kwargs.get("_sys_traceid")
        if not img_url:
            file_urls = kwargs.get("_sys_file_urls", {})
            img_path = img_name
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
        req.language_type = language_type
        result_response, raw_data = self._recognize(req, request_id=traceid)
        result = proto.Message.to_dict(result_response)
        results = {
            "识别结果": " \n".join(item["words"] for item in result["words_result"])
        }
        res = json.dumps(results, ensure_ascii=False, indent=4)
        yield self.create_output(type="text", text=res, raw_data=raw_data, visible_scope="llm")
        yield self.create_output(type="text", text="", raw_data=raw_data, visible_scope="user")
