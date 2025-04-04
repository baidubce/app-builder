# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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

"""Component模块包括组件基类，用户自定义组件需要继承Component类，并至少实现run方法"""
import json

from enum import Enum

from pydantic import BaseModel
from pydantic import Field, field_validator
from typing import (
    Dict, List, Optional, Any, Generator, Union, AsyncGenerator)
from appbuilder.core.utils import ttl_lru_cache
from appbuilder.core._client import HTTPClient, AsyncHTTPClient
from appbuilder.core.message import Message

class ComponentArguments(BaseModel):
    """
    ComponentArguments define Component meta fields

    Attributes:
        name (str): component name.
        tool_desc (dict): component description.
    """
    name: str = ""
    tool_desc: Dict[str, Any] = {}

    def extract_values_to_dict(self):
        r"""extract ComponentArguments fields to dict"""

        inputs = {}
        for name, info in self.model_fields.items():
            value = getattr(self, name)
            # 获取 display_name 元数据
            if not info.json_schema_extra:
                continue
            variable_name = info.json_schema_extra.get('variable_name')
            if not variable_name:
                inputs[name] = value
                continue
            # 使用 Enum 成员的实际值
            if isinstance(value, Message):
                inputs[variable_name] = str(value.content)
            elif isinstance(value, Enum):
                inputs[variable_name] = str(value.value)
            else:
                inputs[variable_name] = str(value)
        return inputs


class Text(BaseModel, extra='allow'):
    info: str = Field(default="", description="具体文本内容")


class Code(BaseModel, extra='allow'):
    code: str = Field(default="", description="代码片段")


class Files(BaseModel, extra='allow'):
    filename: str = Field(default="", description="文件名")
    url: str = Field(default="", description="文件url")
    file_id: str = Field(default="", description="文件ID")


class Urls(BaseModel, extra='allow'):
    url: str = Field(default="", description="链接地址")


class OralText(BaseModel, extra='allow'):
    info: str = Field(default="", description="口语化文本内容")


class References(BaseModel, extra='allow'):
    type: str = Field(default="", description="类型")
    source: str = Field(default="", description="来源")
    doc_id: str = Field(default="", description="文档id")
    title: str = Field(default="", description="标题")
    content: str = Field(default="", description="内容")
    extra: Optional[dict] = Field(default={}, description="其他信息")


class Image(BaseModel, extra='allow'):
    filename: str = Field(default="", description="图片名称")
    url: str = Field(default="", description="图片url")
    base64: Optional[str] = Field(default="", description="图片base64数据")
    mime_type: Optional[str] = Field(default="jpeg", description="图片类型，如image/jpeg, 可选，默认jpeg")


class Chart(BaseModel, extra='allow'):
    type: str = Field(default="", description="图表类型")
    data: str = Field(default="", description="图表数据, json_str格式")


class Audio(BaseModel, extra='allow'):
    filename: str = Field(default="", description="音频名称")
    url: str = Field(default="", description="音频url")
    base64: Optional[str] = Field(default="", description="音频base64数据")
    mime_type: Optional[str] = Field(default="", description="音频类型，如mp3/wav, 可选，暂无默认值")


class PlanStep(BaseModel, extra='allow'):
    name: str = Field(default="", description="step名")
    arguments: dict = Field(default={}, description="step参数")
    thought: str = Field(default="", description="step思考结果")
    
class Task(BaseModel, extra='allow'):
    id: str = Field(default="", description="task id")
    name: str = Field(default="", description="task名")
    description: str = Field(default="", description="task描述")
    requires: list[str] = Field(default=[], description="依赖的task列表")
    tool: str = Field(default="", description="工具名")
    parameters: dict = Field(default={}, description="参数列表")
    status: str = Field(default="", description="task状态")

class Plan(BaseModel, extra='allow'):
    goal: str = Field(default="", description="计划目标")
    thought: str = Field(default="", description="计划思考结果")
    tasks: list[Task] = Field(default=[], description="任务列表")
    # deprecated parameters, delete when dte agent update
    detail: str = Field(default="", description="计划详情")
    steps: list[PlanStep] = Field(default=[], description="步骤列表")


