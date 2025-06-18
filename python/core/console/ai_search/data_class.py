# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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

from pydantic import BaseModel, Field
from typing import Optional, Union, Annotated, List
from typing_extensions import Literal, override, TypeAlias


PropertyFormat = Literal["iso8601", "base64", "custom"]


class PropertyInfo:
    """Metadata class to be used in Annotated types to provide information about a given type.

    For example:

    class MyParams(TypedDict):
        account_holder_name: Annotated[str, PropertyInfo(alias='accountHolderName')]

    This means that {'account_holder_name': 'Robert'} will be transformed to
    {'accountHolderName': 'Robert'} before being sent to the API.
    """

    alias: Optional[str]
    format: Optional[PropertyFormat]
    format_template: Optional[str]
    discriminator: Optional[str]

    def __init__(
        self,
        *,
        alias: Optional[str] = None,
        format: Optional[PropertyFormat] = None,
        format_template: Optional[str] = None,
        discriminator: Optional[str] = None,
    ) -> None:
        self.alias = alias
        self.format = format
        self.format_template = format_template
        self.discriminator = discriminator

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(alias='{self.alias}', format={self.format}, "
            f"format_template='{self.format_template}', discriminator='{self.discriminator}')"
        )


class ImageURL(BaseModel):
    """image url"""

    url: str


class ImageURLContentBlock(BaseModel):
    """A block containing an image URL."""

    image_url: ImageURL
    type: Literal["image_url"] = "image_url"


class TextContentBlock(BaseModel):
    """A block containing plain text."""

    text: str = "text"
    type: Literal["text"]


MessageContent: TypeAlias = Annotated[
    Union[ImageURLContentBlock, TextContentBlock],
    PropertyInfo(discriminator="type"),
]


class Message(BaseModel):
    role: str = Field(..., description="角色设定，可选值：user：用户，assistant：模型")
    content: Union[str, list[MessageContent]] = Field(..., description="消息内容")


class SearchResource(BaseModel):
    """搜索资源类型模型。"""

    top_k: int = Field(..., description="要检索的搜索结果数量")
    type: str = Field(..., description="模态类型(网页/图片内容/视频)")


class PageTime(BaseModel):
    """时间过滤"""

    gth: Optional[str] = Field("")
    gt: Optional[str] = Field("")
    lth: Optional[str] = Field("")
    lt: Optional[str] = Field("")


class Range(BaseModel):
    """区间查找"""

    page_time: Optional[PageTime] = Field(
        None, description="模态类型(网页/图片内容/视频)"
    )


class Match(BaseModel):
    """匹配查找"""

    site: Optional[list[str]] = Field([], description="搜索站点")


class SearchFilter(BaseModel):
    """搜索资源类型模型。"""

    range: Optional[Range] = Field(None)
    match: Optional[Match] = Field(None)


class KnowledgeData(BaseModel):
    """知识数据模型。"""

    content: str = Field(..., description="知识内容")
    title: Optional[str] = Field(None, description="知识标题")
    url: Optional[str] = Field(None, description="知识链接")
    release_date: Optional[str] = Field(None, description="发布日期")


class Knowledge(BaseModel):
    """自定义知识模型。"""

    priority: Optional[int] = Field(
        0, ge=-20, le=20, description="优先级范围[-20,20],默认值0, 值越小优先级越高"
    )
    data_type: Optional[str] = Field(None, description="数据类型")
    id: Optional[int] = Field(None, description="知识ID")
    data: KnowledgeData = Field(..., description="详细知识内容")


