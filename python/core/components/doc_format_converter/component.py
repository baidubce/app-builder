# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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


# -*- coding: utf-8 -*-
"""
文档格式转换
"""
import os
import json
import base64
from typing import Dict, Any
import time

import requests

from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.core.component import Component, Message
from appbuilder.core._client import HTTPClient
from appbuilder.core.components.doc_format_converter.model import DocFormatConverterInMessage, \
                        DocFormatConverterOutMessage, \
                        DocFormatConverterSubmitRequest, DocFormatConverterSubmitResponse, \
                        DocFormatConverterQueryRequest, DocFormatConverterQueryResponse
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class DocFormatConverter(Component):
    r"""
    可识别图片/PDF文档版面布局，提取文字内容，并转换为保留原文档版式的Word、Excel文档，方便二次编辑和复制，
    可支持含表格、印章、水印、手写等内容的文档。满足文档格式转换、企业档案电子化等信息管理需求。

    Examples:

       .. code-block:: python

           import appbuilder
           # 请前往千帆AppBuilder官网创建密钥
           os.environ["APPBUILDER_TOKEN"] = '...'

           table_ocr = appbuilder.DocFormatConverter()
           out = self.component.run(appbuilder.Message(content={"file_path": ""}))
           print(out.content)
    """

    name = "doc_converter"
    version = "v1"
    manifests = [
        {
            "name": "doc_format_converter",
            "description": "提供文档格式转换功能，包含图片转word、图片转excel、PDF转word、PDF转excel",
            "parameters": {
                "type": "object",
                "properties": {
                     "file_name": {
                        "type": "string",
                        "description": "待转换文件的文件名称",
                    },
                    "file_url": {
                        "type": "string",
                        "description": "待转换文件的URL地址",
                    },
                    "page_num": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "integer"}
                        ],
                        "description": "待转换PDF文档的页码, 从1开始, 如果不传则默认转换全部页码",
                    }
                },
            "anyOf": [
                    {"required": ["file_name"]},
                    {"required": ["file_url"]}
                ]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0, request_id: str = None) -> Message:
        """
        将PDF、JPG、PNG、BMP等格式文件转换为Word、Excel格式，并返回转换后的文件URL。

        Args:
            message (Message): 包含待转换文件路径和页码信息的消息对象。
            timeout (float, optional): 请求超时时间，单位为秒。默认为None，表示不设置超时时间。
            retry (int, optional): 请求重试次数。默认为0，表示不重试。

        Returns:
            Message: 包含转换后文件URL的消息对象。
            
        Raises:
            AppBuilderServerException: 文档格式转换服务发生错误时抛出。
        """
        doc_message = DocFormatConverterInMessage(**message.content)
        submit_request = DocFormatConverterSubmitRequest()

        if doc_message.file_path.startswith(('http://', 'https://')):
            # TODO 根据URL判断文件类型Refactor
            if(".pdf" in doc_message.file_path):
                submit_request.pdf_file = base64.b64encode(requests.get(doc_message.file_path).content)
                if doc_message.page_num:
                    submit_request.pdf_file_num = doc_message.page_num
            else:
                submit_request.url = doc_message.file_path
        else:
            if doc_message.file_path.endswith('.pdf'):
                with open(doc_message.file_path, 'rb') as f:
                    submit_request.pdf_file = base64.b64encode(f.read())
                if doc_message.page_num:
                    submit_request.pdf_file_num = doc_message.page_num
            else:
                with open(doc_message.file_path, 'rb') as f:
                    submit_request.image =  base64.b64encode(f.read())
        docConverterSubmitResponse = self.submitDocFormatConverterTask(submit_request, request_id=request_id)
        taskId = docConverterSubmitResponse.result.task_id
        TASK_PROGRESS_COMPLETED = 3
        TASK_PROGRESS_FAILED = 4
        if taskId:
            task_request_time = 1
            while True:
                request = DocFormatConverterQueryRequest()
                request.task_id = taskId
                docConverterQueryResponse = self.queryDocFormatConverterTask(request, request_id=request_id)
                if docConverterQueryResponse.result.ret_code is not None:
                    task_progress = docConverterQueryResponse.result.ret_code
                    if task_progress == TASK_PROGRESS_COMPLETED:
                        break
                    elif task_progress == TASK_PROGRESS_FAILED:
                        raise AppBuilderServerException(f'doc convert task progress failed: {docConverterQueryResponse.error_msg}')
                    # TODO 文档格式转换查询间隔Refactor
                    if task_request_time <= 3:
                        time.sleep(3)
                    else:
                        time.sleep(task_request_time)
                    task_request_time += 1
            word_url = docConverterQueryResponse.result.result_data.word
            excel_url = docConverterQueryResponse.result.result_data.excel
            out = DocFormatConverterOutMessage(word_url=word_url, excel_url=excel_url)
            return Message(content=out.model_dump())
        else:
            raise AppBuilderServerException(f'service error when doc convert：{docConverterSubmitResponse.error_msg}')


    @HTTPClient.check_param
    def submitDocFormatConverterTask(
        self,
        request: DocFormatConverterSubmitRequest,
        timeout: float = None, 
        retry: int = 0,
        request_id: str = None,
    ) -> DocFormatConverterSubmitResponse:
        """
        提交任务
        :param request: 请求参数
        :type request: DocFormatConverterSubmitRequest
        :return: 返回结果
        :rtype: DocFormatConverterSubmitResponse
        """
        url = self.http_client.service_url("/v1/bce/aip/text_mind/v1/doc_convert/request",'/api')
        data = json.loads(DocFormatConverterSubmitRequest.to_json(request, preserving_proto_field_name=True))
        headers = self.http_client.auth_header(request_id)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry

        response = self.http_client.session.post(url, data=data, headers=headers, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        response = DocFormatConverterSubmitResponse.from_json(payload=json.dumps(data))
        return response

    @HTTPClient.check_param
    def queryDocFormatConverterTask(
        self,
        request: DocFormatConverterQueryRequest,
        timeout: float = None, 
        retry: int = 0,
        request_id: str = None
    ) -> DocFormatConverterQueryResponse:
        """
        查询任务
        :param request: 请求参数
        :type request: DoFormatcConverterQueryRequest
        :return: 返回结果
        :rtype: DocFormatConverterSubmitResponse
        """
        url = self.http_client.service_url("/v1/bce/aip/text_mind/v1/doc_convert/get_request_result",'/api')
        data = {
            "task_id": request.task_id
        }
        data = json.loads(DocFormatConverterQueryRequest.to_json(request, preserving_proto_field_name=True))
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = "application/x-www-form-urlencoded"

        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        response = self.http_client.session.post(url, data=data, headers=headers, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        response = DocFormatConverterQueryResponse.from_json(payload=json.dumps(data))
        return response

    @components_run_stream_trace
    def tool_eval(self, streaming: bool, origin_query: str, **kwargs,):
        """
        评估工具函数。
        
        Args:
            streaming (bool): 是否流式输出。如果为True，则逐个生成文件URL；如果为False，则直接返回结果内容。
            origin_query (str): 原始查询字符串。
            **kwargs: 其他关键字参数，包括但不限于：
                traceid (str): 请求的跟踪ID，用于日志追踪。
                file_url (str): 文件的URL地址。如果为空，则从file_urls和file_name中获取。
                file_urls (dict): 包含多个文件路径与URL的映射关系的字典。
                file_name (str): 文件名。如果file_url为空，则从file_urls和file_name中获取file_url。
                page_num (Union[int, str]): 需要处理的页面编号，如果为字符串，必须为纯数字。
        
        Returns:
            如果streaming为True，则逐个生成包含文件URL的字典；如果streaming为False，则直接返回结果内容。
        
        Raises:
            InvalidRequestArgumentError: 如果请求格式错误，如page_num不是整数、file_url为空且无法从file_urls和file_name中获取file_url等。
            AppBuilderServerException: 如果服务执行过程中出现异常。
        
        """
        traceid = kwargs.get("traceid")
        file_url = kwargs.get("file_url", None)
        page_num = kwargs.get("page_num", '')
        if page_num:
            if isinstance(page_num, int) or (isinstance(page_num, str) and page_num.isdigit()):
                page_num = str(page_num)
            else:
                raise InvalidRequestArgumentError("request format error, page_num must be a integer")
        if not file_url or not (file_url.startswith("http") or file_url.startswith("https")):
            file_urls = kwargs.get("file_urls", {})
            file_path = kwargs.get("file_name", file_url)
            if not file_path:
                raise InvalidRequestArgumentError("request format error, file name is not set")
            file_name = os.path.basename(file_path)
            file_url = file_urls.get(file_name, None)
            if not file_url:
                raise InvalidRequestArgumentError("request format error, file url is not set")
        try:
            result = self.run(Message({"file_path": file_url, "page_num": page_num}), request_id=traceid)
        except AppBuilderServerException:
            raise
        except Exception as e:
            raise AppBuilderServerException(f'service error when doc convert：{e}')
        if streaming:
            yield {
                "type": "files",
                "text": [result.content['word_url'], result.content['excel_url']]
            }
        else:
            return result.content