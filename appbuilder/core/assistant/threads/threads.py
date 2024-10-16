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

import os
from typing import Optional
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.threads.messages import Messages
from appbuilder.core.assistant.threads.runs import Runs
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.utils.trace.tracer_wrapper import assistent_tool_trace
class Threads():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    @property
    def messages(self) -> Messages:
        """
        获取消息实例
        
        Args:
            无
        
        Returns:
            Messages: 返回Messages实例
        
        """
        return Messages()
    
    @property
    def runs(self) -> Runs:
        """
        返回Runs对象。
        
        Args:
            无
        
        Returns:
            Runs: 一个Runs对象实例。
        """
        return Runs()

    @assistent_tool_trace
    def create(self, messages: Optional[list[thread_type.AssistantMessage]] = []) -> thread_type.ThreadCreateResponse:
        """
        创建一个新的对话线程。
        
        Args:
            messages: 要发送给助手的消息列表。如果不传入此参数，则会创建一个空对话线程。
        
        Returns:
            一个ThreadCreateResponse对象，包含新创建的线程的相关信息。
        
        Raises:
            ValueError: 如果传入的messages参数不是列表类型。
        
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads")
        
        if  not isinstance(messages, list):
            raise ValueError("Threads().create() messages must be a list, but got: {}".format(messages))

        req = thread_type.ThreadCreateRequest(
            messages=messages)

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        response = thread_type.ThreadCreateResponse(**data)
        return response
    
    @assistent_tool_trace
    def query(self,
              thread_id:str)->thread_type.ThreadQueryResponse:
        """
        查询对话线程信息。

        Args:
            thread_id: 要查询的对话线程ID。

        Returns:
            一个ThreadQueryResponse对象，包含对话线程的相关信息。
            
        Raises:
            ValueError: 如果传入的thread_id参数不是字符串类型。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/query")
        
        req = thread_type.ThreadQueryRequest(
            thread_id=thread_id)

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.ThreadQueryResponse(**data)
        return response
    
    @assistent_tool_trace
    def delete(self,
               thread_id:str)->thread_type.ThreadDeleteResponse:
        """
        删除对话线程。
        Args:
            thread_id: 要删除的对话线程ID。
        Returns:
            一个ThreadDeleteResponse对象，包含对话线程的相关信息。
        Raises:
            ValueError: 如果传入的thread_id参数不是字符串类型。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/delete")
        
        req = thread_type.ThreadDeleteRequest(
            thread_id=thread_id)

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.ThreadDeleteResponse(**data)
        return response
    
    @assistent_tool_trace
    def update(self,
               thread_id:str ,
               metadata:Optional[dict] ={} )->thread_type.ThreadUpdateResponse:
        """
        更新线程信息
        
        Args:
            thread_id (str): 线程ID
            metadata (Optional[dict], optional): 线程元数据. 默认为空字典.
        
        Returns:
            thread_type.ThreadUpdateResponse: 线程更新响应
        
        Raises:
            TypeError: 如果metadata不是字典类型
            ValueError: 如果metadata的键超过64个字符或值超过512个字符
        """
        if not isinstance(metadata, dict):
            raise TypeError("Threads().update() metadata must be a dict, but got: {}".format(type(metadata)))
        for key,value in metadata.items():
            if len(key)>64:
                raise ValueError("Threads().update() metadata key must be less than 64, but got: {}".format(len(key)))
            if len(value)>512:
                raise ValueError("Threads().update() metadata value must be less than 512, but got: {}".format(len(value)))
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/update")
        
        req = thread_type.ThreadUpdateRequest(
            thread_id=thread_id)

        response =self._http_client.session.post(
            url = url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.ThreadUpdateResponse(**data)
        return response