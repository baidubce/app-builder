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

r"""Text2Image component.
"""
import time
import math

from typing import Optional
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, RiskInputException
from appbuilder.core.components.text_to_image.model import Text2ImageSubmitRequest, Text2ImageQueryRequest, \
    Text2ImageQueryResponse, Text2ImageSubmitResponse, Text2ImageOutMessage, Text2ImageInMessage
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class Text2Image(Component):
    r"""
    文生图组件，即对于输入的文本，输出生成的图片url。

    Examples:

    .. code-block:: python

        import appbuilder
        text_to_image = appbuilder.Text2Image()
        os.environ["APPBUILDER_TOKEN"] = '...'
        content_data = {"prompt": "上海的经典风景", "width": 1024, "height": 1024, "image_num": 1}
        msg = appbuilder.Message(content_data)
        out = text_to_image.run(inp)
        # 打印生成结果
        print(out.content) # eg: {"img_urls": ["xxx"]}
    """

    manifests = [
        {
            "name": "text_to_image",
            "description": "文生图，该组件只用于图片创作。当用户需要进行场景、人物、海报等内容的绘制时，使用该画图组件。如果用户需要生成图表（柱状图、折线图、雷达图等），则必须使用代码解释器。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "文生图用的query。特别注意，这个字段只能由中文字符组成，不能含有任何英语描述。"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(
        self,
        message: Message,
        width: int = 1024,
        height: int = 1024,
        image_num: int = 1,
        image: Optional[str] = None,
        url: Optional[str] = None,
        pdf_file: Optional[str] = None,
        pdf_file_num: Optional[str] = None,
        change_degree: Optional[int] = None,
        text_content: Optional[str] = None,
        task_time_out: Optional[int]= None,
        text_check: Optional[int] = 1,
        request_id: Optional[str] = None
    ):
        """
        执行文本到图像的生成任务。
        
        Args:
            message (Message): 包含任务相关信息的消息对象。
            width (int, optional): 生成的图像的宽度，默认为1024。
            height (int, optional): 生成的图像的高度，默认为1024。
            image_num (int, optional): 生成图像的数量，默认为1。
            image (Optional[str], optional): 参考图像的路径或URL，默认为None。
            url (Optional[str], optional): 参考图像的URL，默认为None。
            pdf_file (Optional[str], optional): 参考PDF文件的路径，默认为None。
            pdf_file_num (Optional[str], optional): 参考PDF文件中的页码范围，默认为None。
            change_degree (Optional[int], optional): 图像变换的程度，默认为None。
            text_content (Optional[str], optional): 需要转换的文本内容，默认为None。
            task_time_out (Optional[int], optional): 任务超时时间，默认为None。
            text_check (Optional[int], optional): 是否进行文本内容检查，默认为1。
            request_id (Optional[str], optional): 请求的唯一标识，默认为None。
        
        Returns:
            Message: 包含生成图像URL的消息对象。
        
        Raises:
            HTTPError: 请求失败时抛出异常。
        
        """
        headers = self._http_client.auth_header()
        headers["Content-Type"] = "application/json"
        api_url = self._http_client.service_url("/v1/bce/aip/ernievilg/v1/txt2imgv2")

        req = Text2ImageSubmitRequest(
            prompt=message.content["prompt"],  
            width=width,
            height=height,
            image_num=image_num,
            image=image,
            url=url,
            pdf_file=pdf_file,
            pdf_file_num=pdf_file_num,
            change_degree=change_degree,
            text_content=text_content,
            task_time_out=task_time_out,
            text_check=text_check
        )
        response = self.http_client.session.post(api_url, json=req.model_dump(), headers=headers, timeout=None)
        self._http_client.check_response_header(response)
        data = response.json()
        resp= Text2ImageSubmitResponse(**data)

        taskId = resp.data.task_id
        if taskId is not None:
            task_request_time = 1

            while True:
                request = Text2ImageQueryRequest(task_id=taskId)
                text2ImageQueryResponse = self.queryText2ImageData(request, request_id=request_id)
                if text2ImageQueryResponse.data.task_progress is not None:
                    task_progress = float(text2ImageQueryResponse.data.task_progress)
                    if math.isclose(1.0, task_progress, rel_tol=1e-9, abs_tol=0.0):
                        break
                    
                    # NOTE(chengmo)：文生图组件的返回时间在10s以上，查询过于频繁会被限流，导致异常报错
                    # 此处采用 yangyongzhen老师提供的方案，前三次查询间隔3s，后三次查询间隔逐渐增大
                    if task_request_time <= 3:
                        time.sleep(3)
                    else:
                        time.sleep(task_request_time)
                    task_request_time += 1

            img_urls = self.extract_img_urls(text2ImageQueryResponse)
            out = Text2ImageOutMessage(img_urls=img_urls)
            return Message(content=out.model_dump())

    @HTTPClient.check_param
    def submitText2ImageTask(
        self,
        request: Text2ImageSubmitRequest,
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ) -> Text2ImageSubmitResponse:
        """
        使用给定的输入并返回文生图的任务信息。
        
        Args:
            request (obj:`Text2ImageSubmitRequest`): 输入请求，这是一个必需的参数。
            timeout (float, optional): 请求的超时时间。默认为None。
            retry (int, optional): 请求的重试次数。默认为0。
            request_id (str, optional): 请求的唯一标识符。默认为None。
        
        Returns:
            obj:`Text2ImageSubmitResponse`: 接口返回的输出消息。
        
        """
        url = self.http_client.service_url("/v1/bce/aip/ernievilg/v1/txt2imgv2")
        data = request.model_dump()
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/json'
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        response = self.http_client.session.post(url, json=data, headers=headers, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        response = Text2ImageSubmitResponse(**data)
        return response

    def queryText2ImageData(
        self,
        request: Text2ImageQueryRequest,
        timeout: float = None,
        retry: int = 0,
        request_id: str = None,
    ) -> Text2ImageQueryResponse:
        """
        将文本查询请求转换为图像数据。
        
        Args:
            request (Text2ImageQueryRequest): 输入请求，必填参数。
            timeout (float, optional): 请求的超时时间，默认为None。
            retry (int, optional): 请求的重试次数，默认为0。
            request_id (str, optional): 请求的唯一标识符，默认为None。
        
        Returns:
            Text2ImageQueryResponse: 接口返回的输出消息。
        """
        url = self.http_client.service_url("/v1/bce/aip/ernievilg/v1/getImgv2")
        data = {
            "task_id": request.task_id
        }
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/json'
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        response = self.http_client.session.post(url, json=data, headers=headers, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__.check_service_error(request_id, data)
        response = Text2ImageQueryResponse(**data)
        return response

    def extract_img_urls(self, response: Text2ImageQueryResponse):
        """
        从作画生成的返回结果中提取图片url。
        
        Args:
            response (obj:`Text2ImageQueryResponse`): 作画生成的返回结果。
        
        Returns:
            List[str]: 从返回体中提取的图片url列表。
        
        """
        img_urls = []
        if response and response.data and response.data.sub_task_result_list:
            for sub_task_result in response.data.sub_task_result_list:
                if sub_task_result and sub_task_result.final_image_list:
                    for final_image in sub_task_result.final_image_list:
                        if final_image and final_image.img_url:
                            img_urls.append(final_image.img_url)

        return img_urls

    @staticmethod
    def check_service_error(request_id: str, data: dict):
        """
        检查服务错误信息
        
        Args:
            request_id (str): 请求ID
            data (dict): 响应数据
        
        Raises:
            AppBuilderServerException: 如果响应数据中包含错误信息，则抛出异常
        
        Returns:
            None
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )
