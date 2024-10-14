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
import json
import uuid
from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional
from appbuilder.core._client import HTTPClient
from appbuilder.core.console.knowledge_base import data_class
from appbuilder.core.component import Message, Component
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.trace.tracer_wrapper import client_tool_trace


class KnowledgeBase(Component):

    def __init__(
        self,
        knowledge_id: Optional[str] = None,
        knowledge_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.knowledge_id = knowledge_id
        self.knowledge_name = knowledge_name

    @classmethod
    @deprecated()
    def create_knowledge(cls, knowledge_name: str) -> "KnowledgeBase":
        """
        创建一个新的知识库。
        
        Args:
            cls (type): 类对象，用于调用此方法时不需要显式传递。
            knowledge_name (str): 要创建的知识库名称。
        
        Returns:
            KnowledgeBase: 创建的知识库对象。
        
        Raises:
            HTTPError: 如果HTTP请求失败或响应状态码不为200。
            JSONDecodeError: 如果响应数据不是有效的JSON格式。
        
        Note:
            此方法已被弃用，请使用 create_knowledge_base 方法代替。
        """
        payload = json.dumps({"name": knowledge_name})
        http_client = HTTPClient()
        headers = http_client.auth_header()
        headers["Content-Type"] = "application/json"
        create_url = "/v1/ai_engine/agi_platform/v1/datasets/create"
        response = http_client.session.post(
            url=http_client.service_url(create_url), headers=headers, data=payload
        )
        http_client.check_response_header(response)
        http_client.check_console_response(response)
        response = response.json()["result"]
        return KnowledgeBase(
            knowledge_id=response["id"], knowledge_name=response["name"]
        )

    def upload_file(
        self, file_path: str, client_token: str = None
    ) -> data_class.KnowledgeBaseUploadFileResponse:
        """
        上传文件到知识库服务器。
        
        Args:
            file_path (str): 要上传的文件的路径。
            client_token (str, optional): 客户端令牌，用于标识请求的唯一性。如果未提供，则自动生成。
        
        Returns:
            data_class.KnowledgeBaseUploadFileResponse: 上传文件的响应。
        
        Raises:
            FileNotFoundError: 如果指定的文件路径不存在，则抛出 FileNotFoundError 异常。
        
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File {} does not exist".format(file_path))

        headers = self.http_client.auth_header_v2()
        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2("/file", client_token=client_token)

        with open(file_path, "rb") as f:
            multipart_form_data = {"file": (os.path.basename(file_path), f)}

            response = self.http_client.session.post(
                url=url,
                headers=headers,
                files=multipart_form_data,
            )

            self.http_client.check_response_header(response)
            self.http_client.check_console_response(response)
            data = response.json()
            resp = data_class.KnowledgeBaseUploadFileResponse(**data)

        return resp

    def add_document(
        self,
        content_type: str,
        file_ids: list[str] = [],
        is_enhanced: bool = False,
        custom_process_rule: Optional[data_class.CustomProcessRule] = None,
        knowledge_base_id: Optional[str] = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseAddDocumentResponse:
        """
        向知识库中添加文档。
        
        Args:
            content_type (str): 文档的类型，例如 'TEXT' 或 'PDF'。
            file_ids (list[str], optional): 文档ID列表，默认为空列表。文档ID通常由文件上传接口返回。
            is_enhanced (bool, optional): 是否启用增强模式，默认为False。启用后会对文档进行语义理解和结构化处理。
            custom_process_rule (Optional[data_class.CustomProcessRule], optional): 自定义处理规则，默认为None。
            knowledge_base_id (Optional[str], optional): 知识库ID，默认为None。如果未指定，则使用当前实例的知识库ID。
            client_token (str, optional): 客户端请求的唯一标识，默认为None。如果不指定，则自动生成。
        
        Returns:
            data_class.KnowledgeBaseAddDocumentResponse: 添加文档后的响应对象。
        
        Raises:
            ValueError: 如果知识库ID为空且未先调用`create`方法或未指定现有知识库ID，则抛出ValueError异常。
        
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledge_base/document", client_token=client_token
        )

        request = data_class.KnowledgeBaseAddDocumentRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            content_type=content_type,
            file_ids=file_ids,
            is_enhanced=is_enhanced,
            custom_process_rule=custom_process_rule,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseAddDocumentResponse(**data)
        return resp

    def delete_document(
        self,
        document_id: str,
        knowledge_base_id: Optional[str] = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseDeleteDocumentResponse:
        """
        删除知识库中的文档
        
        Args:
            document_id (str): 要删除的文档ID
            knowledge_base_id (Optional[str], optional): 知识库ID，如果为None，则使用类的知识库ID。默认为None。
            client_token (str, optional): 请求的唯一标识，用于服务器追踪问题。默认为None，如果不传则自动生成。
        
        Returns:
            data_class.KnowledgeBaseDeleteDocumentResponse: 删除文档响应对象
        
        Raises:
            ValueError: 如果未设置类的知识库ID且未提供知识库ID，则抛出ValueError异常。
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledge_base/document", client_token=client_token
        )
        request = data_class.KnowledgeBaseDeleteDocumentRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            document_id=document_id,
        )
        response = self.http_client.session.delete(
            url=url, headers=headers, params=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseDeleteDocumentResponse(**data)
        return resp

    def get_documents_list(
        self,
        limit: int = 10,
        after: Optional[str] = "",
        before: Optional[str] = "",
        knowledge_base_id: Optional[str] = None,
    ) -> data_class.KnowledgeBaseGetDocumentsListResponse:
        """
        获取文档列表。
        
        Args:
            limit (int, optional): 返回的文档数量上限，默认为10。
            after (Optional[str], optional): 返回时间戳大于指定值的文档。默认为空字符串。
            before (Optional[str], optional): 返回时间戳小于指定值的文档。默认为空字符串。
            knowledge_base_id (Optional[str], optional): 知识库ID，如果未指定，则使用当前实例的知识库ID。默认为None。
        
        Returns:
            data_class.KnowledgeBaseGetDocumentsListResponse: 包含文档列表的响应对象。
        
        Raises:
            ValueError: 如果知识库ID为空，且未通过调用create方法创建知识库，则抛出此异常。
        
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledge_base/documents")
        request = data_class.KnowledgeBaseGetDocumentsListRequest(
            knowledge_base_id=knowledge_base_id or self.knowledge_id,
            limit=limit,
            after=after,
            before=before,
        )
        response = self.http_client.session.get(
            url=url, headers=headers, params=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseGetDocumentsListResponse(**data)
        return resp

    def create_knowledge_base(
        self,
        name: str,
        description: str,
        type: str = "public",
        esUrl: str = None,
        esUserName: str = None,
        esPassword: str = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseDetailResponse:
        """
        创建一个知识库
        
        Args:
            name (str): 知识库名称
            description (str): 知识库描述
            type (str, optional): 知识库类型，默认为'public'。默认为 "public"。
            esUrl (str, optional): Elasticsearch 服务地址。默认为 None。
            esUserName (str, optional): Elasticsearch 用户名。默认为 None。
            esPassword (str, optional): Elasticsearch 密码。默认为 None。
            client_token (str, optional): 客户端token，用于区分请求来源。默认为 None。
        
        Returns:
            data_class.KnowledgeBaseDetailResponse: 创建知识库后的响应对象
        
        Raises:
            requests.exceptions.HTTPError: 请求失败时抛出
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateKnowledgeBase", client_token=client_token
        )

        request = data_class.KnowledgeBaseCreateKnowledgeBaseRequest(
            name=name,
            description=description,
            config={
                "index": {
                    "type": type,
                    "esUrl": esUrl,
                    "username": esUserName,
                    "password": esPassword,
                }
            },
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseDetailResponse(**data)
        self.knowledge_id = resp.id
        self.knowledge_name = resp.name
        return resp

    def get_knowledge_base_detail(
        self, knowledge_base_id: Optional[str] = None
    ) -> data_class.KnowledgeBaseDetailResponse:
        """
        获取知识库详情。
        
        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID. 如果为None，则使用实例中的knowledge_id.
                                                        默认为None.
        
        Returns:
            data_class.KnowledgeBaseDetailResponse: 知识库详情响应对象.
        
        Raises:
            ValueError: 如果knowledge_base_id为空且实例中的knowledge_id也为空，则抛出异常.
        
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        request = data_class.KnowledgeBaseGetDetailRequest(
            id=knowledge_base_id or self.knowledge_id
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DescribeKnowledgeBase"
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseDetailResponse(**data)
        return resp

    def modify_knowledge_base(
        self,
        knowledge_base_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        client_token: str = None,
    ):
        """
        修改知识库信息
        
        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID，如果为None，则使用当前实例的知识库ID. 默认为 None.
            name (Optional[str], optional): 知识库名称. 默认为 None.
            description (Optional[str], optional): 知识库描述. 默认为 None.
            client_token (str, optional): 客户端唯一标识符，用于保证幂等性. 默认为 None.
        
        Returns:
            dict: 修改后的知识库信息
        
        Raises:
            ValueError: 如果既没有提供knowledge_base_id，且当前实例没有设置knowledge_id，则抛出此异常.
        
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        request = data_class.KnowledgeBaseModifyRequest(
            id=knowledge_base_id or self.knowledge_id,
            name=name,
            description=description,
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=ModifyKnowledgeBase", client_token=client_token
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def delete_knowledge_base(
        self, knowledge_base_id: Optional[str] = None, client_token: str = None
    ):
        """
        删除知识库
        
        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID. 如果未提供，则使用当前实例的knowledge_id. Defaults to None.
            client_token (str, optional): 请求的唯一标识，用于服务端去重. 如果未提供，则自动生成一个UUID. Defaults to None.
        
        Returns:
            dict: API响应数据
        
        Raises:
            ValueError: 如果既没有提供knowledge_base_id，且当前实例的knowledge_id也为None，则抛出异常
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        request = data_class.KnowledgeBaseDeleteRequest(
            id=knowledge_base_id or self.knowledge_id
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DeleteKnowledgeBase", client_token=client_token
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump()
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def create_documents(
        self,
        id: Optional[str] = None,
        contentFormat: str = "",
        source: data_class.DocumentSource = None,
        processOption: data_class.DocumentProcessOption = None,
        client_token: str = None,
    ):
        """
        创建文档。
        
        Args:
            id (Optional[str], optional): 知识库ID，默认为None。如果为None，则使用当前知识库ID。默认为None。
            contentFormat (str): 文档内容格式，默认为空字符串。
            source (data_class.DocumentSource, optional): 文档来源信息，默认为None。
            processOption (data_class.DocumentProcessOption, optional): 文档处理选项，默认为None。
            client_token (str, optional): 用于标识请求的客户端令牌，默认为None。如果不提供，将自动生成一个UUID。
        
        Returns:
            dict: API响应结果。
        
        Raises:
            ValueError: 如果当前知识库ID为空且未提供id参数，则抛出ValueError异常。
        
        """
        if self.knowledge_id == None and id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"
        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateDocuments", client_token=client_token
        )

        request = data_class.KnowledgeBaseCreateDocumentsRequest(
            id=id or self.knowledge_id,
            source=source,
            contentFormat=contentFormat,
            processOption=processOption,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def get_knowledge_base_list(
        self,
        knowledge_base_id: Optional[str] = None,
        maxKeys: int = 10,
        keyword: Optional[str] = None,
    ) -> data_class.KnowledgeBaseGetListResponse:
        """
        获取知识库列表
        
        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID. 如果为None，则使用self.knowledge_id. 默认为None.
            maxKeys (int, optional): 最大返回数量. 默认为10.
            keyword (Optional[str], optional): 搜索关键字. 默认为None.
        
        Returns:
            data_class.KnowledgeBaseGetListResponse: 知识库列表响应对象.
        
        Raises:
            ValueError: 如果self.knowledge_id和knowledge_base_id都为None，则抛出异常，提示需要先调用create方法或使用已存在的知识库ID.
        
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        request = data_class.KnowledgeBaseGetListRequest(
            marker=knowledge_base_id or self.knowledge_id,
            maxKeys=maxKeys,
            keyword=keyword,
        )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DescribeKnowledgeBases"
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseGetListResponse(**data)
        return resp

    def upload_documents(
        self,
        file_path: str,
        content_format: str = "rawText",
        id: Optional[str] = None,
        processOption: data_class.DocumentProcessOption = None,
        client_token: str = None,
    ):
        """
        上传文档到知识库
        
        Args:
            file_path (str): 文件路径
            content_format (str, optional): 内容格式，默认为 'rawText'。可选项包括 'rawText', 'markdown', 'html' 等
            id (Optional[str], optional): 知识库ID，默认为None，此时将使用当前实例的知识库ID
            processOption (data_class.DocumentProcessOption, optional): 文档处理选项，默认为None
            client_token (str, optional): 客户端token，默认为None，将自动生成一个UUID
        
        Returns:
            dict: 上传文档后的响应数据
        
        Raises:
            FileNotFoundError: 如果指定的文件路径不存在，将抛出 FileNotFoundError 异常
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File {} does not exist".format(file_path))

        headers = self.http_client.auth_header_v2()
        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=UploadDocuments", client_token=client_token
        )

        with open(file_path, "rb") as f:
            multipart_form_data = {"file": (os.path.basename(file_path), f)}

            request = data_class.KnowledgeBaseCreateDocumentsRequest(
                id=id or self.knowledge_id,
                source=data_class.DocumentSource(type="file"),
                contentFormat=content_format,
                processOption=processOption,
            )

            data = {
                "payload": request.model_dump_json(exclude_none=True),
            }

            response = self.http_client.session.post(
                url=url,
                headers=headers,
                data=data,
                files=multipart_form_data,
            )

            self.http_client.check_response_header(response)
            self.http_client.check_console_response(response)
            data = response.json()

        return data

    def create_chunk(
        self,
        documentId: str,
        content: str,
        client_token: str = None,
    ) -> data_class.CreateChunkResponse:
        """
        创建一个知识块。
        
        Args:
            documentId (str): 文档ID。
            content (str): 知识块内容。
            client_token (str, optional): 用于支持幂等性，默认为None。如果为None，则使用uuid4生成一个唯一的client_token。
        
        Returns:
            data_class.CreateChunkResponse: 创建知识块响应。
        
        Raises:
            HTTPError: 如果请求失败，将抛出HTTPError异常。
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateChunk", client_token=client_token
        )

        request = data_class.CreateChunkRequest(
            documentId=documentId,
            content=content,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.CreateChunkResponse(**data)
        return resp

    def modify_chunk(
        self,
        chunkId: str,
        content: str,
        enable: bool,
        client_token: str = None,
    ):
        """
        修改知识库片段
        
        Args:
            chunkId (str): 知识库片段ID
            content (str): 修改后的内容
            enable (bool): 是否启用该知识库片段
            client_token (str, optional): 请求的唯一标识，默认为 None. 如果不指定，则自动生成.
        
        Returns:
            dict: 修改后的知识库片段信息
        
        Raises:
            HttpClientError: 如果请求失败，则抛出 HttpClientError 异常
            ConsoleResponseError: 如果控制台响应错误，则抛出 ConsoleResponseError 异常
        
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=ModifyChunk", client_token=client_token
        )

        request = data_class.ModifyChunkRequest(
            chunkId=chunkId,
            content=content,
            enable=enable,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def delete_chunk(
        self,
        chunkId: str,
        client_token: str = None,
    ):
        """
        删除知识库中的一个块
        
        Args:
            chunkId (str): 要删除的块的ID
            client_token (str, optional): 客户端令牌，用于请求的唯一标识，默认为None。
        
        Returns:
            dict: 包含删除操作结果的字典。
        
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DeleteChunk", client_token=client_token
        )

        request = data_class.DeleteChunkRequest(
            chunkId=chunkId,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def describe_chunk(
        self,
        chunkId: str,
    ) -> data_class.DescribeChunkResponse:
        """
        获取知识库片段信息
        
        Args:
            chunkId (str): 知识库片段的ID
        
        Returns:
            DescribeChunkResponse: 知识库片段信息响应对象
        
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgeBase?Action=DescribeChunk")

        request = data_class.DescribeChunkRequest(
            chunkId=chunkId,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeChunkResponse(**data)
        return resp

    def describe_chunks(
        self,
        documentId: str,
        marker: str = None,
        maxKeys: int = None,
        type: str = None,
    ) -> data_class.DescribeChunksResponse:
        """
        查询文档分块信息
        
        Args:
            documentId (str): 文档ID
            marker (str, optional): 分页标记，默认为None。用于分页查询，如果第一页调用此API后，还有更多数据，API会返回一个Marker值，使用此Marker值调用API可以查询下一页数据，直到没有更多数据，API将不再返回Marker值。
            maxKeys (int, optional): 最大返回记录数，默认为None。指定本次调用最多可以返回的文档分块信息条数，最大值为100。
            type (str, optional): 文档分块类型，默认为None。指定要查询的文档分块类型。
        
        Returns:
            DescribeChunksResponse: 包含文档分块信息的响应对象
        
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgeBase?Action=DescribeChunks")

        request = data_class.DescribeChunksRequest(
            documentId=documentId,
            marker=marker,
            maxKeys=maxKeys,
            type=type,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeChunksResponse(**data)
        return resp

    def get_all_documents(self, knowledge_base_id: Optional[str] = None) -> dict:
        """
        获取知识库中所有文档。
        
        Args:
            knowledge_base_id (Optional[str], optional): 知识库的ID。如果为None，则使用当前实例的knowledge_id。默认为None。
        
        Returns:
            dict: 包含所有文档的列表。
        
        Raises:
            ValueError: 如果knowledge_base_id为空，且当前实例没有已创建的knowledge_id时抛出。
        
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )
        knowledge_base_id = knowledge_base_id or self.knowledge_id
        doc_list = []
        response_per_time = self.get_documents_list(
            knowledge_base_id=knowledge_base_id, limit=100
        )
        list_len_per_time = len(response_per_time.data)
        if list_len_per_time != 0:
            doc_list.extend(response_per_time.data)
        while list_len_per_time == 100:
            after_id = response_per_time.data[-1].id
            response_per_time = self.get_documents_list(
                knowledge_base_id=knowledge_base_id, after=after_id, limit=100
            )
            list_len_per_time = len(response_per_time.data)
            if list_len_per_time != 0:
                doc_list.extend(response_per_time.data)

        return doc_list
