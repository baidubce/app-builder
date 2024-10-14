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

r"""图像内容理解"""
import base64
import time

from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.image_understand.model import *
from typing import Generator, Union
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class ImageUnderstand(Component):
    r"""
    图像内容理解组件，即对于输入的一张图片（可正常解码，且长宽比适宜）与问题，输出对图片的描述

    Examples:

    .. code-block:: python
    
       import os
       import appbuilder
       os.environ["GATEWAY_URL"] = "..."
       os.environ["APPBUILDER_TOKEN"] = "..."
       # 从BOS存储读取样例文件
       image_url = "https://bj.bcebos.com/v1/appbuilder/test_image_understand.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T09%3A41%3A01Z%2F-1%2Fhost%2Fe8665506e30e0edaec4f1cc84a2507c4cb3fdb9b769de3a5bfe25c372b7e56e6"
       # 输入参数为一张图片
       inp = Message(content={"url": image_url, "question": "图片里内容是什么?"})
       # 进行图像内容理解
       image_understand = ImageUnderstand()
       out = image_understand.run(inp)
       # 打印识别结果
       print(out.content)
     """
    name = "image_understanding"
    version = "v1"
    manifests = [
        {
            "name": "image_understanding",
            "description": "可对输入图片进行理解，可输出图片描述、OCR 及图像识别结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "img_name": {
                        "type": "string",
                        "description": "待识别图片的文件名"
                    },
                    "img_url": {
                        "type": "string",
                        "description": "待识别图片的url"
                    }
                },
                "anyOf": [
                    {
                        "required": [
                            "img_name"
                        ]
                    },
                    {
                        "required": [
                            "img_url"
                        ]
                    }
                ]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        执行图像内容理解
        
        Args:
            message (Message): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"...", "question": "图片主要内容是什么？"})
                              或 Message(content={"url": "https://image/download/url", "question": "图片主要内容是什么？"}).
            timeout (float, optional): HTTP超时时间. 默认为 None.
            retry (int, optional): HTTP重试次数. 默认为 0.
        
        Returns:
            Message: 模型识别结果.
        
        """
        inp = ImageUnderstandInMsg(**message.content)
        request = ImageUnderstandRequest()
        # 兼容新参数，确保输出结果一致
        request.subject_detect = False
        request.llm_switch = False
        if inp.raw_image:
            request.image = base64.b64encode(inp.raw_image)
        if inp.url:
            request.url = inp.url
        if inp.question == "":
            raise ValueError("request format error, question is empty")
        if len(inp.question) > 100:
            raise ValueError(f"request format error, expected len(question)>100, got {len(inp.question)}")
        if inp.language != "zh-CN" and inp.language != "en":
            raise ValueError(f"request format error, expected language in ['zh-CN', 'en'], got {inp.language}")
        request.question = inp.question
        request.output_CHN = True
        if inp.language == "en":
            request.output_CHN = False
        response = self.__recognize(request, timeout, retry)
        out = ImageUnderstandOutMsg(description=response.result.description_to_llm)
        return Message(content=out.model_dump())

    def __recognize(
        self, 
        request: ImageUnderstandRequest, 
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ) -> ImageUnderstandResponse:
        r"""调用底层接口进行图像内容理解

            参数:
                request (obj: `ImageUnderstandRequest`) : 图像内容理解输入

            返回：
                response (obj: `ImageUnderstandResponse`): 图像内容理解输出
        """
        if not request.image and not request.url:
            raise ValueError("request format error, one of image or url must be set")
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        data = ImageUnderstandRequest.to_dict(request)
        headers = self.http_client.auth_header(request_id)
        headers['Content-Type'] = 'application/json'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/image-understanding/request")
        response = self.http_client.session.post(url, json=data, timeout=timeout, headers=headers)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__.__check_create_task_service_error(request_id, data)
        task = ImageUnderstandTask(data, request_id=request_id)
        task_id = task.result.get("task_id", "")
        if task_id == "":
            raise AppBuilderServerException(request_id=request_id, service_err_message="empty task_id")
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/image-understanding/get-result")
        while True:
            response = self.http_client.session.post(url, json={"task_id": task_id}, timeout=timeout, headers=headers)
            self.http_client.check_response_header(response)
            data = response.json()
            self.http_client.check_response_json(data)
            request_id = self.http_client.response_request_id(response)
            self.__class__.__check_service_error(request_id, data.get("result", {}))
            # 处理成功
            response = ImageUnderstandResponse(data)
            if response.result.ret_code == 0:
                return ImageUnderstandResponse(data)
            # 还在处理中
            if response.result.ret_code == 1:
                # 避免触发限流（>1QPS），等待1.1秒
                time.sleep(1.1)

    @components_run_stream_trace
    def tool_eval(
        self,
        name: str,
        streaming: bool,
        origin_query: str,
        **kwargs,
    ) -> Union[Generator[str, None, None], str]:
        """
        用于工具的执行，调用底层接口进行图像内容理解
        
        Args:
            name (str): 工具名
            streaming (bool): 是否流式返回
            origin_query (str): 用户原始query
            **kwargs: 工具调用的额外关键字参数
        
        Returns:
            Union[Generator[str, None, None], str]: 图片内容理解结果
        """
        traceid = kwargs.get("traceid")
        img_name = kwargs.get("img_name", "")
        img_url = kwargs.get("img_url", "")
        file_urls = kwargs.get("file_urls", {})
        rec_res = self._recognize_w_post_process(img_name, img_url, file_urls, request_id=traceid)
        if streaming:
            yield {
                "type": "text",
                "text": rec_res,
                "visible_scope": 'llm',
            }
            yield {
                "type": "text",
                "text": "",
                "visible_scope": 'user',
            }
        else:
            return rec_res

    def _recognize_w_post_process(
        self,
        img_name,
        img_url,
        file_urls,
        question="图片内容有哪些",
        request_id=None,
    ) -> str:
        r"""
            参数:
                img_name (str): 图片文件名
                img_url (bool): 图片url
                question (str): 询问有关图片内容的问题
                file_urls (dict): 文件名与对应文件url的映射

            返回：
                str: 图片内容理解结果
        """
        req = ImageUnderstandRequest()
        # 兼容新参数，确保输出结果一致
        req.subject_detect = False
        req.llm_switch = False
        req.question = question
        if img_name in file_urls:
            req.url = file_urls[img_name]
        if img_url:
            if img_url in file_urls:
                img_url = file_urls[img_url]
            req.url = img_url
        response = self.__recognize(req, request_id=request_id)
        description_to_llm = response.result.description_to_llm
        description_processed = description_to_llm.rsplit("。", 2)[0]
        return description_processed

    @staticmethod
    def __check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查

            参数:
                request (dict) : 图像内容理解body返回
            返回：
                无
        """
        ret_code = data.get("ret_code", 0)
        if ret_code != 0 and ret_code != 1:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("ret_code", ""),
                service_err_message=data.get("ret_msg", "")
            )

    @staticmethod
    def __check_create_task_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request_id (str) : 任务请求ID
                data (dict): 响应数据
            返回：
                无
        """

        if "error_code" in data and "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code", ""),
                service_err_message=data.get("error_msg", "")
            )





