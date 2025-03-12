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
from typing import Optional
from appbuilder.core._client import HTTPClient
from appbuilder.core.console.knowledge_base import data_class
from appbuilder.core.component import Message, Component
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.trace.tracer_wrapper import client_tool_trace


class KnowledgeBase(Component):
    r"""
    console知识库操作工具，用于创建、删除、查询、更新知识库等操作

    Examples:

    .. code-block:: python

        import os
        import appbuilder
        os.environ["APPBUILDER_TOKEN"] = "your_appbuilder_token"

        my_knowledge_base_id = "your_knowledge_base_id"
        my_knowledge = appbuilder.KnowledgeBase(my_knowledge_base_id)
        print("知识库ID: ", my_knowledge.knowledge_id)

        list_res = my_knowledge.describe_documents()
        print("文档列表: ", list_res)
    """

    def __init__(
        self,
        knowledge_id: Optional[str] = None,
        knowledge_name: Optional[str] = None,
        **kwargs
    ):
        r"""
        初始化KnowledgeBase类实例

        Args:
            knowledge_id (Optional[str]): 知识库ID
            knowledge_name (Optional[str]): 知识库名称
        """
        super().__init__(**kwargs)
        self.knowledge_id = knowledge_id
        self.knowledge_name = knowledge_name

    @classmethod
    @deprecated()
    def create_knowledge(cls, knowledge_name: str) -> "KnowledgeBase":
        r""" 创建知识库

        Deprecated: use create_knowledge_base instead

        Args:
            knowledge_name (str): 知识库名称

        Returns:
            KnowledgeBase: 返回一个KnowledgeBase对象
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

    @deprecated()
    def upload_file(
        self, file_path: str, client_token: str = None
    ) -> data_class.KnowledgeBaseUploadFileResponse:
        r"""
        上传文件到知识库

        Args:
            file_path (str): 文件路径
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            KnowledgeBaseUploadFileResponse: 返回一个KnowledgeBaseUploadFileResponse对象，包含以下属性：
            - request_id (int): 请求id
            - id (str): 文件id
            - name (dict): 文件名称
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

    @deprecated()
    def add_document(
        self,
        content_type: str,
        file_ids: list[str] = [],
        is_enhanced: bool = False,
        custom_process_rule: Optional[data_class.CustomProcessRule] = None,
        knowledge_base_id: Optional[str] = None,
        client_token: str = None,
    ) -> data_class.KnowledgeBaseAddDocumentResponse:
        r"""
        添加文档到知识库

        Args:
            content_type (str): 内容类型，可选值有"raw_text", "qa"。
            file_ids (List[str], optional): 文件ID列表。默认为空列表。
            is_enhanced (bool, optional): 是否增强。默认为False。
            custom_process_rule (Optional[data_class.CustomProcessRule], optional): 自定义处理规则。默认为None。
            knowledge_base_id (Optional[str], optional): 知识库ID。默认为None，此时使用当前类的knowledge_id属性。
            client_token (str): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            KnowledgeBaseAddDocumentResponse: 添加文档的相应结果。包含以下属性：
            - request_id (str): 请求ID
            - knowledge_base_id (str): 知识库ID
            - document_ids (list[str]): 成功新建的文档id集合
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
        r"""
        删除知识库中的文档

        Args:
            document_id (str): 文档ID
            knowledge_base_id (Optional[str], optional): 知识库ID。默认为None，此时使用当前类的knowledge_id属性。
            client_token (str): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            KnowledgeBaseDeleteDocumentResponse: 删除文档的响应消息,包含以下属性：
            - request_id (str): 请求ID
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

    def describe_documents(self, knowledge_base_id: Optional[str]=None, marker: Optional[str] = None, maxKeys: int = 10):
        r"""
        获取知识库中的文档列表
        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID。默认为None，此时使用当前类的knowledge_id属性。
            marker (Optional[str], optional): 分页标记。默认为None。
            maxKeys (int, optional): 最大键数。默认为10。

        Returns:
            DescribeDocumentsResponse: 描述文档的响应消息, 一个DescribeDocumentsResponse对象,包含以下属性：
            - data (list[DescribeDocument]): 切片列表
            - marker (str): 起始位置
            - isTruncated (bool): true表示后面还有数据，false表示已经是最后一页
            - nextMarker (str): 下一页起始位置
            - maxKeys (int): 本次查询包含的最大结果集数量
        """
        if self.knowledge_id == None and knowledge_base_id == None:
            raise ValueError(
                "knowledge_base_id cannot be empty, please call `create` first or use existing one"
            )

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgeBase?Action=DescribeDocuments")
        request = data_class.DescribeDocumentsRequest(
            knowledgeBaseId=knowledge_base_id or self.knowledge_id,
            marker=marker,
            maxKeys=maxKeys
        )
        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeDocumentsResponse(**data)
        return resp

    @deprecated("use describe_documents instead")
    def get_documents_list(
        self,
        limit: int = 10,
        after: Optional[str] = "",
        before: Optional[str] = "",
        knowledge_base_id: Optional[str] = None,
    ) -> data_class.KnowledgeBaseGetDocumentsListResponse:
        r"""
        获取知识库中的文档列表

        Args:
            limit (int, optional): 限制数量。默认为10。
            after (Optional[str], optional): 起始位置。默认为空字符串""。
            before (Optional[str], optional): 结束位置。默认为空字符串""。
            knowledge_base_id (Optional[str], optional): 知识库ID。默认为None，此时使用当前类的knowledge_id属性。

        Returns:
            KnowledgeBaseGetDocumentsListResponse: 知识库文档列表服务的响应消息,包含以下属性：
            - request_id (str): 请求ID
            - data (list[Document]): 文档信息列表
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
        clusterId: str = None,
        esUserName: str = None,
        esPassword: str = None,
        location: str = None,
        client_token: str = None,
        pathPrefix: str = None,
    ) -> data_class.KnowledgeBaseDetailResponse:
        r"""
        创建知识库

        Args:
            name (str): 知识库名称。
            description (str): 知识库描述。
            type (str, optional): 知识库类型。默认为"public"。
            esUrl (str, optional): Elasticsearch服务器地址。默认为None。
            esUserName (str, optional): Elasticsearch用户名。默认为None。
            esPassword (str, optional): Elasticsearch密码。默认为None。
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
            pathPrefix (str, optional): 知识库所属目录绝对路径。默认为None。


        Returns:
            KnowledgeBaseDetailResponse: 创建知识库的响应消息,包含以下属性：
            - id (str): 知识库ID
            - name (str): 知识库名称
            - description (Optional[str], optional): 知识库描述
            - config (Optional[KnowledgeBaseConfig], optional): 知识库配置
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
                    "clusterId": clusterId,
                    "username": esUserName,
                    "password": esPassword,
                    "location": location,
                },
            },
        )

        if pathPrefix != None:
            request.config.catalogue = {
                "pathPrefix": pathPrefix,
            }

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
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
        r"""
        获取知识库详情

        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。

        Returns:
            KnowledgeBaseDetailResponse: 知识库详情，返回一个KnowledgeBaseDetailResponse对象,包含以下属性：
            - id (str): 知识库ID
            - name(str): 知识库名称
            - description(Optional[str], optional): 知识库描述
            - config(Optional[KnowledgeBaseConfig], optional): 知识库配置
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
        pathPrefix: str = None,
    ):
        r"""
        修改知识库信息

        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
            name (Optional[str], optional): 新的知识库名称。默认值为None。
            description (Optional[str], optional): 新的知识库描述。默认值为None。
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。
            pathPrefix (str, optional): 知识库所属目录绝对路径。默认为None。

        Returns:
            dict: 响应数据，包含请求ID: requestId。
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

        if pathPrefix != None:
            request.config = {
                "catalogue": {
                    "pathPrefix": pathPrefix,
                }
            }

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=ModifyKnowledgeBase", client_token=client_token
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def delete_knowledge_base(
        self, knowledge_base_id: Optional[str] = None, client_token: str = None
    ):
        r"""
        删除知识库

        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            响应数据，包含请求ID: requestId
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
    ) -> data_class.KnowledgeBaseCreateDocumentsResponse:
        r"""
        创建文档

        Args:
            id (Optional[str], optional): 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
            contentFormat (str, optional): 文档内容格式，可以是"rawText"。默认值为""。
            source (data_class.DocumentSource, optional): 文档源数据。默认值为None。
            processOption (data_class.DocumentProcessOption, optional): 文档处理选项。默认值为None。
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            KnowledgeBaseCreateDocumentsResponse: 创建知识库文档的响应消息，返回一个KnowledgeBaseCreateDocumentsResponse对象，包含以下属性：
            - requestId (str): 请求ID
            - documentIds (list[str]): 文档ID列表
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
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.KnowledgeBaseCreateDocumentsResponse(**data)
        return resp

    def get_knowledge_base_list(
        self,
        knowledge_base_id: Optional[str] = None,
        maxKeys: int = 10,
        keyword: Optional[str] = None,
    ) -> data_class.KnowledgeBaseGetListResponse:
        r"""
        获取知识库列表

        Args:
            knowledge_base_id (Optional[str], optional): 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
            maxKeys (int, optional): 最大键数。默认值为10。
            keyword (Optional[str], optional): 关键字。默认值为None。

        Returns:
            KnowledgeBaseGetListResponse: 获取知识库列表的响应消息，返回一个KnowledgeBaseGetListResponse对象，包含以下属性：
            - requestId (str): 请求ID
            - data (list[KnowledgeBaseDetailResponse]): 知识库详情列表
            - marker (str): 起始位置
            - nextMarker (str): 下一页起始位置
            - maxKeys (int): 返回文档数量大小，默认10，最大值100
            - isTruncated (bool): 是否有更多结果
        """
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
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
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
    ) -> data_class.KnowledgeBaseUploadDocumentsResponse:
        r"""
        上传文档

        Args:
            file_path (str): 文件路径
            content_format (str, optional): 内容格式。默认值为"rawText"。
            id (Optional[str], optional): 知识库ID，如果不指定则使用当前实例的knowledge_id属性。默认值为None。
            processOption (data_class.DocumentProcessOption, optional): 文档处理选项。默认值为None。
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            KnowledgeBaseUploadDocumentsResponse: 创建知识库文档的响应消息，返回一个KnowledgeBaseUploadDocumentsResponse对象，包含以下属性：
            - requestId (str): 请求ID
            - documentId (str): 文档ID
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
            resp = data_class.KnowledgeBaseUploadDocumentsResponse(**data)

        return resp

    def create_chunk(
        self,
        documentId: str,
        content: str,
        client_token: str = None,
        knowledgebase_id: Optional[str] = None,
    ) -> data_class.CreateChunkResponse:
        r"""
        创建文档块

        Args:
            documentId (str): 文档ID
            content (str): 内容
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            CreateChunkResponse: 创建文档块的相应消息, 包含以下属性：
            - id (str): 切片ID
        """

        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=CreateChunk", client_token=client_token
        )

        request = data_class.CreateChunkRequest(
            knowledgeBaseId=knowledgebase_id or self.knowledge_id,
            documentId=documentId,
            content=content,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
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
        knowledgebase_id: Optional[str] = None,
        client_token: str = None,
    ):
        r"""
        修改文档块

        Args:
            chunkId (str): 文档块ID
            content (str): 内容
            enable (bool): 是否启用

        Returns:
            dict: 响应数据，包含请求ID: requestId
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=ModifyChunk", client_token=client_token
        )

        request = data_class.ModifyChunkRequest(
            knowledgeBaseId=knowledgebase_id or self.knowledge_id,
            chunkId=chunkId,
            content=content,
            enable=enable,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def delete_chunk(
        self,
        chunkId: str,
        knowledgebase_id: Optional[str] = None,
        client_token: str = None,
    ):
        r"""
        删除文档块

        Args:
            chunkId (str): 文档块ID
            client_token (str, optional): 客户端令牌。默认为None，此时会自动生成一个随机UUID作为客户端令牌。

        Returns:
            dict: 响应数据，包含请求ID: requestId
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        if not client_token:
            client_token = str(uuid.uuid4())
        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DeleteChunk", client_token=client_token
        )

        request = data_class.DeleteChunkRequest(
            knowledgeBaseId=knowledgebase_id or self.knowledge_id,
            chunkId=chunkId,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        return data

    def describe_chunk(
        self,
        chunkId: str,
        knowledgebase_id: Optional[str] = None,
    ) -> data_class.DescribeChunkResponse:
        r"""
        获取文档块详情

        Args:
            chunkId (str): 文档块ID

        Returns:
            DescribeChunkResponse: 文档块详情，一个DescribeChunkResponse对象,包含以下属性：
            - id (str): 切片ID
            - type (str): 切片类型
            - knowledgeBaseId (str): 知识库ID
            - documentId (str): 文档ID
            - content (str): 文档内容
            - enabled (bool): 是否启用
            - wordCount (int): 切片内字符数量
            - tokenCount (int): 切片内token数量
            - status (str): 切片状态
            - statusMessage (str): 切片状态信息
            - createTime (int): 创建时间
            - updateTime (int): 更新时间
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgeBase?Action=DescribeChunk")

        request = data_class.DescribeChunkRequest(
            knowledgeBaseId=knowledgebase_id or self.knowledge_id,
            chunkId=chunkId,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeChunkResponse(**data)
        return resp

    def describe_chunks(
        self,
        documentId: str,
        knowledgebase_id: Optional[str] = None,
        marker: str = None,
        maxKeys: int = None,
        type: str = None,
        keyword: str = None,
    ) -> data_class.DescribeChunksResponse:
        r"""
        获取文档块列表

        Args:
            documentId (str): 文档ID
            marker (str, optional): 分页标记，用于指定从哪个位置开始返回结果。默认为None，表示从头开始返回结果。
            maxKeys (int, optional): 最大返回数量，用于限制每次请求返回的最大文档块数目。默认为None，表示不限制返回数量。
            type (str, optional): 文档块类型。默认为None，表示不限定类型。
            keyword (str, optional): 根据关键字模糊匹配切片，最大长度2000字符。

        Returns:
            DescribeChunksResponse: 文档块列表，一个DescribeChunksResponse对象,包含以下属性：
            - data (list[DescribeChunkResponse]): 切片列表
            - marker (str): 起始位置
            - isTruncated (bool): true表示后面还有数据，false表示已经是最后一页
            - nextMarker (str): 下一页起始位置
            - maxKeys (int): 本次查询包含的最大结果集数量
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2(
            "/knowledgeBase?Action=DescribeChunks")

        request = data_class.DescribeChunksRequest(
            knowledgeBaseId=knowledgebase_id or self.knowledge_id,
            documentId=documentId,
            marker=marker,
            maxKeys=maxKeys,
            type=type,
            keyword=keyword,
        )

        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.DescribeChunksResponse(**data)
        return resp

    def get_all_documents(self, knowledge_base_id: Optional[str] = None) -> list:
        """
        获取知识库中所有文档。

        Args:
            knowledge_base_id (Optional[str], optional): 知识库的ID。如果为None，则使用当前实例的knowledge_id。默认为None。

        Returns:
            list: 包含所有文档的列表。

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

    def query_knowledge_base(
        self,
        query: str,
        knowledgebase_ids: list[str],
        type: Optional[data_class.QueryType] = None,
        metadata_filters: data_class.MetadataFilters = None,
        pipeline_config: data_class.QueryPipelineConfig = None,
        rank_score_threshold: Optional[float] = 0.4,
        top: int = 6,
        skip: int = None,
    ) -> data_class.QueryKnowledgeBaseResponse:
        """
        检索知识库

        Args:
            request (data_class.QueryKnowledgeBaseRequest): 检索知识库的请求对象

        Returns:
            data_class.QueryKnowledgeBaseResponse: 检索知识库的响应对象
        """
        headers = self.http_client.auth_header_v2()
        headers["content-type"] = "application/json"

        url = self.http_client.service_url_v2("/knowledgebases/query")
        request = data_class.QueryKnowledgeBaseRequest(
            query=query,
            knowledgebase_ids=knowledgebase_ids,
            type=type,
            metadata_filters=metadata_filters,
            pipeline_config=pipeline_config,
            rank_score_threshold=rank_score_threshold,
            top=top,
            skip=skip,
        )
        response = self.http_client.session.post(
            url=url, headers=headers, json=request.model_dump(
                exclude_none=True)
        )

        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        data = response.json()

        resp = data_class.QueryKnowledgeBaseResponse(**data)
        return resp
