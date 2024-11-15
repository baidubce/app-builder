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
from appbuilder.core.assistant.type import thread_type
from appbuilder.core._client import AssistantHTTPClient
from typing import Optional
from appbuilder.utils.trace.tracer_wrapper import assistent_tool_trace


class Messages(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    @assistent_tool_trace
    def create(self, 
               thread_id: str,
               content: str,
               role: Optional[str] = "user",
               file_ids: Optional[list[str]] = []) -> thread_type.AssistantMessageCreateResponse:
        """
        创建一条消息。
        
        Args:
            thread_id (str): 线程ID。
            content (str): 消息内容。
            role (Optional[str], optional): 角色，可选值为"user"或"assistant"。默认为"user"。
            file_ids (Optional[list[str]], optional): 消息中包含的文件ID列表。默认为空列表。
        
        Returns:
            thread_type.AssistantMessageCreateResponse: 消息创建响应对象。
        
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/messages")

        req = thread_type.AssistantMessageCreateRequest(
            thread_id=thread_id,
            content=content,
            role=role,
            file_ids=file_ids
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        response = thread_type.AssistantMessageCreateResponse(**data)
        return response
    
    @assistent_tool_trace
    def update(self,
               thread_id: str,
               message_id: str,
               content: Optional[str],
               file_ids: Optional[list[str]] = []) -> thread_type.AssistantMessageUpdateResponse:
        """
        修改Message对象，允许content和file_ids字段
        
        Args:
            thread_id (str): 线程ID。
            message_id (str): 消息ID。
            content (Optional[str], optional): 消息内容。默认为空字符串。
            file_ids (Optional[list[str]], optional): 消息中包含的文件ID列表。默认为空列表。
        
        Returns:
            thread_type.AssistantMessageUpdateResponse: 消息更新响应对象。
        
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/messages/update")
        
        req = thread_type.AssistantMessageUpdateRequest(
            thread_id = thread_id, 
            message_id = message_id,
            content = content,
            file_ids = file_ids
        )
        
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)
        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.AssistantMessageUpdateResponse(**data)
        return response  

    @assistent_tool_trace
    def list(self,
            thread_id: str,
            limit: int = 20,
            order: str = "desc",
            after: str = "",
            before: str = "") -> thread_type.AssistantMessageListResponse:
        """
        查询指定Thread下的Message列表
        
        Args:
            thread_id (str): 线程ID。
            limit (int, optional): 返回消息的最大数量，取值范围为[1,20]。默认为-20。
            order (Optional[str], optional): 排序方式，可选值为"asc"或"desc"。默认为"desc"。
            after (Optional[str], optional): 查询指定message_id之后创建的Message。
            before (Optional[str], optional): 查询指定message_id之前创建的Message
            
        Returns:
            thread_type.AssistantMessageListResponse: 查询thread下的message列表响应对象。
            
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/messages/list")
        
        req = thread_type.AssistantMessageListRequest(
            thread_id = thread_id,
            limit = limit,
            order = order,
            after = after,
            before = before
        )
        
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)
        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.AssistantMessageListResponse(**data)
        return response 
    
    @assistent_tool_trace
    def query(self,
            thread_id:str,
            message_id:str) -> thread_type.AssistantMessageQueryResponse:
        """
        根据message_id查询指定Message的信息
        
        Args:
            thread_id (str): 线程ID
            message_id (str): 消息ID
        
        Returns:
            thread_type.AssistantMessageQueryResponse: 消息信息响应
            
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/messages/query")
        req = thread_type.AssistantMessageQueryRequest(
            thread_id = thread_id,
            message_id = message_id
        )
        
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)
        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.AssistantMessageQueryResponse(**data)
        return response  
    
    @assistent_tool_trace
    def files(self,
              thread_id:str,
              message_id:str,
              limit:Optional[int] =  20,
              order:Optional[str] = "desc",
              after:Optional[str] = "",
              before:Optional[str] = "") -> thread_type.AssistantMessageFilesResponse:
        """
        获取指定消息 ID 的附件信息。
        
        Args:
            thread_id (str): 线程 ID。
            messsages_id (str): 消息 ID。
            limit (Optional[int], optional): 返回结果的最大数量，默认为 20。
            order (Optional[str], optional): 排序方式，可选值为 "asc" 或 "desc"，默认为 "desc"。
            after (Optional[str], optional): 返回结果的时间范围，只返回时间晚于该时间戳的消息附件，默认为空。
            before (Optional[str], optional): 返回结果的时间范围，只返回时间早于该时间戳的消息附件，默认为空。
        
        Returns:
            thread_type.AssistantMessageFilesResponse: 附件信息响应对象。
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/messages/files/list")
        
        req = thread_type.AssistantMessageFilesRequest(
            thread_id = thread_id, 
            message_id = message_id,
            limit = limit,
            order = order,
            after = after,
            before = before
        )
        
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)
        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)
        response = thread_type.AssistantMessageFilesResponse(**data)
        return response 
