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
import logging
import requests
import os.path

from typing import Optional


from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component
from appbuilder.core.components.general_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.core.constants import COMPONENT_SUPPORT_FILE_NUMBER
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
                    "img_urls": {
                        "type": "array",
                        "description": "待识别图片的url,根据该url能够获取图片"
                    },
                    "img_names": {
                        "type": "array",
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
                    "pdf_urls": {
                        "type": "array",
                        "description": "待识别pdf的url,根据该url能够获取pdf文件"
                    },
                    "pdf_names": {
                        "type": "array",
                        "description": "待识别pdf的文件名,用于生成pdf url"
                    },
                    "pdf_file_num": {
                        "type": "object",
                        "description": "需要识别的PDF文件的对应页码，key为pdf_names中的文件名，value为对应的页码，当 pdf_file 参数有效时，识别传入页码的对应页面内容，若不传入，则默认识别第 1 页",
                        "additionalProperties": {
                            "type": "string"
                        },
                        "default": {}
                    },
                    "detect_direction": {
                        "type": "string",
                        "description": "是否检测图像朝向,朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括: true-检测朝向; false-不检测朝向"
                        "默认不检测",
                        "default": "false"
                    },
                    "multidirectional_recognize": {
                        "type": "string",
                        "description": "是否开启行级别的多方向文字识别，可选值包括: true-识别, false-不识别; 若图内有不同方向的文字时，建议将此参数设置为“true”"
                        "默认开启",
                        "default": "true"
                    }
                },
                "anyOf": [
                    {
                        "required": [
                            "img_urls",
                        ]
                    },
                    {
                        "required": [
                            "img_names"
                        ]
                    },
                    {
                        "required": [
                            "pdf_urls",
                        ]
                    },
                    {
                        "required": [
                            "pdf_names",
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
        if inp.image_base64:
            request.image = (inp.image_base64)
        elif inp.image_url:
            request.url = inp.image_url
        elif inp.pdf_base64:
            request.pdf_file = inp.pdf_base64
        elif inp.pdf_url:
            raw_pdf = requests.get(inp.pdf_url).content
            pdf_base64 = base64.b64encode(raw_pdf)
            request.pdf_file = pdf_base64
        request.pdf_file_num = inp.pdf_file_num
        request.detect_direction = inp.detect_direction
        request.multidirectional_recognize = inp.multidirectional_recognize
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
        img_names: Optional[list] = [],
        img_urls: Optional[list] = [],
        pdf_names: Optional[list] = [],
        pdf_urls: Optional[list] = [],
        pdf_file_num: Optional[dict] = {},
        language_type: Optional[str] = 'CHN_ENG',
        detect_direction: Optional[str] = "false",
        multidirectional_recognize: Optional[str] = "true",
        **kwargs
        ):
        """
        对图片或PDF文件中的文字进行识别并返回结果。
        
        Args:
            img_names (list): 图片文件名列表，用于指定要识别的图片文件。
            img_urls (list): 图片URL地址列表，用于指定要识别的图片URL。
            pdf_names (list): PDF文件名列表，用于指定要识别的PDF文件。
            pdf_urls (list): PDF URL地址列表，用于指定要识别的PDF URL。
            pdf_file_num (dict): PDF文件页码字典，key为pdf_names中的文件名，value为对应的页码。
                                例如：{"document1.pdf": 1, "document2.pdf": 3} 表示识别document1.pdf的第1页，
                                document2.pdf的第3页。如果未指定页码，默认为第1页。
            language_type (str): 识别语言类型，可选值为'CHN_ENG'（中英文混合）、'ENG'（英文）、
                                'JAP'（日语）、'KOR'（韩语）等，默认为'CHN_ENG'。
            detect_direction (str): 是否检测图像朝向，可选值为'true'（检测）或'false'（不检测），
                                  朝向是指输入图像是正常方向、逆时针旋转90/180/270度，默认为'false'。
            multidirectional_recognize (str): 是否开启行级别的多方向文字识别，可选值为'true'（识别）
                                            或'false'（不识别），若图内有不同方向的文字时，建议将此参数
                                            设置为'true'，默认为'true'。
            
            **kwargs: 其他参数，目前支持以下参数：
                _sys_traceid (str): 系统追踪ID，用于跟踪请求。
                _sys_file_urls (dict): 文件URL字典，key为文件名，value为文件URL。
                
        Returns:
            Generator: 生成器，每次生成一个包含识别结果的Output对象。
                      对于图片文件，返回格式为：{"图片文件名识别结果": "识别的文字内容"}
                      对于PDF文件，返回格式为：{"PDF文件名识别结果": "识别的文字内容"}
        
        Raises:
            InvalidRequestArgumentError: 如果请求格式错误或文件URL不存在，将抛出此异常。
        
        Examples:
            # 识别单个图片
            img_names = ["test.jpg"]
            img_urls = ["http://example.com/test.jpg"]
            
            # 识别多个PDF文件的不同页码
            pdf_names = ["doc1.pdf", "doc2.pdf"]
            pdf_urls = ["http://example.com/doc1.pdf", "http://example.com/doc2.pdf"]
            pdf_file_num = {"doc1.pdf": 1, "doc2.pdf": 3}
            
        """
        traceid = kwargs.get("_sys_traceid", "")
        if not img_names and not img_urls and not pdf_names and not pdf_urls:
            raise InvalidRequestArgumentError(request_id=traceid,
                                                message="img_names\img_urls\pdf_names\pdf_urls can not both be empty")
        sys_file_urls = kwargs.get("_sys_file_urls", {})
        support_pdf_type = ["pdf"]
        support_img_type = ["png", "jpg", "jpeg", "webp", "heic", "tif", "tiff", "dcm", "mha", "nii.gz"]
        img_map = {}
        pdf_map = {}
        unsupported_files = []
        unknown_files = []
        img_names = [os.path.basename(name) for name in img_names]
        pdf_names = [os.path.basename(name) for name in pdf_names]

        for img_name in img_names:
            if len(img_map) >= COMPONENT_SUPPORT_FILE_NUMBER:
                break
            file_type = img_name.split(".")[-1].lower()
            if img_name in sys_file_urls:
                if file_type in support_img_type:
                    img_map[img_name] = sys_file_urls.get(img_name, "")
                else:
                    unsupported_files.append(img_name)
            else:
                unknown_files.append(img_name)

        for pdf_name in pdf_names:
            if len(img_map) + len(pdf_map) >= 10:
                break
            file_type = pdf_name.split(".")[-1].lower()
            if pdf_name in sys_file_urls:
                if file_type in support_pdf_type:
                    pdf_map[pdf_name] = {"url": sys_file_urls.get(pdf_name, ""), "page_num": pdf_file_num.get(pdf_name, "1")}
                else:
                    unsupported_files.append(pdf_name)
            else:
                unknown_files.append(pdf_name)

        for img_url in img_urls:
            if len(img_map) + len(pdf_map) >= 10:
                break
            if img_url in list(sys_file_urls.values()):
                continue
            file_name = img_url.split("/")[-1].split("?")[0]
            file_type = file_name.split(".")[-1].lower()
            if file_type in support_img_type:
                img_map[img_url] = img_url 
            else:
                unsupported_files.append(img_url)

        for pdf_url in pdf_urls:
            if len(img_map) + len(pdf_map) >= 10:
                break
            if pdf_url in list(sys_file_urls.values()):
                continue
            file_name = pdf_url.split("/")[-1].split("?")[0]
            file_type = file_name.split(".")[-1].lower()
            if file_type in support_pdf_type:
                pdf_map[pdf_url] = {"url": pdf_url, "page_num": pdf_file_num.get(file_name, "1")}
            else:
                unsupported_files.append(pdf_url)

        if not img_map and not pdf_map:
            raise InvalidRequestArgumentError(
                f"request format error, file url does not exist")

        if img_map:
            for img_name, img_url in img_map.items():
                try:
                    req = GeneralOCRRequest(url=img_url)
                    req.detect_direction = detect_direction
                    req.language_type = language_type
                    req.multidirectional_recognize = multidirectional_recognize
                    result_response, raw_data = self._recognize(req, request_id=traceid)
                    result = proto.Message.to_dict(result_response)
                    results = {
                        f"{img_name}": " \n".join(item["words"] for item in result["words_result"])
                    }
                    res = json.dumps(results, ensure_ascii=False)
                    yield self.create_output(type="text", text=res, raw_data=raw_data, visible_scope="llm")
                    yield self.create_output(type="text", text="", raw_data=raw_data, visible_scope="user")
                except Exception as e:
                    logging.warning(f"{img_name} ocr failed with exception: {e}")
                    continue

        if pdf_map:
            for pdf_name, pdf_info in pdf_map.items():
                try:
                    pdf_url = pdf_info.get("url", None)
                    pdf_file_num = pdf_info.get("page_num", "1")
                    raw_pdf = requests.get(pdf_url).content
                    pdf_base64 = base64.b64encode(raw_pdf)
                    req = GeneralOCRRequest(pdf_file=pdf_base64, pdf_file_num=pdf_file_num)
                    req.detect_direction = detect_direction
                    req.language_type = language_type
                    req.multidirectional_recognize = multidirectional_recognize
                    result_response, raw_data = self._recognize(req, request_id=traceid)
                    result = proto.Message.to_dict(result_response)
                    results = {
                        f"{pdf_name}": " \n".join(item["words"] for item in result["words_result"])
                    }
                    res = json.dumps(results, ensure_ascii=False)
                    yield self.create_output(type="text", text=res, raw_data=raw_data, visible_scope="llm")
                    yield self.create_output(type="text", text="", raw_data=raw_data, visible_scope="user")
                except Exception as e:
                    logging.warning(f"{pdf_name} ocr failed with exception: {e}")
                    continue
        
        for file_name in unknown_files:
            results = {
                f"{file_name}": "无法获取url，请确认是否上传成功"
            }
            res = json.dumps(results, ensure_ascii=False)
            llm_result = self.create_output(
                type = "text",
                visible_scope= "llm",
                text=res,
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
        
        for file_name in unsupported_files:
            results = {
                f"{file_name}": "不支持的文件类型，请确认是否为图片或者pdf文件"
            }
            res = json.dumps(results, ensure_ascii=False)
            llm_result = self.create_output(
                type = "text",
                visible_scope= "llm",
                text=res,
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
