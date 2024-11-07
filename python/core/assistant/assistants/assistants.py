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
from appbuilder.core.assistant.type import assistant_type
from appbuilder.utils.collector import Collector
from appbuilder.utils.collector import AssistantKeys
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.core.assistant.assistants.files import Files
from appbuilder.utils.trace.tracer_wrapper import assistent_tool_trace


class Assistants(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    @property
    def files(self):
        """
        获取当前工作目录下的文件对象。
        
        Args:
            无
        
        Returns:
            Files: 返回当前工作目录下的文件对象。
        
        """
        return Files()

    @assistent_tool_trace
    def create(self,
               name: str,
               description: str,
               model: Optional[str] = "ERNIE-4.0T-8K",
               response_format: Optional[str] = 'text',
               instructions: Optional[str] = "你是百度制作的AI助手",
               thought_instructions: Optional[str] = "",
               chat_instructions: Optional[str] = "",
               tools: Optional[list[assistant_type.AssistantTool]] = [],
               file_ids: Optional[list[str]] = [],
               metadata: Optional[dict] = {},
               ) -> assistant_type.AssistantCreateResponse:
        """
        创建助手实例
        
        Args:
            name (str): 助手名称
            description (str): 助手描述
            model (Optional[str], optional): 模型名称. Defaults to "ERNIE-4.0T-8K".
            response_format (Optional[str], optional): 响应格式. Defaults to 'text'.
            instructions (Optional[str], optional): 指令. Defaults to "".
            thought_instructions (Optional[str], optional): 思考指令. Defaults to "".
            chat_instructions (Optional[str], optional): 聊天指令. Defaults to "".
            tools (Optional[list[assistant_type.AssistantTool]], optional): 工具列表. Defaults to [].
            file_ids (Optional[list[str]], optional): 文件ID列表. Defaults to [].
            metadata (Optional[dict], optional): 元数据. Defaults to {}.
        
        Returns:
            assistant_type.AssistantCreateResponse: 助手创建响应
        
        """
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants")

        req = assistant_type.AssistantCreateRequest(
            name=name,
            description=description,
            model=model,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            tools=tools,
            file_ids=file_ids,
            metadata=metadata,
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

        resp = assistant_type.AssistantCreateResponse(**data)
        Collector().add_to_collection(AssistantKeys.ASSISTANT, resp, resp.id)
        return resp
    
    @assistent_tool_trace
    def update(self,
               assistant_id: str,
               model: Optional[str],
               name: Optional[str],
               description: Optional[str],
               instructions: Optional[str] = "",
               tools: Optional[list[assistant_type.AssistantTool]] = [],
               thought_instructions: Optional[str] = "",
               chat_instructions: Optional[str] = "",
               response_format: Optional[str] = "text",
               file_ids: Optional[list[str]] = [],
               metadata: Optional[dict] = {}
               ) -> assistant_type.AssistantUpdateResponse:
        """
        根据assistant_id修改一个已创建的Assistant
        
        Args:
            assistant_id (str): 助手ID。
            model (Optional[str]): 助手模型。
            name (Optional[str]): 助手名称。
            description (Optional[str]): 助手描述。
            response_format (Optional[str], optional): 响应格式。默认为None。
            instructions (Optional[str], optional): 助手指令。默认为None。
            thought_instructions (Optional[str], optional): 思考指令。默认为None。
            chat_instructions (Optional[str], optional): 聊天指令。默认为None。
            tools (Optional[list[assistant_type.AssistantTool]], optional): 助手工具列表。默认为空列表。
            file_ids (Optional[list[str]], optional): 文件ID列表。默认为空列表。
            metadata (Optional[dict], optional): 助手元数据。默认为空字典。
        
        Returns:
            assistant_type.AssistantUpdateResponse: 助手更新响应。
        
        """
        
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/update")
        
        req = assistant_type.AssistantUpdateRequest(
            assistant_id=assistant_id,
            model=model,
            name=name,
            description=description,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            tools=tools,
            file_ids=file_ids,
            metadata=metadata,
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

        resp = assistant_type.AssistantUpdateResponse(**data)
        return resp
    
    @assistent_tool_trace
    def list(self,
             limit: Optional[int] = 20,
             order: Optional[str] = "desc",
             after: Optional[str] = "",
             before: Optional[str] = "",
             ) -> assistant_type.AssistantListResponse:
        """
        查询当前用户已创建的assistant列表
        
        Args:
            limit (Optional[int], optional): 返回助手列表的最大数量，默认为20。
            order (Optional[str], optional): 返回助手列表的排序方式，可选值为"asc"或"desc"，默认为"desc"。
            after (Optional[str], optional): 返回助手列表中id在指定id之后的助手，默认为空字符串。
            before (Optional[str], optional): 返回助手列表中id在指定id之前的助手，默认为空字符串。
        
        Returns:
            assistant_type.AssistantListResponse: 助手列表响应体。
        
        """
        
        
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/list")
        
        req = assistant_type.AssistantListRequest(
            limit=limit,
            order=order,
            after=after,
            before=before
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

        resp = assistant_type.AssistantListResponse(**data)
        return resp
    
    @assistent_tool_trace
    def query(self,
              assistant_id: Optional[str]) -> assistant_type.AssistantQueryResponse:
        """
        根据assistant_id查询Assistant信息
        
        Args:
            assistant_id (Optional[str]): 助手ID
        
        Returns:
            assistant_type.AssistantQueryResponse: 助手查询响应结果
        
        Raises:
            HTTPError: 请求失败，抛出HTTPError异常
        """
        
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/query")
        
        req = assistant_type.AssistantQueryRequest(
            assistant_id=assistant_id
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

        resp = assistant_type.AssistantQueryResponse(**data)
        return resp
    
    @assistent_tool_trace
    def delete(self,
               assistant_id: Optional[str]) -> assistant_type.AssistantDeleteResponse:
        """
        根据assistant_id删除指定Assitant
        
        Args:
            assistant_id (Optional[str]): 待删除的助手实例ID。
        
        Returns:
            assistant_type.AssistantDeleteResponse: 删除助手实例后的响应结果。
        
        Raises:
            HttpRequestError: 发送HTTP请求时发生错误。
        
        """
        
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/delete")
        
        req = assistant_type.AssistantDeleteRequest(
            assistant_id=assistant_id
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
        
        resp = assistant_type.AssistantDeleteResponse(**data)
        return resp
    
    @assistent_tool_trace
    def mount_files(self,
            assistant_id: Optional[str],
            file_id: Optional[str]
            ) -> assistant_type.AssistantFilesResponse:
        """
        指定file_id和assistant_id，挂载File到对应的Assistant
        
        Args:
            assistant_id (Optional[str]): 助理ID。
            file_id (Optional[str]): 文件ID。
        
        Returns:
            assistant_type.AssistantFilesResponse: 助理文件列表响应对象。
        
        """
        if not isinstance(assistant_id, str):
            raise TypeError("assistant_id must be a string")
        if not assistant_id:
            raise ValueError("assistant_id can't be empty")
        if not isinstance(file_id, str):
            raise TypeError("file_id must be a string")
        if not file_id:
            raise ValueError("file_id can't be empty")
        try:
            self.files.query(file_id)
        except:
            raise FileNotFoundError("can't find file with id {}".format(file_id))
        
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/files")
        
        req = assistant_type.AssistantFilesRequest(
            assistant_id=assistant_id,
            file_id=file_id
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
        
        resp = assistant_type.AssistantFilesResponse(**data)
        return resp
    
    @assistent_tool_trace
    def mounted_files_list(self,
                   assistant_id: Optional[str],  
                   limit: Optional[int] = 20,
                   order: Optional[str] =  'desc' , 
                   after: Optional[str] =  "", 
                   before: Optional[str] =  "") -> assistant_type.AssistantMountedFilesListResponse:
        """
        查询Assistant挂载的File列表
        
        Args:
            assistant_id (Optional[str]): 助手ID，为空时获取当前登录用户的助手文件列表。
            limit (Optional[int], optional): 每页最多显示多少个文件。默认为20。
            order (Optional[AssistantListRole], optional): 文件列表排序方式。可选值为 'asc' 或 'desc'。默认为 'desc'。
            after (Optional[str], optional): 返回文件ID大于该值的文件列表。默认为空字符串。
            before (Optional[str], optional): 返回文件ID小于该值的文件列表。默认为空字符串。
        
        Returns:
            assistant_type.AssistantFilesListResponse: 包含文件列表信息的响应对象。
        
        """
        
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/files/list")
        
        req = assistant_type.AssistantMountedFilesListRequest(
            assistant_id=assistant_id,
            limit=limit,
            order=order,
            after=after,
            before=before
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
        
        resp = assistant_type.AssistantMountedFilesListResponse(**data)
        return resp
    
    @assistent_tool_trace
    def unmount_files(self,
                     assistant_id: Optional[str],
                     file_id: Optional[str]
                     ) -> assistant_type.AssistantFilesDeleteResponse:
        """
        指定assistant_id和file_id，解绑Assistant中对应File的关联
        
        Args:
            assistant_id (Optional[str]): 助理ID。
            file_id (Optional[str]): 文件ID。
        Returns:
            assistant_type.AssistantFilesDeleteResponse: 响应对象。
        """
        if not isinstance(assistant_id, str):
            raise TypeError("assistant_id must be a string")
        if not assistant_id:
            raise ValueError("assistant_id can't be empty")
        if not isinstance(file_id, str):
            raise TypeError("file_id must be a string")
        if not file_id:
            raise ValueError("file_id can't be empty")
        try:
            list_response=self.mounted_files_list(assistant_id, limit=2147483647)
            exist_files = False
            for data in list_response.data:
                if data.id == file_id:
                    exist_files = True
                    break
            if exist_files == False:
                raise FileNotFoundError
        except:
            raise FileNotFoundError("can't find file with id {}".format(file_id))
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/assistants/files/delete")
        
        req = assistant_type.AssistantFilesDeleteRequest(
            assistant_id=assistant_id,
            file_id=file_id
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
        
        resp = assistant_type.AssistantFilesDeleteResponse(**data)
        return resp
            

             
    
    
        
