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
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from typing import Union, Optional, List


class KnowledgeBaseUploadFileResponse(BaseModel):
    request_id: str = Field(..., description="请求ID")
    id: str = Field(..., description="文件ID")
    name: str = Field(..., description="文件名称")


class CustomProcessRule(BaseModel):
    separators: list[str] = Field(..., description="分段符号列表", example=[
                                  ",", "?"])
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
    url: Optional[str] = Field(None, description="原文件下载链接")
    mime_type: Optional[str] = Field(
        None,
        description="文件类型，目前支持doc/txt/docx/pdf/ppt/pptx/xlsx/xls/csv/json这几种文件类型。如果是通过url方式导入的文档，该值为url",
    )
    file_size: Optional[int] = Field(None, description="文件大小，单位bytes")


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


class DescribeDocumentsRequest(BaseModel):
    knowledgeBaseId: str = Field(..., description="知识库ID")
    marker: Optional[str] = Field(None, description="起始位置")
    maxKeys: int = Field(
        10, description="返回文档数量大小，默认10，最大值100"
    )


class DescribeDocumentMeata(BaseModel):
    source: Optional[str] = Field(None, description="文档来源")
    fileId: Optional[str] = Field(None, description="文档对应的文件ID")

class DescribeDocument(BaseModel):
    id: str = Field(..., description="文档ID")
    name: str = Field(..., description="文档名称")
    createdAt: str = Field(..., description="文档创建时间")
    wordCount: int = Field(..., description="文档字数")
    enabled: bool = Field(True, description="文档是否可用")
    displayStatus: str = Field(
        ...,
        description="文档状态。available：可用，queuing：排队中，notConfigured：数据待配置，parsing：解析中，indexing：处理中，parseError：解析失败，error：处理失败, retrainingSegmentUnusable：重建切片中，切片不可用, retrainErrSegmentUsable：重建切片错误，旧切片可用",
    )
    meta: Optional[DescribeDocumentMeata] = Field(..., description="文档元信息，包括source、fileId")


class DescribeDocumentsResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    marker: str = Field(..., description="起始位置")
    isTruncated: bool = Field(
        ..., description="true表示后面还有数据，false表示已经是最后一页"
    )
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(..., description="本次查询包含的最大结果集数量")
    data: list[DescribeDocument] = Field(..., description="文档信息列表")


class KnowledgeBaseConfigIndex(BaseModel):
    type: str = Field(..., description="索引类型", enum=["public", "bes", "vdb"])
    clusterId: Optional[str] = Field(None, description="集群/实例 ID")
    username: Optional[str] = Field(None, description="bes用户名")
    password: Optional[str] = Field(None, description="bes密码")
    location: Optional[str] = Field(
        None, description="托管资源的区域", enum=["bj", "bd", "sz", "gz"])


class KnowledgeBaseConfigCatalogue(BaseModel):
    pathPrefix: Optional[str] = Field(None, description="知识库所属目录绝对路径")


class KnowledgeBaseConfig(BaseModel):
    index: Optional[KnowledgeBaseConfigIndex] = Field(..., description="索引配置")
    catalogue: Optional[KnowledgeBaseConfigCatalogue] = Field(
        None, description="知识库目录配置")


class KnowledgeBaseCreateKnowledgeBaseRequest(BaseModel):
    name: str = Field(..., description="知识库名称")
    description: str = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")


class KnowledgeBaseGetDetailRequest(BaseModel):
    id: str = Field(..., description="知识库ID")


class KnowledgeBaseDetailResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    id: str = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(..., description="知识库配置")


class KnowledgeBaseModifyRequest(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: Optional[str] = Field(None, description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseConfig] = Field(None, description="知识库配置")


class KnowledgeBaseDeleteRequest(BaseModel):
    id: str = Field(..., description="知识库ID")


class KnowledgeBaseGetListRequest(BaseModel):
    marker: Optional[str] = Field(None, description="起始位置")
    keyword: Optional[str] = Field(None, description="搜索关键字")
    maxKeys: int = Field(
        10, description="返回文档数量大小，默认10，最大值100", le=100, ge=1
    )


class KnowledgeBaseGetListConfigIndex(BaseModel):
    type: str = Field(None, description="索引类型")
    esUrl: Optional[str] = Field('', description="es地址")


class KnowledgeBaseGetListConfig(BaseModel):
    index: Optional[KnowledgeBaseGetListConfigIndex] = Field(
        ..., description="索引配置")


class KnowledgeBaseGetListDetailResponse(BaseModel):
    id: str = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    config: Optional[KnowledgeBaseGetListConfig] = Field(
        ..., description="知识库配置")


class KnowledgeBaseGetListResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    data: list[KnowledgeBaseGetListDetailResponse] = Field(
        [], description="知识库详情列表")
    marker: str = Field(..., description="起始位置")
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(10, description="返回文档数量大小，默认10，最大值100")
    isTruncated: bool = Field(..., description="是否有更多结果")


class DocumentSourceUrlConfig(BaseModel):
    frequency: int = Field(
        ...,
        description="更新频率，目前支持的更新频率为-1(不自动更新),1（每天）,3（每3天）,7（每7天）,30（每30天）。",
    )


class DocumentSource(BaseModel):
    type: str = Field(..., description="数据来源类型", enum=["bos", "web"])
    urls: list[str] = Field(None, description="文档URL")
    urlDepth: int = Field(None, description="url下钻深度，1时不下钻")
    urlConfigs: Optional[list[DocumentSourceUrlConfig]] = Field(
        None, description="该字段的长度需要和source、urls字段长度保持一致。")


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
        None,
        description="chunker关联元数据，可选值为title (增加标题), filename(增加文件名)",
    )
    separator: Optional[DocumentSeparator] = Field(None, description="分段符号")
    pattern: Optional[DocumentPattern] = Field(None, description="正则表达式")