class AISearchRequest(BaseModel):
    """
    请求参数：参考文档：https://cloud.baidu.com/doc/AppBuilder/s/amaxd2det
    """

    messages: List[Message] = Field(
        ...,
        description="搜索输入；array的长度需要是奇数, role必须是user-assistant-user交替，以user开始以user结束;在百度搜索时，仅支持单论输入，若传入多轮输入，则以用户传入最后的content为输入查询。",
    )
    search_source: Optional[str] = Field(
        "使用的搜索引擎版本；可选值：baidu_search_v1、baidu_search_v2。智能搜索生成时均可输入，兼容性考虑默认为baidu_search_v1。V2相比于V1：提升了性能表现，提升了数据内容的丰富度，更适用于结合大模型使用的场景，建议默认使用V2。"
    )
    resource_type_filter: Optional[List[SearchResource]] = Field(
        [SearchResource(type="web", top_k=20)], description="单次搜索最大返回数量。"
    )
    search_filter: Optional[SearchFilter] = Field(
        None,
        description="根据SearchFilter下的子条件做检索过滤，使用方式详见后文；仅search_source为baidu_search_v2时生效",
    )
    search_recency_filter: Optional[str] = Field(
        None,
        description="根据网页发布时间进行筛选；week:最近7天/month:最近30天/semiyear:最近180天/year:最近一年",
    )
    search_domain_filter: Optional[List[str]] = Field(
        None,
        description='支持设置基于站点的过滤条件，对搜索到的结果按指定站点进行筛选，仅返回来自所设站点的内容。例如：设置["baidu.com"] ，在搜索到的结果中仅返回来自 baidu.com 的搜索结果。',
    )
    model: Optional[str] = Field(
        None,
        description="使用的模型名。不传模型名称时，搜索模式为百度搜索，传入模型名称时则为智能搜索生成",
    )
    instruction: Optional[str] = Field(
        "", description="人设指令，用于设定输出风格等。注意：字符长度需要小于等于2000"
    )
    temperature: Optional[float] = Field(
        1e-10,
        gt=0,
        le=1,
        description="模型采样参数。较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定。",
    )
    top_p: Optional[float] = Field(
        1e-10,
        gt=0,
        le=1,
        description="模型采样参数。影响输出文本的多样性，取值越大，生成文本的多样性越强。",
    )
    prompt_template: Optional[str] = Field(
        None, description="面向高阶用户开放自定义prompt模版，普通用户不需要设置。"
    )
    search_mode: Optional[str] = Field(
        default="auto",
        description="搜索模式，默认auto，(auto:自动判断是否需要搜索/required:必须执行搜索/disabled:禁用搜索功能仅模型回答)",
    )
    enable_reasoning: Optional[bool] = Field(
        True,
        description="是否开启深度思考，仅对DeepSeek-R1、文心X1模型生效，开启后，在总结前会进行模型推理和思考并输出相关内容。",
    )
    enable_deep_search: Optional[bool] = Field(
        False,
        description="是否开启深搜索。深搜索会产生10次以内的智能搜索生成服务调用。",
    )
    additional_knowledge: Optional[List[Knowledge]] = Field(
        [],
        description="调用方提供的定制化知识内容集合，与公开的联网搜索结果构成合集，注入到模型中进行问答总结。知识注入的条数和长度， 与模型有关，限制最大10条。可以配合 priority（优先级参数）使用，让本地搜索结果在能回答问题时优先被采用。当前支持三个优先级：-1、0、1，数值越小优先级越高，回答时会优先选择高优先级的内容。其中，百度搜索结果的优先级为 0。",
    )
    max_completion_tokens: Optional[int] = Field(
        2048, description="默认2048，不同模型支持的最大输出token不一样。"
    )
    response_format: Optional[str] = Field(
        "auto",
        description="输出内容样式。默认值 auto。auto：智能判断是纯文本输出还是图文混排输出。text：文本输出。rich_text: 图文混排输出。如：在美食和旅游两个场景下，输出文本中嵌入markdown语法的图片内容。",
    )
    enable_corner_markers: Optional[bool] = Field(
        True,
        description="用于设置在最后生成的总结内容正文时，是否返回角标用于标记模型输出内容的参考来源。true：开启角标，false：隐藏角标。",
    )
    enable_followup_queries: Optional[bool] = Field(
        False,
        description="针对用户问题和大模型回答结果，给出推荐的追问。true: 开启追问。false：不开启追问。",
    )
    stream: Optional[bool] = Field(False, description="是否使用流式响应")
    safety_level: Optional[str] = Field(
        "standard", description="安全等级参数，standard-标准, strict-严格"
    )
    max_refer_search_items: Optional[int] = Field(
        100, description="调节用于模型问答总结的最大搜索条数，默认是全部搜索结果。"
    )
    config_id: Optional[str] = Field(
        None,
        description="指定使用该配置id下的领域知识注入、网页黑名单、问答干预策略等配置",
    )
    model_appid: Optional[str] = Field(None, description="模型调用appid")


