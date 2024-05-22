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

from appbuilder.core._exception import AppBuilderServerException,HTTPConnectionException

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
        根据文件ID查询文件信息
        
        Args:
            file_id (str): 文件ID
        
        Returns:
            assistant_type.AssistantFilesQueryResponse: 文件查询响应对象
        
        Raises:
            TypeError: 如果file_id不是str类型
            ValueError: 如果file_id不存在
        """

        if not isinstance(file_id, str):
            raise TypeError("file_id must be str")
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
        try:
            self._http_client.check_response_header(response)

            request_id = self._http_client.response_request_id(response)
            data = response.json()

            self._http_client.check_assistant_response(request_id, data)
            resp = assistant_type.AssistantFilesQueryResponse(**data)
        except AssertionError:
            raise ValueError('file_id {} is not exist'.format(file_id))
        except TypeError:
            raise ValueError('file_id {} is not exist'.format(file_id))
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
                 file_path:str="", # 要求若文件路径不为空，需要以/结尾，默认下载到当前文件夹
                 timeout:Optional[int]=None,
                 ):
        """
        下载文件
        
        Args:
            file_id (str): 文件ID
            file_path (str, optional): 文件保存路径，默认为空字符串。如果未指定，则使用文件名的默认值。要求若文件路径不为空，需要以/结尾。
            timeout (Optional[int], optional): 请求超时时间，单位秒。如果未指定，则使用默认超时时间。
        
        Returns:
            None
        
        Raises:
            TypeError: 当file_path或file_id类型不为str时引发此异常。
            ValueError: 当file_id为空或None时，或file_path不是文件目录时引发此异常。
            FileNotFoundError: 当指定的文件路径或文件不存在时引发此异常。
            OSError: 当磁盘空间不足时引发此异常。
            HTTPConnectionException: 当请求失败时引发此异常。
            Exception: 当发生其他异常时引发此异常。
        """
        if not isinstance(file_path, str):
            raise TypeError("file_path must be str")
        if not isinstance(file_id, str):
            raise TypeError("file_id must be str")
        if file_id == "" or file_id is None:
            raise ValueError("file_id cannot be empty or None")
        try:
            self.query(file_id)
        except:
            raise FileNotFoundError("file_id {} not found".format(file_id))
        if file_path != "" and not file_path.endswith('/'):
            raise ValueError("file_path must be a file directory")
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/storage/files/download")
        try:
            response = self._http_client.session.post(
                url=url,
                headers=headers,
                json={
                    'file_id': file_id
                },
                timeout=timeout
            )
        except:
            raise HTTPConnectionException("request failed")
        self._http_client.check_response_header(response)
        
        filename=response.headers['Content-Disposition'].split("filename=")[-1]
        file_path+=filename
        try:    
            with open(file_path,'wb') as file:
                for chunk in response.iter_content():
                    if chunk:
                        file.write(chunk)
        except FileNotFoundError as e:
            raise FileNotFoundError("请检查文件路径是否正确,错误信息{}".format(e))
        except OSError as e:
            raise OSError("磁盘空间不足,错误信息{}".format(e))
        except Exception as e:
            raise Exception("出现错误,错误信息{}".format(e))
        
        
           
        
    def content(self,
                file_id:str,
                timeout:Optional[int]=None):
        """
        获取指定文件的内容
        
        Args:
            file_id (str): 文件ID
            timeout (Optional[int], optional): 请求超时时间，单位秒. Defaults to None.
        
        Returns:
            assistant_type.AssistantFilesContentResponse: 包含文件内容的响应对象
        
        Raises:
            TypeError: 当file_id不是字符串类型时引发此异常
            FileNotFoundError: 当指定的文件路径不存在时引发此异常
            HTTPConnectionException: 当请求失败时引发此异常
        
        """
        if not isinstance(file_id, str):
            raise TypeError("file_id must be str")
        try:
            self.query(file_id)
        except:
            raise FileNotFoundError("can't find file with id {}".format(file_id))
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        url = self._http_client.service_url("/v2/storage/files/content")
        try:
            response = self._http_client.session.post(
                url=url,
                headers=headers,
                json={
                    'file_id': file_id
                },
                timeout=timeout
            )
        except:
            raise HTTPConnectionException("request failed")
        self._http_client.check_response_header(response)
        
        content=b''
        for chunk in response.iter_content():
            if chunk:
                content+=chunk
        
        res=assistant_type.AssistantFilesContentResponse(
            content_type =response.headers['Content-Type'],
            content = content
        )
        
        return res

 