class DocumentProcessOption(BaseModel):
    template: str = Field(
        ...,
        description="模板类型，ppt: 模版配置—ppt幻灯片, resume：模版配置—简历文档, paper：模版配置—论文文档, custom：自定义配置—自定义切片, default：自定义配置—默认切分",
        enum=["ppt", "paper", "qaPair", "resume", " custom", "default"],
    )
    parser: Optional[DocumentChoices] = Field(
        None,
        description="解析方法(文字提取默认启动，参数不体现，layoutAnalysis版面分析，ocr光学字符识别，pageImageAnalysis文档图片解析，chartAnalysis图表解析，tableAnalysis表格深度解析，按需增加)",
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
        description="文档内容格式, (rawText 普通文件上传)"
    )
    processOption: Optional[DocumentProcessOption] = Field(
        None, description="文档处理选项"
    )


class KnowledgeBaseCreateDocumentsResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    documentIds: list[str] = Field(..., description="文档ID列表")


class KnowledgeBaseUploadDocumentsResponse(BaseModel):
    requestId: str = Field(..., description="请求ID")
    documentId: str = Field(..., description="文档ID")


class CreateChunkRequest(BaseModel):
    knowledgeBaseId: str = Field(None, description="知识库ID")
    documentId: str = Field(..., description="文档ID")
    content: str = Field(..., description="文档内容")


class CreateChunkResponse(BaseModel):
    id: str = Field(..., description="切片ID")


class ModifyChunkRequest(BaseModel):
    knowledgeBaseId: str = Field(None, description="知识库ID")
    chunkId: str = Field(..., description="切片ID")
    content: str = Field(..., description="文档内容")
    enable: bool = Field(..., description="是否启用")


class DeleteChunkRequest(BaseModel):
    knowledgeBaseId: str = Field(None, description="知识库ID")
    chunkId: str = Field(..., description="切片ID")


class DescribeChunkRequest(BaseModel):
    knowledgeBaseId: str = Field(None, description="知识库ID")
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
    knowledgeBaseId: str = Field(None, description="知识库ID")
    documentId: str = Field(..., description="文档ID")
    marker: Optional[str] = Field(None, description="起始位置")
    maxKeys: Optional[int] = Field(
        None, description="返回文档数量大小，默认10，最大值100"
    )
    type: Optional[str] = Field(
        None, description="切片类型。RAW：原文切片、NEW：新增切片、COPY：复制切片"
    )
    keyword: Optional[str] = Field(
        None, description="根据关键字模糊匹配切片，最大长度2000字符"
    )


class DescribeChunksResponse(BaseModel):
    data: list[DescribeChunkResponse] = Field(..., description="切片列表")
    marker: str = Field(..., description="起始位置")
    isTruncated: bool = Field(
        ..., description="true表示后面还有数据，false表示已经是最后一页"
    )
    nextMarker: str = Field(..., description="下一页起始位置")
    maxKeys: int = Field(..., description="本次查询包含的最大结果集数量")


class MetadataFilter(BaseModel):
    operator: str = Field(..., description="操作符名称。==:等于，in:在数组中，not_in:不在数组中")
    field: str = Field(None, description="字段名，目前支持doc_id")
    value: Union[str, list[str]] = Field(
        ..., description="字段值，如果是in操作符，value为数组"
    )


class MetadataFilters(BaseModel):
    filters: list[MetadataFilter] = Field(..., description="过滤条件")
    condition: str = Field(..., description="文档组合条件。and:与，or:或")


class PreRankingConfig(BaseModel):
    bm25_weight: float = Field(
        None, description="粗排bm25比重，取值范围在 [0, 1]，默认0.75"
    )
    vec_weight: float = Field(
        None, description="粗排向量余弦分比重，取值范围在 [0, 1]，默认0.25"
    )
    bm25_b: float = Field(
        None, description="控制文档长度对评分影响的参数，取值范围在 [0, 1]，默认0.75"
    )
    bm25_k1: float = Field(
        None,
        description="词频饱和因子，控制词频（TF）对评分的影响，常取值范围在 [1.2, 2.0]，默认1.5",
    )
    bm25_max_score: float = Field(
        None, description="得分归一化参数，不建议修改，默认50"
    )