class FunctionCall(BaseModel, extra='allow'):
    thought: str = Field(default="", description="思考结果")
    name: str = Field(default="", description="工具名")
    arguments: dict = Field(default={}, description="参数列表")


class Json(BaseModel, extra='allow'):
    data: str = Field(default="", description="json数据")
    
class ScreenShot(BaseModel, extra='allow'):
    browser_url: str = Field(default="", description="截图时的浏览器当前URL")
    url: str = Field(default="", description="图片URL (url, filename与data, mime_type二选一)")
    filename: str = Field(default="", description="图像文件名")
    mime_type: str = Field(default="image/jpeg", description="图片类型，如image/jpeg, image/png，可选，默认为image/jpeg")
    data: str = Field(default="", description="图片base64串 (url, filename与data, mime_type二选一)")
    file_id: str = Field(default="", description="图片文件ID")
    
    

class Content(BaseModel):
    name: str = Field(default="",
                      description="介绍当前yield内容的阶段名， 使用name的必要条件，是同一组件会输出不同type的content，并且需要加以区分，方便前端渲染与用户展示")
    visible_scope: str = Field(default="all",
                               description="为了界面展示明确的说明字段，三种取值：llm、user、all。llm为思考模型可见，类似function calling结果中submit的执行结果，user为终端用户可见，all包含上述两者")
    raw_data: dict = Field(default={},
                           description="raw_data是原始数据，可以是任何格式，比如json、html等，具体由开发者决定，用户上游请求结果透传，内部系统返回的信息，例如API节点收到的resp，大模型节点的MB resp")
    usage: dict = Field(default={},
                        description="大模型的token用量, ")
    metrics: dict = Field(default={},
                          description="耗时、性能、内存等trace及debug所需信息")
    type: str = Field(default="text",
                      description="代表event 类型，包括 text、code、files、urls、oral_text、references、image、chart、audio、screenshot、plan、function_call、json该字段的取值决定了下面text字段的内容结构")
    text: Union[Text, Code, Files, Urls, OralText, References, Image, Chart, Audio, Plan, Json, FunctionCall, ScreenShot] = Field(default=Text,
                                                                                                                      description="代表当前 event 元素的内容，每一种 event 对应的 text 结构固定")

    @field_validator('text', mode='before')
    def set_text(cls, v, values, **kwargs):
        if values.data['type'] == 'text':
            return Text(**v)
        elif values.data['type'] == 'code':
            return Code(**v)
        elif values.data['type'] == 'files':
            return Files(**v)
        elif values.data['type'] == 'urls':
            return Urls(**v)
        elif values.data['type'] == 'oral_text':
            return OralText(**v)
        elif values.data['type'] == 'references':
            return References(**v)
        elif values.data['type'] == 'image':
            return Image(**v)
        elif values.data['type'] == 'chart':
            return Chart(**v)
        elif values.data['type'] == 'audio':
            return Audio(**v)
        elif values.data['type'] == 'plan':
            return Plan(**v)
        elif values.data['type'] == 'function_call':
            return FunctionCall(**v)
        elif values.data['type'] == 'json':
            return Json(**v)
        elif values.data['type'] == 'screenshot':
            return ScreenShot(**v)
        else:
            raise ValueError(f"Invalid value for 'type': {values['type']}")


class ComponentOutput(BaseModel):
    role: str = Field(default="tool",
                      description="role是区分当前消息来源的重要字段，对于绝大多数组件而言，都是填写tool，标明role所在的消息来源为组件。部分思考及问答组件，role需要填写为assistant")
    content: list[Content] = Field(default=[],
                                   description="content是当前组件返回内容的主要payload，List[Content]，每个Content Dict 包括了当前输出的一个元素")


