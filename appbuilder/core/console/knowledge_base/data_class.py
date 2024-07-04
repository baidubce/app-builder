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

from pydantic import BaseModel
from pydantic import Field
from typing import Union
from typing import Optional


class KnowledgeBaseUploadFileResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    id: str = Field(..., description="文件ID")
    name: str = Field(..., description="文件名称")


class CustomProcessRule(BaseModel):
    separators: list[str] = Field(..., description="分段符号列表", example=[",", "?"])
    target_length: int = Field(..., description="分段最大长度", ge=300, le=1200)
    overlap_rate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25", ge=0, le=0.3, example=0.2)


class KnowledgeBaseAddDocumentRequest(BaseModel):
    knowledge_base_id: str = Field(..., description="知识库ID")
    content_type: str = Field(
        'raw_text', description="文档类型", enum=["raw_text", "qa"])
    file_ids: list[str] = Field(..., description="文件ID列表")
    is_enhanced: bool = Field(False, description="是否开启知识增强")
    custom_process_rule: Optional[CustomProcessRule] = Field(
        None, description="自定义分段规则")


class KnowledgeBaseAddDocumentResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    knowledge_base_id: str = Field(..., description="知识库ID")
    document_ids: list[str] = Field(..., description="成功新建的文档id集合")


class KnowledgeBaseDeleteDocumentRequest(BaseModel):
    knowledge_base_id: str = Field(..., description="知识库ID")
    document_id: str = Field(..., description="待删除的文档id")


class KnowledgeBaseDeleteDocumentResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")


class KnowledgeBaseGetDocumentsListRequest(BaseModel):
    knowledge_base_id: str = Field(..., description="知识库ID")
    limit: int = Field(10, description="返回文档数量大小，默认10，最大值100", le=100, ge=1)
    after: str = Field(
        "", description="用于分页的游标。after 是一个文档的id，它定义了在列表中的位置。例如，如果你发出一个列表请求并收到 10个对象，以 app_id_123 结束，那么你后续的调用可以包含 after=app_id_123 以获取列表的下一页数据。")
    before: str = Field(
        "", description="用于分页的游标。与after相反，填写它将获取前一页数据,如果和after都传，两个参数都会起到分页效果，维度是创建时间")

class DocumentMeta(BaseModel):
    source: str = Field("", description="文档来源")
    file_id: str = Field("", description="文档对应的文件ID")

class Document(BaseModel):
    id: str = Field(..., description="文档ID")
    name: str = Field(..., description="文档名称")
    created_at: int = Field(..., description="文档创建时间")
    word_count: int = Field(..., description="文档字数")
    enabled: bool = Field(True, description="文档是否可用")
    meta: Optional[DocumentMeta] = Field(..., description="文档元信息，包括source、file_id")


class KnowledgeBaseGetDocumentsListResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    data: list[Document] = Field([], description="文档信息列表")