class Usage(BaseModel):
    completion_tokens: Optional[int] = Field(None, description="完成的token数")
    prompt_tokens: Optional[int] = Field(None, description="提示的token数")
    total_tokens: Optional[int] = Field(None, description="总共的token数")


class VideoDetail(BaseModel):
    url: Optional[str] = Field(None, description="视频链接")
    height: Optional[str] = Field(None, description="视频高度")
    width: Optional[str] = Field(None, description="视频宽度")
    size: Optional[str] = Field(None, description="视频大小，单位Bytes")
    duration: Optional[str] = Field(None, description="视频长度，单位秒")
    hover_pic: Optional[str] = Field(None, description="视频封面图")


class ImageDetail(BaseModel):
    url: Optional[str] = Field(None, description="图片链接")
    height: Optional[str] = Field(None, description="图片高度")
    width: Optional[str] = Field(None, description="图片宽度")


class Reference(BaseModel):
    id: Optional[int] = Field(..., description="引用编号1、2、3")
    title: Optional[str] = Field(..., description="网页标题")
    url: Optional[str] = Field(..., description="网页地址")
    web_anchor: Optional[str] = Field(..., description="网站锚文本或网站标题")

    icon: Optional[str] = Field(None, description="站点图标")
    content: Optional[str] = Field(None, description="网站内容")
    date: Optional[str] = Field(None, description="网页日期")
    type: Optional[Literal["web", "image", "video"]] = Field(
        None, description="检索资源类型"
    )
    image: Optional[ImageDetail] = Field(None, description="图片详情")
    video: Optional[VideoDetail] = Field(None, description="视频详情")


class Delta(BaseModel):
    """
    AI响应增量数据对象，用于流式传输场景
    """

    content: str = Field(..., description="completion内容")
    role: Literal["assistant"] = Field(..., description="固定值assistant")
    reasoning_content: Optional[str] = Field(
        None,
        description="仅适用于 deepseek思考系列模型。内容为 assistant 消息中在最终答案之前的推理内容",
    )


class ChoiceMessage(BaseModel):
    """
    AI响应消息实体，封装完整对话交互数据
    """

    content: str = Field(..., min_length=1, description="生成内容主体，要求非空字符串")
    role: Literal["assistant"] = Field(
        "assistant", description="消息角色标识符，固定为assistant"
    )
    reasoning_content: Optional[str] = Field(
        None, min_length=1, description="推理逻辑内容，仅deepseek思考系列模型返回时有效"
    )


class Choice(BaseModel):
    """
    模型生成结果选择器，封装不同格式的响应输出
    """

    index: int = Field(..., ge=0, description="生成结果在选择列表中的序号，从0开始计数")
    finish_reason: Optional[Literal["stop", "length"]] = Field(
        None, description="生成终止原因：stop=自然停止 | length=长度限制"
    )
    message: Optional[ChoiceMessage] = Field(
        None, description="完整响应消息（非流式模式使用）"
    )
    delta: Optional[Delta] = Field(None, description="增量响应数据（流式模式使用）")


class AISearchResponse(BaseModel):
    request_id: str = Field(
        ...,
        description="请求request_id",
    )
    is_safe: Optional[bool] = Field(
        None,  description="query是否安全")
    choices: Optional[List[Choice]] = Field(
        None, min_items=1, description="	模型生成的 completion 的选择列表"
    )
    code: Optional[str] = Field(None, description="错误代码，当发生异常时返回")
    message: Optional[str] = Field(
        None, min_length=5, description="错误信息，当发生异常时返回"
    )
    usage: Optional["Usage"] = Field(None, description="token开销")
    references: Optional[List[Reference]] = Field(
        None, description="模型回答参考引用内容"
    )
    followup_queries: Optional[List[str]] = Field(
        None,
        description="追问问题",
    )
