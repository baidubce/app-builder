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


import os
import json
from typing import Optional
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core._client import AssistantHTTPClient

from appbuilder.core._exception import AppBuilderServerException

class Files(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    def create(self, file_path: str, purpose: str = "assistant") -> assistant_type.AssistantFilesCreateResponse:
        """
        上传文件到助理存储中。
        
        Args:
            file_path (str): 要上传的文件路径。
            purpose (str, optional): 上传文件的用途。默认为 "assistant"。
        
        Returns:
            assistant_type.AssistantFilesCreateResponse: 上传文件后返回的响应对象。
        
        Raises:
            ValueError: 如果指定的文件路径不存在，则会引发此异常。
        """
        headers = self._http_client.auth_header()
        headers.pop("Content-Type")
        url = self._http_client.service_url("/v2/storage/files")

        if not os.path.exists(file_path):
            raise ValueError("File {} not exists".format(file_path))

        with open(file_path, 'rb') as f:
            files = [
                ('file',(os.path.basename(file_path), f))
            ]

            response = self._http_client.session.post(
                url,
                headers=headers,
                files=files,
                params={
                    'purpose': purpose
                }
            )

        self._http_client.check_response_header(response)

        request_id = self._http_client.response_request_id(response)
        data = response.json()

        self._http_client.check_assistant_response(request_id, data)
        resp = assistant_type.AssistantFilesCreateResponse(**data)
        return resp

        
    def list(self) -> assistant_type.AssistantFilesListResponse:
        """
        列出存储中的文件列表
        
        Args:
            无
        
        Returns:
            assistant_type.AssistantFilesListResponse: 文件列表的响应对象，包含以下属性：
        
        Raises:
            assistant_type.AssistantError: 请求发生错误时抛出，具体错误信息可通过 `error_msg` 属性获取
        """
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self._http_client.service_url("/v2/storage/files/list")
        
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json={},
            timeout=None
        ) 
        self._http_client.check_response_header(response)

        request_id = self._http_client.response_request_id(response)
        data = response.json()

        self._http_client.check_assistant_response(request_id, data)
        resp = assistant_type.AssistantFilesListResponse(**data)
        return resp

    
    
    def query(self,
              file_id: str,
            ) -> assistant_type.AssistantFilesQueryResponse:
        """
        查询文件详情
        
        Args:
            file_id (str): 文件ID
        
        Returns:
            assistant_type.AssistantFilesQueryResponse: 文件详情
        
        Raises:
            无
        """

        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self._http_client.service_url("/v2/storage/files/query")
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json={
                'file_id': file_id
            },
            timeout=None
        )
        self._http_client.check_response_header(response)

        request_id = self._http_client.response_request_id(response)
        data = response.json()

        self._http_client.check_assistant_response(request_id, data)
        resp = assistant_type.AssistantFilesQueryResponse(**data)
        return resp 
    
    def delete(self,
               file_id: str,
            ) -> assistant_type.AssistantFilesDeleteResponse:
        """
        删除文件
        Args:
            file_id (str): 文件ID
        Returns:
            assistant_type.AssistantFilesDeleteResponse: 删除文件后的响应对象。
        Raises:
            无
        """
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self._http_client.service_url("/v2/storage/files/delete")
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json={
                'file_id': file_id
            },
            timeout=None
        )
        self._http_client.check_response_header(response)
        request_id = self._http_client.response_request_id(response)
        data = response.json()
        self._http_client.check_assistant_response(request_id, data)
        resp = assistant_type.AssistantFilesDeleteResponse(**data)
        return resp
    
    def download(self,
                 file_id:str,
                 file_path:str="",
                 timeout:Optional[int]=None,
                 ):
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self._http_client.service_url("/v2/storage/files/download")
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json={
                'file_id': file_id
            },
            timeout=timeout
        )
        self._http_client.check_response_header(response)
        request_id = self._http_client.response_request_id(response) 
        
        filename=response.headers['Content-Disposition'].split("filename=")[-1]
        file_path+=filename
        try:    
            with open(file_path,'wb') as file:
                for chunk in response.iter_content():
                    if chunk:
                        file.write(chunk)
        except Exception as e:
            raise FileNotFoundError("请检查文件路径是否正确")
        
           
        
    def content(self,
                file_id:str,
                timeout:Optional[int]=None):
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self._http_client.service_url("/v2/storage/files/content")
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json={
                'file_id': file_id
            },
            timeout=timeout
        )
        self._http_client.check_response_header(response)
        request_id = self._http_client.response_request_id(response)
        
        content=b''
        for chunk in response.iter_content():
            if chunk:
                content+=chunk
        
        res=assistant_type.AssistantFilesContentResponse(
            content_type =response.headers['Content-Type'],
            content = content
        )
        
        return res

 