class Component:
    """
    Component基类, 其它实现的Component子类需要继承该基类，并至少实现run方法.

    Args:
        meta (ComponentArguments): component meta information.
        secret_key (str): user authentication token.
        gateway (str): backend gateway server address.
        lazy_certification (bool): lazy certification flag.
    """

    manifests = []

    def __init__(
        self,
        meta: Optional[ComponentArguments] = ComponentArguments(),
        secret_key: Optional[str] = None,
        gateway: str = "",
        lazy_certification: bool = False,
        is_aysnc: bool = False,
        **kwargs
    ):
        r"""Component初始化方法.

            参数:
                meta (obj: `ComponentArguments`, 可选) : component元信息.
                secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
                gateway(str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
                lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
            返回：
                无
        """
        self.meta = meta
        self.secret_key = secret_key
        self.gateway = gateway
        self._http_client = None
        self.lazy_certification = lazy_certification
        self.is_async = is_aysnc
        if not self.lazy_certification:
            self.set_secret_key_and_gateway(self.secret_key, self.gateway)

    def set_secret_key_and_gateway(self, secret_key: Optional[str] = None, gateway: str = ""):
        """
        设置密钥和网关地址。

        Args:
            secret_key (Optional[str], optional): 密钥，默认为None。如果未指定，则使用实例当前的密钥。
            gateway (str, optional): 网关地址，默认为空字符串。如果未指定，则使用实例当前的网关地址。

        Returns:
            None

        """
        self.secret_key = secret_key
        self.gateway = gateway
        # 因为子类可能重载init方法，导致没有is_async属性，所以此处需要判断一下
        try:
            self.is_async
        except AttributeError:
            # 目前async仅在AppBuilderClient中使用，所以没有async属性的组件都可以设置为False
            self.is_async = False

        if self.is_async:
            self._http_client = AsyncHTTPClient(self.secret_key, self.gateway)
        else:
            self._http_client = HTTPClient(self.secret_key, self.gateway)

    def set_model_info(self, model_name: str, model_url: str):
        """为llm component设置模型，其它component不生效"""
        pass

    @property
    def http_client(self):
        """
        获取 HTTP 客户端实例。

        Args:
            无

        Returns:
            HTTPClient: HTTP 客户端实例。

        """
        if self._http_client is None:
            if self.is_async:
                self._http_client = AsyncHTTPClient(
                    self.secret_key, self.gateway)
            else:
                self._http_client = HTTPClient(self.secret_key, self.gateway)
        return self._http_client

    def __call__(self, *inputs, **kwargs):
        r"""implement __call__ method"""
        return self.run(*inputs, **kwargs)

    def tool_eval(self, *input, **kwargs) -> Generator:
        """
        对给定的输入执行工具的FunctionCall。

        Args:
            *input: 一个可变数量的参数，代表输入数据。
            **kwargs: 关键字参数，可以包含任意数量的键值对，用于传递额外的参数。

        Returns:
            Generator[dict, ComponentOutput]: 生成器，生成字典和ComponentOutput类型的对象。

        Raises:
            NotImplementedError: 如果子类没有实现此方法，则抛出此异常。

        """
        raise NotImplementedError

    def run(self, *inputs, **kwargs) -> Message:
        """
        run method,待子类重写实现

        Args:
            inputs: list of arguments
            kwargs: keyword arguments
        """
        raise NotImplementedError

    def batch(self, *args, **kwargs) -> List[Message]:
        """
        批量处理输入并返回结果列表。

        Args:
            *args: 可变数量的输入参数，每个参数将依次被处理。
            **kwargs: 关键字参数，这些参数将被传递给每个输入的处理函数。

        Returns:
            List[Message]: 包含处理结果的列表，每个元素对应一个输入参数的处理结果。

        """

        results = [self.run(inp, **kwargs) for inp in args]
        return results

    def non_stream_tool_eval(self, *args, **kwargs) -> Union[ComponentOutput, dict]:
        """
        对工具评估结果进行非流式处理。

        Args:
            *args: 可变参数，具体参数依赖于调用的工具评估函数。
            **kwargs: 关键字参数，具体参数依赖于调用的工具评估函数。

        Returns:
            Union[ComponentOutput, dict]: 返回包含评估结果的 ComponentOutput 对象或字典。
                如果评估结果为空，则返回包含评估结果的字典。

        """
        result = ComponentOutput()
        result_content = []
        for iter_result in self.tool_eval(*args, **kwargs):
            result.role = iter_result.role
            result_content += iter_result.content
        result.content = result_content
        return result

    async def atool_eval(self, *args, **kwargs) -> AsyncGenerator:
        r"""
        atool_eval method,待子类重写实现

        Args:
            args: list of arguments
            kwargs: keyword arguments
        """
        return None

    async def arun(self, *args, **kwargs) -> Optional[Message]:
        r"""
        arun method,待子类重写实现

        Args:
            args: list of arguments
            kwargs: keyword arguments
        """
        return None

    async def abatch(self, *args, **kwargs) -> List[Message]:
        r"""
        abatch method,待子类重写实现

        Args:
            args: list of arguments
            kwargs: keyword arguments
        """
        return None

    def _trace(self, **data) -> None:
        r"""pass"""
        pass

    def _debug(self, **data) -> None:
        r"""pass"""
        pass

    def tool_desc(self) -> List[str]:
        r"""
        tool_desc method,待子类重写实现

        Args:
            None

        Returns:
            list of strings
        """
        return [json.dumps(manifest, ensure_ascii=False) for manifest in self.manifests]

    def tool_name(self) -> List[str]:
        r"""
        tool_name method,待子类重写实现

        Args:
            None

        Returns:
            list of strings
        """
        return [manifest["name"] for manifest in self.manifests]

    def create_langchain_tool(self, tool_name="", **kwargs):
        r"""
        create_langchain_tool method,将AB-SDK的Tool转换为LangChain的StructuredTool

        Args:
            tool_name: string, optional, default is empty string
            kwargs: keyword arguments

        Returns:
            StructuredTool
        """
        try:
            from langchain_core.tools import StructuredTool
        except ImportError:
            raise ImportError(
                "Please install langchain to use create_langchain_tool.")

        # NOTE(chengmo): 可以支持LangChain的组件，必须要求具备mainfest
        if self.manifests == []:
            raise ValueError(
                "Compnent {} No manifests found. Cannot convert it into LangChain Tool".format(type(self)))

        langchain_tool_json_schema = {}
        # NOTE(chengmo): 虽然现阶段，组件的mainfest列表中最多只有一个元素，但是需要兼容后期可能的多Tool的情况
        if len(self.manifests) > 1:
            if tool_name == "":
                raise ValueError(
                    "Multiple tools found, please use 'tool_name' specify which one to use.")

            for manifest in self.manifests:
                if manifest["name"] == tool_name:
                    langchain_tool_json_schema = manifest
                    break

            if langchain_tool_json_schema == {}:
                raise ValueError(
                    "Tool {} not found in mainfest.".format(tool_name))
        else:
            langchain_tool_json_schema = self.manifests[0]

        # NOTE(chengmo): 当前AB-SDK的Tool有两种情况
        # 1、存在tool_eval方法，则直接调用tool_eval方法，并设置stream=True, 汇总结果，封装成Message返回
        # 2、不存在tool_eval方法，则调用run方法，并设置 stream=False, 封装成Message返回
        has_tool_eval = self._has_implemented_tool_eval()
        langchain_tool_func = None
        if has_tool_eval:
            langchain_tool_func = self._langchain_tool_eval_implement
        else:
            langchain_tool_func = self._langchain_run_implement

        # NOTE(chengmo): name 及 description 都从mainfest中获取
        langchain_tool_name = langchain_tool_json_schema["name"]
        langchain_tool_description = langchain_tool_json_schema["description"]

        # NOTE(chengmo): 从mainfest中获取参数的json_schema，并转换成Pydantic的BaseModel
        from appbuilder.utils.json_schema_to_model import json_schema_to_pydantic_model
        try:
            import copy
            schema = copy.deepcopy(langchain_tool_json_schema["parameters"])
            schema["title"] = langchain_tool_name
            langchain_tool_model = json_schema_to_pydantic_model(
                schema,
                name_override=langchain_tool_name)
        except Exception as e:
            raise RuntimeError(
                "Failed to generate Pydantic model for tool schema: {}".format(e))

        return StructuredTool.from_function(
            func=langchain_tool_func,
            name=langchain_tool_name,
            description=langchain_tool_description,
            args_schema=langchain_tool_model,
            return_direct=False
        )

    def _has_implemented_tool_eval(self):
        has_tool_eval = False
        try:
            # 调用self.tool_eval方法，如果抛出NotImplementedError异常，则说明没有实现tool_eval方法
            self.tool_eval(**{'name': "", "streaming": False})
        except NotImplementedError:
            has_tool_eval = False
        else:
            has_tool_eval = True

        return has_tool_eval

    def _langchain_run_implement(self, **kwargs):
        # NOTE(chengmo): 调用run方法，并设置 stream=False, 封装成Message返回
        kwargs["stream"] = False
        return self.run(**kwargs)

    def _langchain_tool_eval_implement(self, **kwargs):
        # NOTE(chengmo): 调用tool_eval方法，并设置 stream=True, 封装成Message返回
        kwargs["stream"] = True
        kwargs["streaming"] = True
        res = self.tool_eval(**kwargs)

        final_result = ""

        # TODO(chengmo): 在组件标准化管理前，复用DTE对流式组件的处理逻辑
        for step in res:
            if isinstance(step, str):
                final_result += step
            else:
                final_result += step.get("text", "")
        return final_result

    @classmethod
    def create_output(cls, type, text, role="tool", name="", visible_scope="all", raw_data={}, usage={}, metrics={}):
        """create_text_output

        Args:
            type (str): 类型，包括"text", "code", "files", "urls", "oral_text", "references", "image", "chart", "audio", "plan", "function_call"
            text (str|dict): text字段，可输入str或dict
            role (str, optional): 当前消息来源. Defaults to "tool".
            name (str, optional): 当前yield内容的step name. Defaults to "".
            visible_scope (str, optional): 界面展示明确的说明字段. Defaults to "all".
            raw_data (dict, optional): 内部信息，由开发者请求透传. Defaults to {}.
            usage (dict, optional): 大模型的token用量. Defaults to {}.
            metrics (dict, optional): 耗时、性能、内存等trace及debug所需信息. Defaults to {}.

        Returns:
            ComponentOutput: 组件输出
        """
        if isinstance(text, str):
            if type == "text":
                text = {"info": text}
            elif type == "code":
                text = {"code": text}
            elif type == "urls":
                text = {"url": text}
            elif type == "oral_text":
                text = {"info": text}
            elif type == "json":
                text = {"data": text}
            else:
                raise ValueError(
                    "Only when type=text/code/urls/oral_text, string text is allowed! Please give dict text")
        elif isinstance(text, dict):
            if type == "text":
                key_list = ["info"]
            elif type == "code":
                key_list = ["code"]
            elif type == "oral_text":
                key_list = ["info"]
            elif type == "urls":
                key_list = ["url"]
            elif type == "files":
                key_list = ["filename", "url"]
            elif type == "references":
                key_list = ["type", "source", "doc_id", "title", "content"]
            elif type == "image":
                key_list = ["filename", "url"]
            elif type == "chart":
                key_list = ["type", "data"]
            elif type == "audio":
                key_list = ["filename", "url"]
            elif type == "plan":
                # add follow key_list when dte_agent update
                key_list = []#["goal", "thought", "tasks", "detail", "steps"]
            elif type == "function_call":
                key_list = ["thought", "name", "arguments"]
            elif type == "json":
                key_list = ["data"]
            elif type == "screenshot":
                key_list = ["browser_url"]
            else:
                raise ValueError("Unknown type: {}".format(type))
            assert all(key in text for key in key_list), "all keys:{} must be included in the text field".format(key_list)
        else:
            raise ValueError("text must be str or dict")

        assert role in [
            "tool", "assistant"], "role must be 'tool' or 'assistant'"
        result = {
            "role": role,
            "content": [{
                "type": type,
                "name": name,
                "text": text,
                "visible_scope": visible_scope,
                "raw_data": raw_data,
                "usage": usage,
                "metrics": metrics
            }]
        }
        return ComponentOutput(**result)