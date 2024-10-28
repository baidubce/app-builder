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
import datetime


class KnowledgeBaseUploadFileResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    id: str = Field(..., description="文件ID")
    name: str = Field(..., description="文件名称")


class CustomProcessRule(BaseModel):
    separators: list[str] = Field(..., description="分段符号列表", example=[",", "?"])
    target_length: int = Field(..., description="分段最大长度", ge=300, le=1200)
    overlap_rate: float = Field(
        ..., description="分段重叠最大字数占比，推荐值0.25", ge=0, le=0.3, example=0.2
    )


class KnowledgeBaseAddDocumentRequest(BaseModel):
    knowledge_base_id: str = Field(..., description="知识库ID")
    content_type: str = Field(
        "raw_text", description="文档类型", enum=["raw_text", "qa"]
    )
    file_ids: list[str] = Field(..., description="文件ID列表")
    is_enhanced: bool = Field(False, description="是否开启知识增强")
    custom_process_rule: Optional[CustomProcessRule] = Field(
        None, description="自定义分段规则"
    )


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
    limit: int = Field(
        10, description="返回文档数量大小，默认10，最大值100", le=100, ge=1
    )
    after: str = Field(
        "",
        description="用于分页的游标。after 是一个文档的id，它定义了在列表中的位置。例如，如果你发出一个列表请求并收到 10个对象，以 app_id_123 结束，那么你后续的调用可以包含 after=app_id_123 以获取列表的下一页数据。",
    )
    before: str = Field(
        "",
        description="用于分页的游标。与after相反，填写它将获取前一页数据,如果和after都传，两个参数都会起到分页效果，维度是创建时间",
    )


class DocumentMeta(BaseModel):
    source: Optional[str] = Field(None, description="文档来源")
    file_id: Optional[str] = Field(None, description="文档对应的文件ID")


class Document(BaseModel):
    id: str = Field(..., description="文档ID")
    name: str = Field(..., description="文档名称")
    created_at: int = Field(..., description="文档创建时间")
    word_count: int = Field(..., description="文档字数")
    enabled: bool = Field(True, description="文档是否可用")
    meta: Optional[DocumentMeta] = Field(
        ..., description="文档元信息，包括source、file_id"
    )


class KnowledgeBaseGetDocumentsListResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    data: list[Document] = Field([], description="文档信息列表")


class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    esUrl: Optional[str] = Field(..., description="bes地址")
    username: Optional[str] = Field(None, description="bes用户名")
    password: Optional[str] = Field(None, description="bes密码")


class KnowledgeBaseConfig(BaseModel):
    index: Optional[KnowledgeBaseConfigIndex] = Field(..., description="索引配置")


class KnowledgeBaseCreateKnowledgeBaseRequest(BaseModel):
    name: str = Field(..., description="知识库名称")
    description: str = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")


class KnowledgeBaseGetDetailRequest(BaseModel):
    id: str = Field(..., description="知识库ID")


