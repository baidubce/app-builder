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
from appbuilder.utils.trace.tracer_wrapper import assistent_tool_trace

class Files(object):
    def __init__(self):
        self._http_client = AssistantHTTPClient()

    @assistent_tool_trace
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

    @assistent_tool_trace
    def list(self) -> assistant_type.AssistantFilesListResponse:
        """
        列出存储中的文件列表。
        
        此方法向存储服务发送请求，获取已上传的文件列表。返回的文件列表包含每个文件的详细信息，
        包括文件ID、大小、用途、审核状态、创建时间、文件名、文件分类ID等。

        Args:
            无

        Returns:
            assistant_type.AssistantFilesListResponse: 文件列表的响应对象，包含以下属性：
            
            - object (str): 表示对象类型，默认值为 "list"
            
            - data (list[AssistantFilesListData]): 包含文件信息的列表，列表中的每个元素为 AssistantFilesListData 对象。该对象包含以下属性：
            
                - id (str): 文件ID
                - bytes (int): 文件大小（字节）
                - object (str): 文件对象标识
                - purpose (str): 文件用途
                - censored (AuditStatus): 文件的审核状态
                - create_at (int): 文件创建时间戳
                - filename (str): 文件名
                - classification_id (str): 文件分类ID
                - file_type (str): 文件类型

        Raises:
            assistant_type.AssistantError: 请求发生错误时抛出，具体错误信息可通过 `error_msg` 属性获取。
        """
        headers = self._http_client.auth_header()  # 获取身份认证头
        headers['Content-Type'] = 'application/json'  # 设置请求头为JSON格式
        url = self._http_client.service_url("/v2/storage/files/list")  # 拼接存储服务的URL
        
        response = self._http_client.session.post(  # 向存储服务发送POST请求，获取文件列表
            url=url,
            headers=headers,
            json={},  # 发送空的JSON请求体
            timeout=None  # 设置为无超时限制
        ) 
        self._http_client.check_response_header(response)  # 检查响应头是否合法

        request_id = self._http_client.response_request_id(response)  # 从响应中获取请求ID
        data = response.json()  # 将响应内容转换为JSON格式

        self._http_client.check_assistant_response(request_id, data)  # 检查Assistant响应是否有错误
        resp = assistant_type.AssistantFilesListResponse(**data)  # 将响应数据映射为AssistantFilesListResponse对象
        return resp  # 返回文件列表响应对象

    
    @assistent_tool_trace
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
    
    @assistent_tool_trace
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
    
    @assistent_tool_trace
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
        if file_path != "" and not os.path.exists(file_path):
            raise FileNotFoundError("file_path {} not found".format(file_path))
        if file_path != "" and not os.path.isdir(file_path):
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
        
    @assistent_tool_trace
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

 