class QueryType(str, Enum):
    FULLTEXT = "fulltext"  # 全文检索
    SEMANTIC = "semantic"  # 语义检索
    HYBRID = "hybrid"  # 混合检索


class ElasticSearchRetrieveConfig(BaseModel):  # 托管资源为共享资源 或 BES资源时使用该配置
    name: str = Field(..., description="配置名称")
    type: str = Field(None, description="elastic_search标志，该节点为es全文检索")
    threshold: float = Field(None, description="得分阈值，默认0.1")
    top: int = Field(None, description="召回数量，默认400")


class VectorDBRetrieveConfig(BaseModel):
    name: str = Field(..., description="该节点的自定义名称。")
    type: str = Field("vector_db", description="该节点的类型，默认为vector_db。")
    threshold: Optional[float] = Field(
        0.1, description="得分阈值。取值范围：[0, 1]", ge=0.0, le=1.0)
    top: Optional[int] = Field(
        400, description="召回数量。取值范围：[0, 800]", ge=0, le=800)
    pre_ranking: Optional[PreRankingConfig] = Field(None, description="粗排配置")


class SmallToBigConfig(BaseModel):
    name: str = Field(..., description="配置名称")
    type: str = Field(
        "small_to_big", description="small_to_big标志，该节点为small_to_big节点")


class RankingConfig(BaseModel):
    name: str = Field(..., description="配置名称")
    type: str = Field(None, description="ranking标志，该节点为ranking节点")
    inputs: list[str] = Field(
        ...,
        description='输入的节点名，如es检索配置的名称为pipeline_001，则该inputs为["pipeline_001"]',
    )
    model_name: str = Field(None, description="ranking模型名（当前仅一种，暂不生效）")
    top: int = Field(None, description="取切片top进行排序，默认20，最大400")


class QueryPipelineConfig(BaseModel):
    id: str = Field(
        None, description="配置唯一标识，如果用这个id，则引用已经配置好的QueryPipeline"
    )
    pipeline: list[Union[ElasticSearchRetrieveConfig, RankingConfig, VectorDBRetrieveConfig, SmallToBigConfig]] = Field(
        None, description="配置的Pipeline，如果没有用id，可以用这个对象指定一个新的配置"
    )


class QueryKnowledgeBaseRequest(BaseModel):
    query: str = Field(..., description="检索query")
    type: Optional[QueryType] = Field(
        None, description="检索策略的枚举, fulltext:全文检索, semantic:语义检索, hybrid:混合检索")
    top: int = Field(None, description="返回结果数量")
    skip: int = Field(
        None,
        description="跳过多少条记录, 通过top和skip可以实现类似分页的效果，比如top 10 skip 0，取第一页的10个，top 10 skip 10，取第二页的10个",
    )
    rank_score_threshold: float = Field(
        0.4,
        description="重排序匹配分阈值，只有rank_score大于等于该分值的切片重排序时才会被筛选出来。当且仅当，pipeline_config中配置了ranking节点时，该过滤条件生效。取值范围： [0, 1]。",
        ge=0.0,
        le=1.0,
    )
    knowledgebase_ids: list[str] = Field(..., description="知识库ID列表")
    metadata_filters: MetadataFilters = Field(None, description="元数据过滤条件")
    pipeline_config: QueryPipelineConfig = Field(None, description="检索配置")


class RowLine(BaseModel):
    key: str = Field(..., description="列名")
    index: int = Field(..., description="列号")
    value: str = Field(..., description="列值")
    enable_indexing: bool = Field(..., description="是否索引")
    enable_response: bool = Field(
        ...,
        description="是否参与问答（即该列数据是否对大模型可见）。当前值固定为true。",
    )


class ChunkLocation(BaseModel):
    page_num: list[int] = Field(..., description="页面")
    box: list[list[int]] = Field(
        ...,
        description="文本内容位置，在视觉上是文本框，格式是长度为4的int数组，含义是[x, y, width, height]",
    )


class Chunk(BaseModel):
    chunk_id: str = Field(..., description="切片ID")
    knowledgebase_id: str = Field(..., description="知识库ID")
    document_id: str = Field(..., description="文档ID")
    document_name: str = Field(None, description="文档名称")
    meta: dict = Field(None, description="文档元数据")
    chunk_type: str = Field(..., description="切片类型")
    content: str = Field(..., description="切片内容")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    retrieval_score: float = Field(..., description="粗检索得分")
    rank_score: float = Field(..., description="rerank得分")
    locations: ChunkLocation = Field(None, description="切片位置")
    children: List[Chunk] = Field(None, description="子切片")


class QueryKnowledgeBaseResponse(BaseModel):
    requestId: str = Field(None, description="请求ID")
    code: str = Field(None, description="状态码")
    message: str = Field(None, description="状态信息")
    chunks: list[Chunk] = Field(..., description="切片列表")
    total_count: int = Field(..., description="切片总数")