class KnowledgeBaseDetailResponse(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")


class KnowledgeBaseModifyRequest(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: Optional[str] = Field(None, description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")


class KnowledgeBaseDeleteRequest(BaseModel):
    id: str = Field(..., description="知识库ID")


class KnowledgeBaseGetListRequest(BaseModel):
    marker: str = Field(None, description="起始位置")
    keyword: Optional[str] = Field(None, description="搜索关键字")
    maxKeys: int = Field(
        10, description="返回文档数量大小，默认10，最大值100", le=100, ge=1
    )


class KnowledgeBaseGetListResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    data: list[KnowledgeBaseDetailResponse] = Field([], description="知识库详情列表")
    marker: str = Field(..., description="起始位置")
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(10, description="返回文档数量大小，默认10，最大值100")
    isTruncated: bool = Field(..., description="是否有更多结果")


class DocumentSource(BaseModel):
    type: str = Field(..., description="数据来源类型", enum=["bos", "web"])
    urls: list[str] = Field(None, description="文档URL")
    urlDepth: int = Field(None, description="url下钻深度，1时不下钻")


class DocumentChoices(BaseModel):
    choices: list[str] = Field(..., description="选择项")


class DocumentSeparator(BaseModel):
    separators: list[str] = Field(..., description="分段符号")
    targetLength: int = Field(..., description="分段最大长度")
    overlapRate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25")


class DocumentPattern(BaseModel):
    markPosition: str = Field(
        ...,
        description="命中内容放置策略, head：前序切片, tail：后序切片, drop：匹配后丢弃",
        enum=["head", "tail", "drop"],
    )
    regex: str = Field(..., description="正则表达式")
    targetLength: int = Field(..., description="分段最大长度")
    overlapRate: float = Field(..., description="分段重叠最大字数占比，推荐值0.25")


class DocumentChunker(BaseModel):
    choices: list[str] = Field(
        ...,
        description="使用哪些chunker方法 (separator | pattern | onePage)，separator：自定义切片—标识符，pattern：自定义切片—标识符中选择正则表达式，onePage：整文件切片",
    )
    prependInfo: list[str] = Field(
        ...,
        description="chunker关联元数据，可选值为title (增加标题), filename(增加文件名)",
    )
    separator: Optional[DocumentSeparator] = Field(..., description="分段符号")
    pattern: Optional[DocumentPattern] = Field(None, description="正则表达式")


class DocumentProcessOption(BaseModel):
    template: str = Field(
        ...,
        description="模板类型，ppt: 模版配置—ppt幻灯片, resume：模版配置—简历文档, paper：模版配置—论文文档, custom：自定义配置—自定义切片, default：自定义配置—默认切分",
        enum=["ppt", "paper", "qaPair", "resume", " custom", "default"],
    )
    parser: Optional[DocumentChoices] = Field(
        None,
        description="解析方法(文字提取默认启动，参数不体现，layoutAnalysis版面分析，ocr按需增加)",
    )
    knowledgeAugmentation: Optional[DocumentChoices] = Field(
        None,
        description="知识增强，faq、spokenQuery、spo、shortSummary按需增加。问题生成:faq、spokenQuery，段落摘要:shortSummary，三元组知识抽取:spo",
    )
    chunker: Optional[DocumentChunker] = Field(None, description="分段器类型")


class KnowledgeBaseCreateDocumentsRequest(BaseModel):
    id: str = Field(..., description="知识库ID")
    source: DocumentSource = Field(..., description="文档来源")
    contentFormat: str = Field(
        ...,
        description="文档内容格式, (rawText 普通文件上传 | qa 问答对)",
        enum=["rawText", "qa"],
    )
    processOption: Optional[DocumentProcessOption] = Field(
        None, description="文档处理选项"
    )


class CreateChunkRequest(BaseModel):
    documentId: str = Field(..., description="文档ID")
    content: str = Field(..., description="文档内容")


class CreateChunkResponse(BaseModel):
    id: str = Field(..., description="切片ID")


class ModifyChunkRequest(BaseModel):
    chunkId: str = Field(..., description="切片ID")
    content: str = Field(..., description="文档内容")
    enable: bool = Field(..., description="是否启用")


class DeleteChunkRequest(BaseModel):
    chunkId: str = Field(..., description="切片ID")


class DescribeChunkRequest(BaseModel):
    chunkId: str = Field(..., description="切片ID")


class DescribeChunkResponse(BaseModel):
    id: str = Field(..., description="切片ID")
    type: str = Field(..., description="切片类型")
    knowledgeBaseId: str = Field(..., description="知识库ID")
    documentId: str = Field(..., description="文档ID")
    content: str = Field(..., description="文档内容")
    enabled: bool = Field(..., description="是否启用")
    wordCount: int = Field(..., description="切片内字符数量")
    tokenCount: int = Field(..., description="切片内token数量")
    status: str = Field(..., description="切片状态")
    statusMessage: str = Field(..., description="切片状态信息")
    imageUrls: list[str] = Field(..., description="图片地址")
    createTime: int = Field(..., description="创建时间")
    updateTime: int = Field(None, description="更新时间")


class DescribeChunksRequest(BaseModel):
    documentId: str = Field(..., description="文档ID")
    marker: Optional[str] = Field(None, description="起始位置")
    maxKeys: Optional[int] = Field(
        None, description="返回文档数量大小，默认10，最大值100"
    )
    type: Optional[str] = Field(None, description="切片类型")


class DescribeChunksResponse(BaseModel):
    data: list[DescribeChunkResponse] = Field(..., description="切片列表")
    marker: str = Field(..., description="起始位置")
    isTruncated: bool = Field(
        ..., description="true表示后面还有数据，false表示已经是最后一页"
    )
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(..., description="本次查询包含的最大结果集数量")
